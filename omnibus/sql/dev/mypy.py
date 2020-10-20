import typing as ta

import mypy.plugin as mp
import mypy.types as mt


class SqlAlchemyPlugin(mp.Plugin):

    def get_function_hook(self, fullname: str) -> ta.Optional[ta.Callable[[mp.FunctionContext], mt.Type]]:
        if fullname == 'sqlalchemy.sql.elements.BindParameter':
            def inner(ctx: mp.FunctionContext) -> mt.Type:
                return mt.Instance(
                    ctx.default_return_type.type,
                    [],
                    line=ctx.default_return_type.line,
                    column=ctx.default_return_type.column,
                )
            return inner
        return None
