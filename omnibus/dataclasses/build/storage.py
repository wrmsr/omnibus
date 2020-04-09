"""
TODO:
 - class-level descriptor proto not optional / overridable, but instance level fully so
 - need to re-run checks/validators on all mutations
"""
import typing as ta

from ... import check
from ..internals import frozen_get_del_attr
from .context import BuildContext
from .context import FunctionBuildContext


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

    def install_frozen(self) -> None:
        for fn in frozen_get_del_attr(
                self.ctx.cls,
                self.ctx.spec.fields.instance,
                self.ctx.spec.globals
        ):
            if self.ctx.set_new_attribute(fn.__name__, fn):
                raise TypeError(f'Cannot overwrite attribute {fn.__name__} in class {self.fctx.ctx.cls.__name__}')

    def create_init_builder(self, fctx: FunctionBuildContext) -> 'Storage.InitBuilder':
        return self.InitBuilder(self, fctx)

    class InitBuilder:

        def __init__(self, owner: 'Storage', fctx: FunctionBuildContext) -> None:
            super().__init__()

            self._owner = check.isinstance(owner, Storage)
            self._fctx = check.isinstance(fctx, FunctionBuildContext)

        @property
        def owner(self) -> 'Storage':
            return self._owner

        @property
        def fctx(self) -> FunctionBuildContext:
            return self._fctx

        def build_field_assign(self, self_name, name, value) -> str:
            # FIXME: hidden impl detail - ALL ASSIGNS HAPPEN AT ONCE - gives storage impl option to setup/reorder
            if self.fctx.ctx.params.frozen:
                return f'BUILTINS.object.__setattr__({self_name}, {name!r}, {value})'

            return f'{self_name}.{name} = {value}'

        def build_field_init_lines(self, values_by_field: ta.Mapping[str, str], self_name: str) -> ta.List[str]:
            ret = []
            for field, value in values_by_field.items():
                ret.append(self.build_field_assign(self_name, field, value))
            return ret
