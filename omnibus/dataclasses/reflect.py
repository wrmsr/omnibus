"""
TODO:
 - *spec is authoritative*
 - delegate to backends
"""
import dataclasses as dc
import typing as ta
import weakref

from .. import check
from .. import defs
from .. import properties
from .defdecls import ClsDefdecls
from .defdecls import get_cls_defdecls
from .internals import DataclassParams
from .internals import PARAMS
from .types import ExtraParams
from .types import METADATA_ATTR


Field = dc.Field


REFLECTS_BY_CLS = weakref.WeakKeyDictionary()


class DataReflect:

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

    @property
    def extra_params(self) -> ExtraParams:
        return self._extra_params

    @properties.cached
    def metadata(self) -> ta.Mapping[type, ta.Any]:
        return self.cls.__dict__.get(METADATA_ATTR, {})

    @properties.cached
    def fields(self) -> ta.Sequence[Field]:
        return dc.fields(self._cls)

    @properties.cached
    def fields_by_name(self) -> ta.Mapping[str, Field]:
        return {fld.name: fld for fld in self.fields}

    @properties.cached
    def defdecls(self) -> ClsDefdecls:
        return get_cls_defdecls(self._cls)


def get_cls_reflect(cls: type) -> DataReflect:
    try:
        return REFLECTS_BY_CLS[cls]
    except KeyError:
        spec = REFLECTS_BY_CLS[cls] = DataReflect(cls)
        return spec
