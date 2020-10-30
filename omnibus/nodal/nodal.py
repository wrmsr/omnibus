"""
TODO:
 - ** diffing **
 - explicit subclass registration for serde
 - (optional) id + refs
"""
import collections
import operator
import types
import typing as ta

from . import annotations as ans
from .. import check
from .. import collections as col
from .. import dataclasses as dc
from .. import lang
from .. import reflect as rfl
from ..serde import mapping as sm


Self = ta.TypeVar('Self')
NodalT = ta.TypeVar('NodalT', bound='Nodal')
AnnotationT = ta.TypeVar('AnnotationT', bound=ans.Annotation)


class FieldInfo(dc.Pure):
    spec: rfl.TypeSpec
    opt: bool = False
    seq: bool = False


class FieldsInfo(dc.Pure):
    flds: ta.Mapping[str, FieldInfo]


class _NodalMeta(dc.Meta):

    def __new__(mcls, name, bases, namespace, **kwargs):
        if name == 'Nodal' and namespace['__module__'] == __name__:
            return super().__new__(mcls, name, bases, namespace, **kwargs)

        for k in [
            '_ann_cls',
            '_anns_cls',
            'anns',
            'meta',
        ]:
            check.not_in(k, kwargs)
            check.not_in(k, namespace.get('__annotations__', {}))

        nbs = {nb for b in bases for nb in b.__mro__ if Nodal in nb.__bases__}
        if not nbs:
            check.in_(Nodal, bases)
            nos = check.single([
                obs
                for ob in namespace['__orig_bases__']
                for obs in [rfl.spec(ob)]
                if isinstance(obs, rfl.ExplicitParameterizedGenericTypeSpec) and obs.erased_cls is Nodal
            ])

            ann_cls = check.issubclass(nos.cls_args[1], ans.Annotation)
            namespace['_ann_cls'] = ann_cls

            Annotations = lang.new_type(  # noqa
                f'Annotations${name}',
                (ans.Annotations[ann_cls],),
                {},
            )

            namespace['_anns_cls'] = Annotations

            namespace['anns'] = dc.field(
                (),
                kwonly=True,
                repr=False,
                hash=False,
                compare=False,
                coerce=Annotations,
                metadata={sm.Ignore: operator.not_},
            )

            namespace.setdefault('__annotations__', {})['anns'] = Annotations

            namespace['meta'] = dc.field(
                col.frozendict(),
                kwonly=True,
                repr=False,
                hash=False,
                compare=False,
                coerce=lambda d: col.frozendict(
                    (k, v) for k, v in check.isinstance(d, ta.Mapping).items() if v is not None),
                check=lambda d: not any(isinstance(k, ann_cls) or v is None for k, v in d.items()),
                metadata={sm.Ignore: True},
            )

            namespace.setdefault('__annotations__', {})['meta'] = ta.Mapping[ta.Any, ta.Any]

        else:
            nb = check.single(nbs)  # noqa

        cls = super().__new__(mcls, name, bases, namespace, **kwargs)

        if not nbs:
            cls._nodal_cls = cls

        return cls


_COMMON_META_KWARGS = {
    'frozen': True,
    'reorder': True,
}


def _confer_final(att, sub, sup, bases):
    return sub['abstract'] is dc.MISSING or not sub['abstract']


