"""
TODO:
 - SingletonEnum? - java-style inner classes are all singletons - could tools understand shared parent inheritance?
 - inheritance>
 - IntEnum/Flag from base
"""
import enum
import typing as ta

from .classes import SimpleMetaDict
from .strings import is_dunder


EnumT = ta.TypeVar('EnumT', bound=enum.Enum)
V = ta.TypeVar('V')


_EnumDict = enum._EnumDict  # type: ignore


def parse_enum(obj: ta.Union[EnumT, str], cls: ta.Type[EnumT]) -> EnumT:
    if isinstance(obj, cls):
        return ta.cast(EnumT, cls)
    elif not isinstance(obj, str) or obj.startswith('__'):
        raise ValueError(f'Illegal {cls!r} name: {obj!r}')
    else:
        return getattr(cls, obj)


class _AutoEnumMeta(enum.EnumMeta):

    class Dict(SimpleMetaDict, _EnumDict):  # type: ignore

        def __init__(self, src: _EnumDict) -> None:  # type: ignore
            super().__init__()
            self.update(src)
            if hasattr(src, '_generate_next_value'):
                self._generate_next_value = src._generate_next_value  # type: ignore

        def __setitem__(self, key, value):
            if value is Ellipsis:
                value = enum.auto()
            return super().__setitem__(key, value)

    def __new__(mcls, name, bases, namespace):
        if 'AutoEnum' not in globals():
            return type.__new__(mcls, name, bases, namespace)
        bases = tuple(b if b is not AutoEnum else enum.Enum for b in bases)
        return super().__new__(mcls, name, bases, namespace)

    @classmethod
    def __prepare__(mcls, cls, bases):
        if 'AutoEnum' not in globals():
            return {}
        bases = tuple(b if b is not AutoEnum else enum.Enum for b in bases)
        return _AutoEnumMeta.Dict(super().__prepare__(cls, bases))


class AutoEnum(metaclass=_AutoEnumMeta):
    pass


class _ValueEnumMeta(type):

    IGNORED_BASES = {
        object,
        ta.Generic,
    }

    ILLEGAL_ATTRS = {
        '_name_value_pairs',
        '_by_name',
        '_by_value',
    }

    class _ByValueDescriptor:

        def __get__(self, instance, owner=None):
            if owner is None:
                return self

            by_value = {}
            for k, v in owner._by_name.items():
                if v in by_value:
                    raise TypeError(f'Duplicate value {v!r} with name {k!r}')
                by_value[v] = k

            owner._by_value = by_value
            return by_value

    def __new__(mcls, name, bases, namespace, *, unique=False, ignore=(), **kwargs):
        if isinstance(ignore, str):
            raise TypeError(ignore)

        cls = super().__new__(mcls, name, bases, namespace, **kwargs)  # noqa

        for k in mcls.ILLEGAL_ATTRS:
            if k in namespace:
                raise NameError(k)

        pairs = []
        by_name = {}
        for mrocls in cls.__mro__:
            if mrocls in mcls.IGNORED_BASES:
                continue
            for k, v in mrocls.__dict__.items():
                if k in mcls.ILLEGAL_ATTRS or k in ignore or is_dunder(k):
                    continue
                pairs.append((k, v))
                if k not in by_name:
                    by_name[k] = v

        cls._name_value_pairs = pairs
        cls._by_name = by_name
        cls._by_value = mcls._ByValueDescriptor()  # noqa

        if unique:
            getattr(cls, '_by_value')

        return cls


class ValueEnum(ta.Generic[V], metaclass=_ValueEnumMeta):

    _name_value_pairs: ta.ClassVar[ta.Sequence[ta.Tuple[str, V]]]
    _by_name: ta.ClassVar[ta.Mapping[str, V]]
    _by_value: ta.ClassVar[ta.Mapping[V, str]]

    def __new__(cls, *args, **kwargs):
        if len(args) == 1 and isinstance(args, str):
            [name] = args
            return cls._by_name[name]
        raise TypeError((args, kwargs))
