"""
TODO:
 - statics? once, every, and_every, ...
 - io - FileObj protocol
 - cached_unary?
 - s/cached/memoized/?
 - @classmethod with instancemethod override/overload
 - functools.partial but check prototype fits (kwargs, #args)
 - curry
  - functions.py..
 - no_bool class/staticmethod
"""
import collections.abc
import functools
import itertools
import time
import types
import typing as ta
import weakref


T = ta.TypeVar('T')
K = ta.TypeVar('K')
V = ta.TypeVar('V')

BytesLike = ta.Union[bytes, bytearray]


BUILTIN_SCALAR_ITERABLE_TYPES = {
    bytearray,
    bytes,
    str,
}


_MISSING = object()


def register_on(reg, name=None):
    def inner(obj):
        obj_name = name if name is not None else obj.__name__
        if hasattr(reg, obj_name):
            raise NameError(obj_name)
        setattr(reg, obj_name, obj)
        return obj
    return inner


def attr_repr(obj: ta.Any, *attrs: str) -> str:
    return '%s(%s)' % (
        type(obj).__name__,
        ', '.join('%s=%r' % (attr, getattr(obj, attr)) for attr in attrs))


def arg_repr(*args, **kwargs) -> str:
    return ', '.join(*(
        list(map(repr, args)) +
        [f'{k}={repr(v)}' for k, v in kwargs.items()]
    ))


def new_type(
        name: str,
        bases: ta.Sequence[ta.Any],
        namespace: ta.Mapping[str, ta.Any],
        **kwargs
) -> ta.Type:
    return types.new_class(
        name,
        tuple(bases),
        kwds=kwargs,
        exec_body=lambda ns: ns.update(namespace),
    )


def super_meta(
        super_meta: ta.Type,
        meta: ta.Type,
        name: str,
        bases: ta.Sequence[ta.Any],
        namespace: ta.MutableMapping[str, ta.Any],
        **kwargs
) -> ta.Type:
    """Per types.new_class"""
    resolved_bases = types.resolve_bases(bases)
    if resolved_bases is not bases:
        if '__orig_bases__' in namespace:
            raise TypeError((bases, resolved_bases))
        namespace['__orig_bases__'] = bases
    return super_meta.__new__(meta, name, resolved_bases, dict(namespace), **kwargs)  # type: ignore


def is_descriptor(obj: ta.Any) -> bool:
    return (
        hasattr(obj, '__get__') or
        hasattr(obj, '__set__') or
        hasattr(obj, '__delete__')
    )


def unwrap_instance_weakproxy(proxy: weakref.ProxyType, cls: ta.Type[T]) -> T:
    if not isinstance(proxy, weakref.ProxyType):
        raise TypeError(proxy)
    inst = proxy.__repr__.__self__  # type: ignore
    if not isinstance(inst, cls):
        raise TypeError(inst)
    return inst


def exhaust(it: ta.Iterable[ta.Any]) -> None:
    for _ in it:
        pass


class Accessor(ta.Generic[T]):

    def __init__(
            self,
            getter: ta.Callable[[str], T],
            translated_exceptions: ta.Iterable[ta.Type[Exception]] = (),
    ) -> None:
        super().__init__()

        self.__getter = getter
        self.__translated_exceptions = tuple(translated_exceptions)

    def __getitem__(self, name: str) -> T:
        try:
            return self.__getter(name)
        except self.__translated_exceptions:
            raise KeyError(name)

    def __getattr__(self, name: str) -> T:
        try:
            return self.__getter(name)
        except self.__translated_exceptions:
            raise AttributeError(name)

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        else:
            return Accessor(
                self.__getter.__get__(instance, owner),
                self.__translated_exceptions
            )

    @classmethod
    def from_dict(cls, dct: ta.Dict[str, T]) -> 'Accessor[T]':
        return cls(dct.__getitem__, (KeyError,))


def anon_object(name: str) -> ta.Any:
    return new_type(name, (object,), {})()


