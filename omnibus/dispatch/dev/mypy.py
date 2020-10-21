"""
TODO:
 - if can't do per-func do as class wrapper - read mro, rewrite nodes as if wrapped in @typing.overload
  - customize_class_mro is only callee
"""
import typing as ta

import mypy.plugin as mp


class DispatchPlugin(mp.Plugin):

    def get_customize_class_mro_hook(self, fullname: str) -> ta.Optional[ta.Callable[[mp.ClassDefContext], None]]:
        def inner(ctx: mp.ClassDefContext) -> None:  # noqa
            pass
        return inner
