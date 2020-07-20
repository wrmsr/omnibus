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
from ..internals import FieldType
from ..internals import get_field_type
from .access import Access
from .types import Aspect
from .types import attach
from .types import InitPhase


StorageT = ta.TypeVar('StorageT', bound='Storage', covariant=True)


class Storage(Aspect, lang.Abstract):

    class Function(Aspect.Function[StorageT]):
        pass


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
                ret.append(self.fctx.get_aspect(Access.Function).build_setattr(f.name, f.name))
            return ret
