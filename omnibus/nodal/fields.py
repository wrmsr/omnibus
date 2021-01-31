import collections.abc
import types
import typing as ta

from .. import check
from .. import dataclasses as dc
from .. import reflect as rfl


T = ta.TypeVar('T')
StrMap = ta.Mapping[str, ta.Any]


class FieldInfo(dc.Pure):
    name: str
    spec: rfl.TypeSpec
    opt: bool = False
    seq: bool = False

    @classmethod
    def of(
            cls,
            obj: ta.Union['FieldInfo', dc.Field],
            *,
            type_hints: ta.Optional[StrMap] = None,
    ) -> 'FieldInfo':
        if isinstance(obj, FieldInfo):
            return obj

        elif isinstance(obj, dc.Field):
            if type_hints is not None:
                ty = type_hints[obj.name]
            else:
                ty = obj.type

            fs = rfl.spec(ty)
            opt = False
            seq = False

            if isinstance(fs, rfl.UnionSpec) and fs.optional_arg is not None:
                fs = fs.optional_arg
                opt = True

            if isinstance(fs, rfl.SpecialParameterizedGenericTypeSpec) and fs.erased_cls is collections.abc.Sequence:
                [fs] = fs.args
                seq = True

            return FieldInfo(obj.name, fs, opt, seq)

        else:
            raise TypeError(obj)


class FieldsInfo(dc.Pure):
    flds: ta.Mapping[str, FieldInfo]


def build_nodal_fields(cls: type, root_cls: type) -> FieldsInfo:
    check.arg(isinstance(cls, type) and dc.is_dataclass(cls))
    check.issubclass(cls, root_cls)

    th = ta.get_type_hints(cls)
    flds = {}

    for f in dc.fields(cls):
        fi = FieldInfo.of(f, type_hints=th)

        if isinstance(fi.spec, rfl.TypeSpec) and issubclass(fi.spec.erased_cls, root_cls):
            flds[f.name] = fi

        else:
            def flatten(s):
                yield s
                if isinstance(s, (rfl.UnionSpec, rfl.GenericTypeSpec)):
                    for a in s.args:
                        yield from flatten(a)

            l = list(flatten(fi.spec))
            if any(isinstance(e, rfl.TypeSpec) and issubclass(e.erased_cls, root_cls) for e in l):
                raise TypeError(f'Peer fields must be sequences: {f.name} {fi.spec}')

    return FieldsInfo(flds)


def check_nodal_field_value(v: T, f: FieldInfo) -> T:
    if f.opt and v is None:
        pass

    elif v is None:
        raise TypeError(v, f)

    elif f.seq:
        if isinstance(v, types.GeneratorType):
            raise TypeError(v, f)

        for e in v:
            if not isinstance(e, f.spec.erased_cls):
                raise TypeError(e, f)

    else:
        if not isinstance(v, f.spec.erased_cls):
            raise TypeError(v, f)

    return v


def check_nodal_fields(obj: ta.Any, fi: FieldsInfo) -> None:
    for a, f in fi.flds.items():
        v = getattr(obj, a)
        check_nodal_field_value(v, f)