class Nodal(
    dc.Data,
    ta.Generic[NodalT, AnnotationT],
    metaclass=_NodalMeta,
    abstract=True,
    eq=False,
    **_COMMON_META_KWARGS,
    confer={
        'abstract': True,
        **_COMMON_META_KWARGS,
        'confer': {
            **_COMMON_META_KWARGS,
            'final': dc.Conferrer(_confer_final),
            'repr': dc.SUPER,
            'eq': dc.SUPER,
            'allow_setattr': dc.SUPER,
            'aspects': dc.SUPER,
            'confer': dc.SUPER,
        },
    },
):

    anns: ans.Annotations[AnnotationT] = dc.field((), kwonly=True, coerce=lambda o: lang.raise_(TypeError))
    meta: ta.Mapping[ta.Any, ta.Any] = dc.field(col.frozendict(), kwonly=True, coerce=lambda o: lang.raise_(TypeError))

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)

        # Note: Cannot build fields info here as this is happening during class construction.
        check.state(dc.is_dataclass(cls))

    _nodal_cls: ta.ClassVar[ta.Type[NodalT]]

    @classmethod
    def _build_nodal_fields(cls) -> FieldsInfo:
        th = ta.get_type_hints(cls)
        flds = {}

        for f in dc.fields(cls):
            fs = rfl.spec(th[f.name])
            opt = False
            seq = False

            if isinstance(fs, rfl.UnionSpec) and fs.optional_arg is not None:
                fs = fs.optional_arg
                opt = True

            if isinstance(fs, rfl.SpecialParameterizedGenericTypeSpec) and fs.erased_cls is collections.abc.Sequence:
                [fs] = fs.args
                seq = True

            if isinstance(fs, rfl.TypeSpec) and issubclass(fs.erased_cls, cls._nodal_cls):
                flds[f.name] = FieldInfo(fs, opt, seq)

            else:
                def flatten(s):
                    yield s
                    if isinstance(s, (rfl.UnionSpec, rfl.GenericTypeSpec)):
                        for a in s.args:
                            yield from flatten(a)
                l = list(flatten(fs))
                if any(isinstance(e, rfl.TypeSpec) and issubclass(e.erased_cls, cls._nodal_cls) for e in l):
                    raise TypeError(f'Peer fields must be sequences: {f.name} {fs}')

        return FieldsInfo(flds)

    def __post_init__(self) -> None:
        cls = type(self)
        try:
            fi = cls.__dict__['_nodal_fields']
        except KeyError:
            fi = cls._build_nodal_fields()
            setattr(cls, '_nodal_fields', fi)

        for a, f in fi.flds.items():
            v = getattr(self, a)

            if f.opt and v is None:
                continue
            elif v is None:
                raise TypeError(v, f, a)

            if f.seq:
                if isinstance(v, types.GeneratorType):
                    raise TypeError(v, f, a)
                for e in v:
                    if not isinstance(e, f.spec.erased_cls):
                        raise TypeError(e, f, a)

            else:
                if not isinstance(v, f.spec.erased_cls):
                    raise TypeError(v, f, a)

        try:
            sup = super().__post_init__
        except AttributeError:
            pass
        else:
            sup()

    def yield_field_children(self, fld: ta.Union[dc.Field, str]) -> ta.Iterator[NodalT]:
        if isinstance(fld, dc.Field):
            val = getattr(self, fld.name)
        elif isinstance(fld, str):
            val = getattr(self, fld)
        else:
            raise TypeError(fld)

        if isinstance(val, self._nodal_cls):
            yield val
        elif isinstance(val, collections.abc.Sequence) and not isinstance(val, str):
            yield from (item for item in val if isinstance(item, self._nodal_cls))

    @property
    def children(self) -> ta.Generator[NodalT, None, None]:
        for fld in dc.fields(self):
            yield from self.yield_field_children(fld)

    def build_field_map_kwargs(
            self,
            fn: ta.Callable[[NodalT], NodalT], fld: ta.Union[dc.Field, str],
    ) -> ta.Mapping[str, ta.Any]:
        if isinstance(fld, dc.Field):
            val = getattr(self, fld.name)
        elif isinstance(fld, str):
            val = getattr(self, fld)
        else:
            raise TypeError(fld)

        if isinstance(val, self._nodal_cls):
            return {fld.name: fn(val)}
        elif isinstance(val, collections.abc.Sequence) and not isinstance(val, str):
            return {fld.name: tuple([fn(item) if isinstance(item, self._nodal_cls) else item for item in val])}
        else:
            return {}

    def map(self: Self, fn: ta.Callable[[NodalT], ta.Mapping[str, ta.Any]], **kwargs) -> Self:
        rpl_kw = {**kwargs}
        for fld in dc.fields(self):
            if fld.name in kwargs:
                continue
            for k, v in self.build_field_map_kwargs(fn, fld).items():
                if k in rpl_kw:
                    raise KeyError(k)
                rpl_kw[k] = v
        return dc.replace(self, **rpl_kw)

    def fmap(self: Self, fn: ta.Callable[[NodalT], ta.Mapping[str, ta.Any]]) -> Self:
        return self.map(fn, **fn(self))


def meta_chain(
        obj: Nodal,
        key: ta.Any,
        *,
        cls: ta.Type[Nodal] = Nodal,
        next: ta.Callable[[ta.Any], Nodal] = lambda o: o,
) -> ta.List[Nodal]:
    lst = []
    while True:
        lst.append(check.isinstance(obj, cls))
        try:
            val = obj.meta[key]
        except KeyError:
            break
        obj = next(val)
    return lst
