import dataclasses as dc
import sys
import types
import typing as ta
import weakref

from .. import check
from .. import collections as ocol
from .. import defs
from .. import properties
from .fields import Fields
from .internals import DataclassParams
from .internals import FIELDS
from .internals import PARAMS
from .types import ExtraParams
from .types import Extras
from .types import METADATA_ATTR
from .types import MetaParams


Field = dc.Field


TypeT = ta.TypeVar('TypeT', bound=type, covariant=True)


REFLECTS_BY_CLS = weakref.WeakKeyDictionary()


class DataSpec(ta.Generic[TypeT]):

    def __init__(self, cls: TypeT) -> None:
        super().__init__()

        self._cls = check.isinstance(cls, type)

    defs.repr('cls')

    @property
    def cls(self) -> TypeT:
        return self._cls

    @properties.cached
    @property
    def params(self) -> DataclassParams:
        check.state(hasattr(self._cls, PARAMS))
        return check.isinstance(getattr(self._cls, PARAMS), DataclassParams)

    @properties.cached
    @property
    def _metadata(self) -> ta.Mapping[type, ta.Any]:
        return self.cls.__dict__.get(METADATA_ATTR, {})

    @properties.cached
    @property
    def metadata(self) -> ta.Mapping[type, ta.Any]:
        return types.MappingProxyType(self._metadata)

    @properties.cached
    @property
    def extra_params(self) -> ExtraParams:
        return self.metadata.get(ExtraParams, ExtraParams())

    @properties.cached
    @property
    def meta_params(self) -> MetaParams:
        return self.metadata.get(MetaParams, MetaParams())

    @properties.cached
    @property
    def fields(self) -> Fields:
        check.state(hasattr(self._cls, FIELDS))
        return Fields(getattr(self._cls, FIELDS).values())

    @property
    def rmro(self) -> ta.Sequence[type]:
        return tuple(reversed(self.cls.__mro__))

    @properties.cached
    def rmro_extras(self) -> ta.Sequence[ta.Any]:
        return tuple(
            e
            for c in self.rmro
            for e in c.__dict__.get(METADATA_ATTR, {}).get(Extras, [])
        )

    @properties.cached
    def rmro_extras_by_cls(self) -> ocol.ItemSeqTypeMap:
        return ocol.ItemSeqTypeMap(self.rmro_extras)

    @properties.cached
    def globals(self) -> ta.MutableMapping[str, ta.Any]:
        if self.cls.__module__ in sys.modules:
            return sys.modules[self.cls.__module__].__dict__
        else:
            return {}


def get_cls_spec(cls: type) -> DataSpec:
    try:
        return REFLECTS_BY_CLS[cls]
    except KeyError:
        spec = REFLECTS_BY_CLS[cls] = DataSpec(cls)
        return spec
