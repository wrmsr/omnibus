"""
TODO:
 - class-level descriptor proto not optional / overridable, but instance level fully so
 - need to re-run checks/validators on all mutations
"""
import typing as ta

from ... import check
from ..internals import frozen_get_del_attr
from .context import BuildContext


class Storage:

    def __init__(self, ctx: BuildContext) -> None:
        super().__init__()

        self._ctx = check.isinstance(ctx, BuildContext)

    @property
    def ctx(self) -> BuildContext:
        return self._ctx

    def set_new_attribute(self, name: str, value: ta.Any) -> bool:
        if name in self.ctx.cls.__dict__:
            return True
        setattr(self.ctx.cls, name, value)
        return False

    def install_field_attrs(self) -> None:
        for f in self.ctx.spec.fields:
            setattr(self.ctx.cls, f.name, f)

    def install_frozen(self) -> None:
        for fn in frozen_get_del_attr(self.ctx.cls, self.ctx.spec.fields.instance, self.ctx.spec.globals):
            if self.set_new_attribute(fn.__name__, fn):
                raise TypeError(f'Cannot overwrite attribute {fn.__name__} in class {self.ctx.cls.__name__}')

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
