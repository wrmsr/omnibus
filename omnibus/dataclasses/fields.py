import dataclasses as dc
import types
import typing as ta

from .. import properties
from .internals import FieldType
from .internals import get_field_type


class Fields(ta.Sequence[dc.Field]):

    def __init__(self, fields: ta.Iterable[dc.Field]) -> None:
        super().__init__()

        self._seq = tuple(fields)

        by_name = {}
        for fld in self._seq:
            if fld.name in by_name:
                raise NameError(fld.name)
            by_name[fld.name] = fld
        self._by_name = types.MappingProxyType(by_name)

    @property
    def all(self) -> ta.Sequence[dc.Field]:
        return self._seq

    def __getitem__(self, item: ta.Union[int, slice, str]) -> dc.Field:
        if isinstance(item, (int, slice)):
            return self._seq[item]
        elif isinstance(item, str):
            return self._by_name[item]
        else:
            raise TypeError(item)

    def __contains__(self, item: ta.Union[dc.Field, str]) -> bool:
        if isinstance(item, dc.Field):
            return item in self._seq
        elif isinstance(item, str):
            return item in self._by_name
        else:
            raise TypeError(item)

    def __len__(self) -> int:
        return len(self._seq)

    def __iter__(self) -> ta.Iterable[dc.Field]:
        return iter(self._seq)

    @properties.cached
    def by_name(self) -> ta.Mapping[str, dc.Field]:
        return self._by_name

    @properties.cached
    def by_field_type(self) -> ta.Mapping[FieldType, ta.Sequence[dc.Field]]:
        ret = {}
        for f in self:
            ret.setdefault(get_field_type(f), []).append(f)
        return types.MappingProxyType({k: list(v) for k, v in ret.items()})

    @properties.cached
    def instance(self) -> ta.Sequence[dc.Field]:
        return self.by_field_type.get(FieldType.INSTANCE, ())

    @properties.cached
    def init(self) -> ta.List[dc.Field]:
        return [f for f in self if get_field_type(f) in (FieldType.INSTANCE, FieldType.INIT)]
