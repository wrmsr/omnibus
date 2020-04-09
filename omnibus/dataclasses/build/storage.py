"""
TODO:
 - class-level descriptor proto not optional / overridable, but instance level fully so
 - validators
"""
import typing as ta

from ... import check
from .context import BuildContext


class Storage:

    def __init__(self, ctx: BuildContext) -> None:
        super().__init__()

        self._ctx = check.isinstance(ctx, BuildContext)

    @property
    def ctx(self) -> BuildContext:
        return self._ctx

    def install_field_attrs(self) -> None:
        for f in self.ctx.spec.fields:
            setattr(self.ctx.cls, f.name, f)

    def build_field_assign(self, self_name, name, value) -> str:
        # FIXME: hidden impl detail - ALL ASSIGNS HAPPEN AT ONCE - gives storage impl option to setup/reorder
        if self.ctx.params.frozen:
            return f'BUILTINS.object.__setattr__({self_name}, {name!r}, {value})'

        return f'{self_name}.{name} = {value}'

    def build_field_init_lines(self, values_by_field: ta.Mapping[str, str], self_name: str) -> ta.List[str]:
        ret = []
        for field, value in values_by_field.items():
            ret.append(self.build_field_assign(self_name, field, value))
        return ret
