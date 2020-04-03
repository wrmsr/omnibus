import dataclasses as dc_
import typing as ta
import weakref

from .. import check
from .. import defs
from .. import properties


Field = dc_.Field


INFO_BY_CLS = weakref.WeakKeyDictionary()


class DataclassInfo:

    def __init__(self, cls: type) -> None:
        super().__init__()

        check.arg(dc_.is_dataclass(cls))
        self._cls = check.isinstance(cls, type)

    defs.repr('cls')

    @property
    def cls(self) -> type:
        return self._cls

    @properties.cached
    def fields(self) -> ta.Sequence[Field]:
        return dc_.fields(self._cls)

    @properties.cached
    def fields_by_name(self) -> ta.Mapping[str, Field]:
        return {fld.name: fld for fld in self.fields}

    def _get_merged_mro_attr_list(self, att: str) -> ta.List:
        return [v for c in reversed(self._cls.__mro__) for v in getattr(c, att, [])]

    @properties.cached
    def field_validators(self) -> ta.List:
        return self._get_merged_mro_attr_list('__dataclass_field_validators__')

    @properties.cached
    def validators(self) -> ta.List:
        return self._get_merged_mro_attr_list('__dataclass_validators__')


def get_info(cls: type) -> DataclassInfo:
    try:
        return INFO_BY_CLS[cls]
    except KeyError:
        info = INFO_BY_CLS[cls] = DataclassInfo(cls)
        return info
