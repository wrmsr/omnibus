import dataclasses as dc
import typing as ta

from .. import properties
from .internals import FIELDS
from .internals import FieldType
from .internals import get_field
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


def build_cls_fields(cls: type, *, install: bool = False) -> Fields:
    fields = {}
    dc_mro = [b for b in reversed(cls.__mro__) if getattr(b, FIELDS, None)]
    for b in dc_mro:
        base_fields = getattr(b, FIELDS, None)
        if base_fields:
            for f in base_fields.values():
                fields[f.name] = f

    # Annotations that are defined in this class (not in base classes).  If __annotations__ isn't present, then this
    # class adds no new annotations.  We use this to compute fields that are added by this class.
    #
    # Fields are found from cls_annotations, which is guaranteed to be ordered.  Default values are from class
    # attributes, if a field has a default.  If the default value is a Field(), then it contains additional info
    # beyond (and possibly including) the actual default value.  Pseudo-fields ClassVars and InitVars are included,
    # despite the fact that they're not real fields.  That's dealt with later.
    cls_annotations = cls.__dict__.get('__annotations__', {})

    # Now find fields in our class.  While doing so, validate some things, and set the default values (as class
    # attributes) where we can.
    cls_fields = [get_field(cls, name, type) for name, type in cls_annotations.items()]
    for f in cls_fields:
        fields[f.name] = f

        if install:
            # If the class attribute (which is the default value for this field) exists and is of type 'Field', replace
            # it with the real default.  This is so that normal class introspection sees a real default value, not a
            # Field.
            if isinstance(getattr(cls, f.name, None), dc.Field):
                if f.default is dc.MISSING:
                    # If there's no default, delete the class attribute. This happens if we specify field(repr=False),
                    # for example (that is, we specified a field object, but no default value).  Also if we're using a
                    # default factory.  The class attribute should not be set at all in the post-processed class.
                    delattr(cls, f.name)
                else:
                    setattr(cls, f.name, f.default)

    # Do we have any Field members that don't also have annotations?
    for name, value in cls.__dict__.items():
        if isinstance(value, dc.Field) and name not in cls_annotations:
            raise TypeError(f'{name!r} is a field but has no type annotation')

    if install:
        setattr(cls, FIELDS, dict(fields))

    return Fields(fields.values())