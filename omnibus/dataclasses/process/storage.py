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
import dataclasses as dc
import typing as ta

from ..internals import FieldType
from ..internals import get_field_type
from .types import Aspect
from .types import attach
from .types import InitPhase


class Storage(Aspect):

    @attach('init')
    class Init(Aspect.Function['Storage']):

        def _build_field_assign(self, self_name, name, value) -> str:
            if self.fctx.ctx.params.frozen:
                return f'BUILTINS.object.__setattr__({self_name}, {name!r}, {value})'

            return f'{self_name}.{name} = {value}'

        @attach(InitPhase.SET_ATTRS)
        def build_set_attr_lines(self) -> ta.List[str]:
            ret = []
            for f in self.fctx.ctx.spec.fields.init:
                if get_field_type(f) is FieldType.INIT:
                    continue
                if not f.init and f.default_factory is dc.MISSING:
                    continue
                ret.append(self._build_field_assign(self.fctx.self_name, f.name, f.name))
            return ret
