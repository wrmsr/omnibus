import dataclasses as dc
import typing as ta

from .. import properties
from .internals import FieldType
from .internals import get_field_type


class Fields(ta.Sequence[dc.Field]):

    def __init__(self, fields: ta.Iterable[dc.Field]) -> None:
        super().__init__()

        self._list = list(fields)

        by_name = {}
        for fld in self._list:
            if fld.name in by_name:
                raise NameError(fld.name)
            by_name[fld.name] = fld
        self._by_name = by_name

    @property
    def all(self) -> ta.Sequence[dc.Field]:
        return self._list

    def __getitem__(self, item: ta.Union[int, slice, str]) -> dc.Field:
        if isinstance(item, (int, slice)):
            return self._list[item]
        elif isinstance(item, str):
            return self._by_name[item]
        else:
            raise TypeError(item)

    def __contains__(self, item: ta.Union[dc.Field, str]) -> bool:
        if isinstance(item, dc.Field):
            return item in self._list
        elif isinstance(item, str):
            return item in self._by_name
        else:
            raise TypeError(item)

    def __len__(self) -> int:
        return len(self._list)

    def __iter__(self) -> ta.Iterable[dc.Field]:
        return iter(self._list)

    @properties.cached
    def by_name(self) -> ta.Mapping[str, dc.Field]:
        return self._by_name

    @properties.cached
    def by_field_type(self) -> ta.Mapping[FieldType, ta.Sequence[dc.Field]]:
        ret = {}
        for f in self:
            ret.setdefault(get_field_type(f), []).append(f)
        return ret

    @properties.cached
    def instance(self) -> ta.Sequence[dc.Field]:
        return self.by_field_type.get(FieldType.INSTANCE, [])