def dir_dict(
        obj: ta.Any,
        *,
        default=_MISSING,
        public: bool = False,
        filter: ta.Callable[[str], bool] = None,
) -> ta.Dict[str, ta.Any]:
    if filter is None:
        filter = lambda _: True  # noqa
    args = (default,) if default is not _MISSING else ()
    return {a: getattr(obj, a, *args) for a in dir(obj) if filter(a) and not (public and a.startswith('_'))}


class NoBool:

    def __bool__(self) -> bool:
        raise TypeError


class _NoBoolDescriptor:

    def __init__(self, fn, instance=None, owner=None) -> None:
        super().__init__()
        self._fn = fn
        self._instance = instance
        self._owner = owner
        functools.update_wrapper(self, fn)

    def __bool__(self) -> bool:
        raise TypeError

    def __get__(self, instance, owner=None):
        if instance is self._instance and owner is self._owner:
            return self
        return _NoBoolDescriptor(self._fn.__get__(instance, owner), instance, owner)

    def __call__(self, *args, **kwargs):
        return self._fn(*args, **kwargs)


def no_bool(fn):
    return _NoBoolDescriptor(fn)


class VoidException(Exception):
    pass


class Void:

    def __new__(cls, *args, **kwargs):
        raise VoidException

    def __init_subclass__(cls, **kwargs):
        raise VoidException


def void(*args, **kwargs) -> ta.NoReturn:
    raise VoidException


def make_cell(value: ta.Any) -> 'CellType':  # type: ignore
    def fn():
        nonlocal value
    return fn.__closure__[0]  # type: ignore


CellType = type(make_cell(None))


class EmptyMap(ta.Mapping[K, V]):

    INSTANCE: ta.Optional['EmptyMap[K, V]'] = None

    def __init_subclass__(cls, **kwargs):
        raise TypeError

    def __new__(cls, *args, **kwargs):
        if args or kwargs:
            raise TypeError
        return EmptyMap.INSTANCE

    def __repr__(self) -> str:
        return 'EmptyMap()'

    def __init__(self) -> None:
        super().__init__()

    def __getitem__(self, k: K) -> V:
        raise KeyError

    def __len__(self) -> int:
        return 0

    def __iter__(self) -> ta.Iterator[K]:
        return
        yield  # type: ignore


EmptyMap.INSTANCE = object.__new__(EmptyMap)  # type: ignore


def empty_map():
    return EmptyMap.INSTANCE


def is_not_none(obj: T) -> bool:
    return obj is not None


def iterable(obj: T) -> bool:
    return isinstance(obj, collections.abc.Iterable)


def peek(vs: ta.Iterable[T]) -> ta.Tuple[T, ta.Iterator[T]]:
    it = iter(vs)
    v = next(it)
    return v, itertools.chain(iter((v,)), it)


class SimpleProxy(ta.Generic[T]):

    class Descriptor:

        def __init__(self, attr: str) -> None:
            super().__init__()
            self._attr = attr

        def __get__(self, instance, owner=None):
            if instance is None:
                return self
            return getattr(object.__getattribute__(instance, '__wrapped__'), self._attr)

        def __set__(self, instance, value):
            if instance is None:
                return self
            setattr(object.__getattribute__(instance, '__wrapped__'), self._attr)

        def __delete__(self, instance):
            if instance is None:
                return self
            delattr(object.__getattribute__(instance, '__wrapped__'), self._attr)

    __wrapped_attrs__: ta.Iterable[str] = set()

    def __init__(self, wrapped: T) -> None:
        super().__init__()
        object.__setattr__(self, '__wrapped__', wrapped)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        for attr in cls.__wrapped_attrs__:
            setattr(cls, attr, SimpleProxy.Descriptor(attr))

    def __getattr__(self, item):
        return getattr(object.__getattribute__(self, '__wrapped__'), item)

    def __setattr__(self, name, value):
        setattr(object.__getattribute__(self, '__wrapped__'), name, value)

    def __delattr__(self, item):
        delattr(object.__getattribute__(self, '__wrapped__'), item)


class TimeoutException(Exception):
    pass


def ticking_timeout(s: ta.Union[int, float, None]) -> ta.Callable[[], None]:
    if s is None:
        return lambda: None
    def tick():  # noqa
        if time.time() >= deadline:
            raise TimeoutException
    deadline = time.time() + s
    return tick
