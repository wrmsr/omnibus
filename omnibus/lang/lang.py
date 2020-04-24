"""
TODO:
 - statics? once, every, and_every, ...
 - io - FileObj protocol
"""
import functools
import sys
import types
import typing as ta
import weakref


T = ta.TypeVar('T')
K = ta.TypeVar('K')
V = ta.TypeVar('V')

Self = ta.TypeVar('Self')
BytesLike = ta.Union[bytes, bytearray]


BUILTIN_SCALAR_ITERABLE_TYPES = {
    bytearray,
    bytes,
    str,
}


_MISSING = object()


_CLS_DCT_ATTR_SETS = [
    {
        '__module__',
        '__qualname__',
    },
    {
        '__all__',
    },
]


def is_possibly_cls_dct(dct: ta.Mapping[str, ta.Any]) -> bool:
    return any(all(a in dct for a in s) for s in _CLS_DCT_ATTR_SETS)


class ClassDctFn:

    def __init__(self, fn: ta.Callable, offset=1) -> None:
        super().__init__()

        self._fn = fn
        self._offset = offset

        functools.update_wrapper(self, fn)

    def __get__(self, instance, owner):
        return type(self)(self._fn.__get__(instance, owner), self._offset)

    def __call__(self, *args, **kwargs):
        try:
            cls_dct = kwargs.pop('cls_dct')
        except KeyError:
            cls_dct = sys._getframe(self._offset).f_locals
        if not is_possibly_cls_dct(cls_dct):
            raise TypeError(cls_dct)
        return self._fn(cls_dct, *args, **kwargs)


def cls_dct_fn(offset=1):
    def outer(fn):
        return ClassDctFn(fn, offset)
    return outer


@cls_dct_fn()
def public(cls_dct, target, *names: str):
    __all__ = cls_dct.setdefault('__all__', [])
    subtargets = ta.cast(list, target if isinstance(target, tuple) else (target,))
    for subtarget in subtargets:
        subnames = names or (subtarget.__name__,)
        for subname in subnames:
            if subname in cls_dct or subname in __all__:
                raise NameError(subname)
            cls_dct[subname] = target
            __all__.append(subname)
    return target


@cls_dct_fn()
def public_as(cls_dct, *names):
    def inner(target):
        return public(target, *names, cls_dct=cls_dct)
    return inner


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
        namespace: ta.Mapping[str, ta.Any],
        **kwargs
) -> ta.Type:
    """Per types.new_class"""
    resolved_bases = types.resolve_bases(bases)
    if resolved_bases is not bases:
        if '__orig_bases__' in namespace:
            raise TypeError((bases, resolved_bases))
        namespace['__orig_bases__'] = bases
    return super_meta.__new__(meta, name, resolved_bases, namespace, **kwargs)


def is_lambda(f: ta.Any) -> bool:
    l = lambda: 0
    return isinstance(f, type(l)) and f.__name__ == l.__name__


def is_descriptor(obj: ta.Any) -> bool:
    return (
        hasattr(obj, '__get__') or
        hasattr(obj, '__set__') or
        hasattr(obj, '__delete__')
    )


def unwrap_instance_weakproxy(proxy: weakref.ProxyType, cls: ta.Type[T]) -> T:
    if not isinstance(proxy, weakref.ProxyType):
        raise TypeError(proxy)
    inst = proxy.__repr__.__self__
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

    def __get__(self, instance, owner):
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


def maybe_call(obj: ta.Any, att: str, *args, default: ta.Any = None, **kwargs) -> ta.Any:
    try:
        fn = getattr(obj, att)
    except AttributeError:
        return default
    else:
        return fn(*args, **kwargs)


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


def cached_nullary(fn: ta.Callable[[], T]) -> ta.Callable[[], T]:
    value = missing = object()

    @functools.wraps(fn)
    def inner():
        nonlocal value
        if value is missing:
            value = fn()
        return value

    return inner


class VoidException(Exception):
    pass


def void(*args, **kwargs) -> ta.NoReturn:
    raise VoidException


def raise_(exc: ta.Union[Exception, ta.Type[Exception]]) -> ta.NoReturn:
    raise exc


def identity(obj: T) -> T:
    return obj


try:
    from .._ext.cy.lang import identity  # noqa
except ImportError:
    pass


class constant(ta.Generic[T]):

    def __init__(self, obj: T) -> None:
        super().__init__()

        self._obj = obj

    def __call__(self) -> T:
        return self._obj


try:
    from .._ext.cy.lang import constant  # noqa
except ImportError:
    pass


def _get_cell_type() -> type:
    def fn():
        nonlocal value
    value = None  # noqa
    return type(fn.__closure__[0])


CellType = _get_cell_type()


class EmptyMap(ta.Mapping[K, V]):

    INSTANCE: 'EmptyMap[K, V]' = None

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
        yield


EmptyMap.INSTANCE = object.__new__(EmptyMap)


def empty_map():
    return EmptyMap.INSTANCE


def cmp(l: ta.Any, r: ta.Any) -> int:
    return (l > r) - (l < r)
