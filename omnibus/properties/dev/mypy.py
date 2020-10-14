import typing as ta

import mypy.plugin as mp
import mypy.types as mt


class TypeIgnoreRegionPlugin(mp.Plugin):

    def get_function_hook(self, fullname: str) -> ta.Optional[ta.Callable[[mp.FunctionContext], mt.Type]]:
        raise NotImplementedError
