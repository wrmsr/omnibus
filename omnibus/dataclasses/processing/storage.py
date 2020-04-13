"""
TODO:
 - class-level descriptor proto not optional / overridable, but instance level fully so
 - need to re-run checks/validators on all mutations
 - nesting
 - rebuilding from existing
  - stubbing (query comp cache)
 - dc.replace
 - have to override __new__ for tups, pyr

NOTES:
 - can change ctor
  - config takes only a source
 - dc.replace has to work
  - is only way to modify tuple/pyrsistent / any frozen
   - backend.is_frozen

Backends:
 - default
  - slots
 - tuple
 - pyrsistent
 - struct
  - w/ bitfield packing
 - arrays
  - numpy
  - mmap
 - configs
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

    def process(self) -> None:
        pass

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

        def _build_field_assign(self, self_name, name, value) -> str:
            if self.fctx.ctx.params.frozen:
                return f'BUILTINS.object.__setattr__({self_name}, {name!r}, {value})'

            return f'{self_name}.{name} = {value}'

        def build_field_init_lines(self, values_by_field: ta.Mapping[str, str], self_name: str) -> ta.List[str]:
            ret = []
            for field, value in values_by_field.items():
                ret.append(self._build_field_assign(self_name, field, value))
            return ret
