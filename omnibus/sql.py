import io
import re
import typing as ta

import sqlalchemy.dialects  # noqa
import sqlalchemy.ext.compiler  # noqa
import sqlalchemy.pool  # noqa
import sqlalchemy as sa

from . import check
from . import lang


lang.warn_unstable()


def yield_sql_statements(body: str) -> ta.Iterator[str]:
    """Lame and shameful."""

    buf = io.StringIO()
    for line in body.split('\n'):
        stripped = line.strip()
        if stripped.startswith('--'):
            continue
        check.arg('/*' not in stripped)
        check.arg(stripped.rfind(';', 0, -1) < 0)
        if stripped.endswith(';'):
            buf.write(line.rpartition(';')[0])
            stmt = buf.getvalue().strip()
            if stmt:
                yield stmt
            buf = io.StringIO()
        else:
            buf.write(line)
            buf.write('\n')
    if buf.tell() > 0:
        stmt = buf.getvalue().strip()
        if stmt:
            yield stmt


VARIABLE_PATTERN = re.compile(r'[A-Za-z_]+')


def variable(name: str, type=None):
    check.arg(VARIABLE_PATTERN.fullmatch(name) is not None)
    return sa.literal_column('@' + name, type)


class SetVariables(sa.sql.expression.Executable, sa.sql.expression.ClauseElement):

    def __init__(
            self,
            updates: ta.List[ta.Tuple[sa.sql.ColumnElement, sa.sql.Selectable]],
    ) -> None:
        super().__init__()
        self.updates = updates


@sa.ext.compiler.compiles(SetVariables)
def visit_set_variables(element, compiler, **kw):
    stmt = 'SET %s' % (
        ', '.join('%s = %s' % (compiler.preparer.format_column(c), v._compiler_dispatch(compiler))
                  for c, v in element.updates),
    )
    return stmt


class ParenExpression(sa.sql.expression.UnaryExpression):

    __visit_name__ = 'paren'


paren = ParenExpression


@sa.ext.compiler.compiles(ParenExpression)
def visit_paren(element, compiler, **kw):
    return '(%s)' % (element.element._compiler_dispatch(compiler),)


class CustomEscape:

    def __init__(self, escape: ta.Union[ta.Callable[[], str], str]) -> None:
        super().__init__()
        check.arg(callable(escape) or isinstance(escape, str))
        self.escape = escape

    def __call__(self):
        if callable(self.escape):
            return self.escape()
        elif isinstance(self.escape, str):
            return self.escape
        else:
            raise TypeError(repr(self.escape))


@lang.cached_nullary
def _dummy_pymysql_connection():
    import pymysql.connections

    class DummyPymysqlConnection(pymysql.connections.Connection):

        def connect(self, sock=None):
            self.charset = 'utf8mb4'

            # See pymysql.constants.CLIENT for details unpacking
            self.server_capabilities = 0x807ff7ff

            self.server_charset = 'latin1'
            self.server_language = 8
            self.server_status = 0

        def execute(self, query, args=None):
            raise NotImplementedError

        def executemany(self, query, args):
            raise NotImplementedError

        def escape(self, obj, mapping=None):
            if isinstance(obj, CustomEscape):
                return obj()
            else:
                return super().escape(obj, mapping=mapping)

    return DummyPymysqlConnection


@lang.cached_nullary
def _MySQLDialect_dummypymysql():
    import sqlalchemy.dialects.mysql.pymysql  # noqa

    class __MySQLDialect_dummypymysql(sa.dialects.mysql.pymysql.MySQLDialect_pymysql):
        driver = 'dummypymysql'

        def connect(self, *cargs, **cparams):
            return _dummy_pymysql_connection()(*cargs, **cparams)

        def initialize(self, connection):
            pass

        def do_execute(self, cursor, statement, parameters, context=None):
            raise NotImplementedError

        def do_rollback(self, dbapi_connection):
            pass

    globals()['__MySQLDialect_dummypymysql'] = __MySQLDialect_dummypymysql
    sa.dialects.registry.register(
        'dummypymysql',
        __MySQLDialect_dummypymysql.__module__,
        __MySQLDialect_dummypymysql.__name__,
    )

    return __MySQLDialect_dummypymysql


def _create_pymysql_dummy_engine() -> sa.engine.Engine:
    _MySQLDialect_dummypymysql()

    def creator(*cargs, **cparams):
        return _dummy_pymysql_connection()(*cargs, **cparams)

    dialect = sa.dialects.registry.load('dummypymysql')()
    engine = sa.engine.base.Engine(sa.pool.NullPool(creator, dialect=dialect), dialect, 'dummy')
    dialect.engine_created(engine)
    return engine


def pymysql_render_statement(elem, *multiparams, **params) -> str:
    engine = _create_pymysql_dummy_engine()
    dialect = engine.dialect

    distilled_params = sa.cutils._distill_params(multiparams, params)
    if distilled_params:
        # note this is usually dict but we support RowProxy
        # as well; but dict.keys() as an iterable is OK
        keys = distilled_params[0].keys()
    else:
        keys = []

    with engine.connect() as connection:
        compiled = elem.compile(
            dialect=dialect,
            column_keys=keys,
            inline=len(distilled_params) > 1,
            schema_translate_map=engine.schema_for_object
            if not engine.schema_for_object.is_default else None
        )

        context = dialect.execution_ctx_cls._init_compiled(
            dialect,
            connection,
            connection.connection,
            compiled,
            distilled_params
        )

        cursor = context.cursor
        statement = context.statement
        parameters = context.parameters

        if not context.executemany:
            parameters = parameters[0]

        statement = cursor.mogrify(statement, parameters)

        return statement
