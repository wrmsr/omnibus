"""
TODO:
 - *spec is authoritative*
 - delegate to backends
"""
import dataclasses as dc
import types
import typing as ta
import weakref

from .. import check
from .. import defs
from .. import properties
from .fields import Fields
from .internals import DataclassParams
from .internals import PARAMS
from .types import ExtraParams
from .types import METADATA_ATTR


Field = dc.Field


REFLECTS_BY_CLS = weakref.WeakKeyDictionary()


class DataSpec:

    def __init__(self, cls: type) -> None:
        super().__init__()

        check.arg(dc.is_dataclass(cls))
        self._cls = check.isinstance(cls, type)

    defs.repr('cls')

    @property
    def cls(self) -> type:
        return self._cls

    @properties.cached
    def params(self) -> DataclassParams:
        return check.isinstance(getattr(self._cls, PARAMS), DataclassParams)

    @properties.cached
    def metadata(self) -> ta.Mapping[type, ta.Any]:
        return self.cls.__dict__.get(METADATA_ATTR, types.MappingProxyType({}))

    @property
    def extra_params(self) -> ExtraParams:
        return self.metadata.get(ExtraParams, ExtraParams())

    @properties.cached
    def fields(self) -> Fields:
        return Fields(dc.fields(self._cls))


def get_cls_spec(cls: type) -> DataSpec:
    try:
        return REFLECTS_BY_CLS[cls]
    except KeyError:
        spec = REFLECTS_BY_CLS[cls] = DataSpec(cls)
        return spec
