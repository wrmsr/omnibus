"""
TODO:
- codec
"""
import abc
import collections
import collections.abc
import copy
import dataclasses as dc_
import typing as ta
import weakref

from . import check
from . import lang


T = ta.TypeVar('T')


Field = dc_.Field
FrozenInstanceError = dc_.FrozenInstanceError
InitVar = dc_.InitVar
MISSING = dc_.MISSING

fields = dc_.fields
is_dataclass = dc_.is_dataclass
make_dataclass = dc_.make_dataclass
replace = dc_.replace


_ORIGIN = '__dataclass_origin__'


def fields_dict(class_or_instance) -> ta.Dict[str, Field]:
    return {f.name: f for f in fields(class_or_instance)}


def _compose_fields(cls: ta.Type) -> ta.Dict[str, Field]:
    fields = {}

    for b in cls.__mro__[-1:0:-1]:
        base_fields = getattr(b, dc_._FIELDS, None)
        if base_fields:
            for f in base_fields.values():
                fields[f.name] = f

    cls_annotations = cls.__dict__.get('__annotations__', {})

    cls_fields = [dc_._get_field(cls, name, type) for name, type in cls_annotations.items()]
    for f in cls_fields:
        fields[f.name] = f

    return fields


def _check_bases(mro: ta.Sequence[ta.Type], *, frozen=False) -> None:
    any_frozen_base = False
    has_dataclass_bases = False
    for b in mro[-1:0:-1]:
        base_fields = getattr(b, dc_._FIELDS, None)
        if base_fields:
            has_dataclass_bases = True
            if getattr(b, dc_._PARAMS).frozen:
                any_frozen_base = True

    if has_dataclass_bases:
        if any_frozen_base and not frozen:
            raise TypeError('cannot inherit non-frozen dataclass from a frozen one')

        if not any_frozen_base and frozen:
            raise TypeError('cannot inherit frozen dataclass from a non-frozen one')


def _has_default(fld: Field) -> bool:
    return fld.default is not MISSING or fld.default_factory is not MISSING


TypeHints = ta.Mapping[str, ta.Any]

_TYPE_HINTS: ta.MutableMapping[type, TypeHints] = weakref.WeakKeyDictionary()


def _get_mro_type_hints(cls: type) -> TypeHints:
    try:
        return _TYPE_HINTS[cls]
    except KeyError:
        ret = _TYPE_HINTS[cls] = ta.get_type_hints(cls)
        return ret


def asdict(obj, *, dict_factory=dict, shallow=False):
    if not dc_._is_dataclass_instance(obj):
        raise TypeError('asdict() should be called on dataclass instances')
    if shallow:
        return {f.name: getattr(obj, f.name) for f in fields(obj)}
    return _asdict_inner(obj, dict_factory)


def _asdict_inner(obj, dict_factory):
    # https://bugs.python.org/issue35540
    if dc_._is_dataclass_instance(obj):
        result = []
        for f in fields(obj):
            value = _asdict_inner(getattr(obj, f.name), dict_factory)
            result.append((f.name, value))
        return dict_factory(result)
    elif isinstance(obj, tuple) and hasattr(obj, '_fields'):
        return type(obj)(*[_asdict_inner(v, dict_factory) for v in obj])
    elif isinstance(obj, (list, tuple)):
        return type(obj)(_asdict_inner(v, dict_factory) for v in obj)
    elif isinstance(obj, collections.defaultdict):
        return type(obj)(obj.default_factory,
                         ((_asdict_inner(k, dict_factory), _asdict_inner(v, dict_factory)) for k, v in obj.items()))
    elif isinstance(obj, dict):
        return type(obj)((_asdict_inner(k, dict_factory), _asdict_inner(v, dict_factory)) for k, v in obj.items())
    else:
        return copy.deepcopy(obj)


def astuple(obj, *, tuple_factory=tuple):
    if not dc_._is_dataclass_instance(obj):
        raise TypeError("astuple() should be called on dataclass instances")
    return _astuple_inner(obj, tuple_factory)


def _astuple_inner(obj, tuple_factory):
    if dc_._is_dataclass_instance(obj):
        result = []
        for f in fields(obj):
            value = _astuple_inner(getattr(obj, f.name), tuple_factory)
            result.append(value)
        return tuple_factory(result)
    elif isinstance(obj, tuple) and hasattr(obj, '_fields'):
        return type(obj)(*[_astuple_inner(v, tuple_factory) for v in obj])
    elif isinstance(obj, (list, tuple)):
        return type(obj)(_astuple_inner(v, tuple_factory) for v in obj)
    elif isinstance(obj, collections.defaultdict):
        return type(obj)(obj.default_factory,
                         ((_asdict_inner(k, tuple_factory), _asdict_inner(v, tuple_factory)) for k, v in obj.items()))
    elif isinstance(obj, dict):
        return type(obj)((_astuple_inner(k, tuple_factory), _astuple_inner(v, tuple_factory)) for k, v in obj.items())
    else:
        return copy.deepcopy(obj)


class SizeMetadata(lang.Marker):
    pass


class ValidateMetadata(lang.Marker):
    pass


class CoerceMetadata(lang.Marker):
    pass


class DeriveMetadata(lang.Marker):
    pass


