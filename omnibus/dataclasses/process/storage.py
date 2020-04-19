"""
TODO:
 - need to re-run checks/validators on all mutations
 - nesting
 - rebuilding from existing
  - stubbing (query comp cache)

Backends:
 - struct
  - w/ bitfield packing
 - arrays
  - numpy
  - mmap
 - configs
"""
import dataclasses as dc
import typing as ta

from ... import lang
from ... import properties
from ..internals import FieldType
from ..internals import get_field_type
from .types import Aspect
from .types import attach
from .types import InitPhase


StorageT = ta.TypeVar('StorageT', bound='Storage', covariant=True)


class Storage(Aspect, lang.Abstract):

    class Function(Aspect.Function[StorageT]):

        @properties.cached
        def setattr_name(self) -> str:
            return self.fctx.nsb.put(object.__setattr__, '__setattr__')

        def build_setattr(self, name: str, value: str) -> str:
            if self.fctx.ctx.params.frozen:
                return f'{self.setattr_name}({self.fctx.self_name}, {name!r}, {value})'
            else:
                return f'{self.fctx.self_name}.{name} = {value}'


class StandardStorage(Storage):

    @attach('init')
    class Init(Storage.Function['StandardStorage']):

        @attach(InitPhase.SET_ATTRS)
        def build_set_attr_lines(self) -> ta.List[str]:
            ret = []
            for f in self.fctx.ctx.spec.fields.init:
                if get_field_type(f) is FieldType.INIT:
                    continue
                if not f.init and f.default_factory is dc.MISSING:
                    continue
                ret.append(self.build_setattr(f.name, f.name))
            return ret
