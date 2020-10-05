import sqlalchemy as sa
import sqlalchemy.pool  # noqa

import pytest

from .. import instrument as inst
from ... import lang


@pytest.mark.xfail()
def test_instrument():
    from sqlalchemy.dialects.postgresql.pg8000 import PGDialect_pg8000
    dia = inst.create_instrumented_dialect(PGDialect_pg8000)
    assert issubclass(dia, PGDialect_pg8000)

    from sqlalchemy.dialects.sqlite import dialect as sqlite_dialect
    inst.create_instrumented_dialect(sqlite_dialect)

    engine: sa.engine.Engine
    with lang.disposing(
            sa.create_engine(
                'sqlite__omnibus_sql_instrumented://',
                connect_args={'check_same_thread': False},
                poolclass=sa.pool.StaticPool,
            )
    ) as engine:
        with engine.connect() as conn:
            print(list(conn.execute('select 1')))