def field(
        *,
        default=MISSING,
        default_factory=MISSING,
        init=True,
        repr=True,
        hash=None,
        compare=True,
        metadata=None,
        size=None,
        validate=None,
        coerce=None,
        derive=None,
        **kwargs
) -> dc_.Field:
    if size is not None:
        metadata[SizeMetadata] = size
    if validate is not None:
        metadata[ValidateMetadata] = validate
    if coerce is not None:
        metadata[CoerceMetadata] = coerce
    if derive is not None:
        metadata[DeriveMetadata] = derive

    return dc_.field(
        default=default,
        default_factory=default_factory,
        init=init,
        repr=repr,
        hash=hash,
        compare=compare,
        metadata=metadata,
        **kwargs
    )


def dataclass(
        _cls: ta.Type[T] = None,
        *,
        init=True,
        repr=True,
        eq=True,
        order=False,
        unsafe_hash=None,
        frozen=False,
        reorder=False,
        **kwargs
) -> ta.Type[T]:
    fwd_kwargs = dict(
        init=init,
        repr=repr,
        eq=eq,
        order=order,
        unsafe_hash=unsafe_hash,
        frozen=frozen,
    )

    def wrap(cls):
        def post_process(dcls):
            if not hasattr(dcls, '_fields_by_name'):
                dcls._fields_by_name = {f.name: f for f in fields(dcls)}

            if not hasattr(dcls, '_asdict'):
                def _asdict(self, *args, **kwargs):
                    return asdict(self, *args, **kwargs)
                dcls._asdict = _asdict

            if not hasattr(dcls, '_astuple'):
                def _astuple(self, *args, **kwargs):
                    return astuple(self, *args, **kwargs)
                dcls._astuple = _astuple

            if not hasattr(dcls, '_fields'):
                dcls._fields = tuple(f.name for f in fields(dcls))

            if not hasattr(dcls, '_replace'):
                def _replace(self, **kwargs):
                    return dcls(**{**self._asdict(shallow=True), **kwargs})
                dcls._replace = _replace

            return dcls

        if reorder:
            flds = _compose_fields(cls)
            new_flds = {k: v for d in [False, True] for k, v in flds.items() if _has_default(v) == d}
            if list(flds.keys()) != list(new_flds.keys()):
                _check_bases(cls.__mro__, frozen=frozen)
                anns = {name: fld.type for name, fld in new_flds.items()}
                ns = {'__annotations__': anns, _ORIGIN: cls, **new_flds}
                new_dc = dc_.dataclass(type('_Reordered', (object,), ns), **fwd_kwargs)
                ret = post_process(type(cls.__name__, (new_dc, cls), {}))
                ret.__module__ = cls.__module__
                return ret

        return post_process(
            dc_.dataclass(
                cls,
                init=init,
                repr=repr,
                eq=eq,
                order=order,
                unsafe_hash=unsafe_hash,
                frozen=frozen,
                **kwargs
            )
        )

    if _cls is None:
        return wrap
    return wrap(_cls)


class SimplePickle:

    def __reduce__(self):
        return (Reducer(), (type(self).__module__, type(self).__qualname__, self._asdict(),))


class Reducer:

    def __call__(self, mod, name, dct):
        cur = __import__(mod)
        for part in mod.split('.')[1:]:
            cur = getattr(cur, part)
        for part in name.split('.'):
            cur = getattr(cur, part)
        return cur(**dct)


class _Meta(abc.ABCMeta):

    def __new__(
            mcls,
            name,
            bases,
            namespace,
            *,
            abstract=False,
            final=False,
            sealed=False,
            pickle=False,
            **kwargs
    ):
        check.arg(not (abstract and final))
        namespace = dict(namespace)

        bases = tuple(b for b in bases if b is not Dataclass)
        if final and lang.Final not in bases:
            bases += (lang.Final,)
        if sealed and lang.Sealed not in bases:
            bases += (lang.Sealed,)

        cls = dataclass(lang.super_meta(super(), mcls, name, bases, namespace), **kwargs)

        def _build_init():
            def __init__(self):
                raise NotImplementedError
            return __init__
        rebuild = False

        if abstract and '__init__' not in cls.__abstractmethods__:
            kwargs['init'] = False
            namespace['__init__'] = abc.abstractmethod(_build_init())
            rebuild = True
        elif not abstract and '__init__' in cls.__abstractmethods__:
            bases = (lang.new_type('ConcreteDataclass', (Dataclass,), {'__init__': _build_init()}, init=False),) + bases
            rebuild = True

        if pickle and cls.__reduce__ is object.__reduce__:
            namespace['__reduce__'] = SimplePickle.__reduce__
            rebuild = True

        if rebuild:
            cls = dataclass(lang.super_meta(super(), mcls, name, bases, namespace), **kwargs)
        return cls


class Dataclass(metaclass=_Meta):
    pass


class _VirtualClassMeta(type):

    def __subclasscheck__(cls, subclass):
        return is_dataclass(subclass)

    def __instancecheck__(cls, instance):
        return is_dataclass(instance)


class VirtualClass(metaclass=_VirtualClassMeta):

    def __new__(cls, *args, **kwargs):
        raise TypeError

    def __init_subclass__(cls, **kwargs):
        raise TypeError
