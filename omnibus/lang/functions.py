import functools
import sys
import typing as ta


T = ta.TypeVar('T')
U = ta.TypeVar('U')


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

    def __init__(self, fn: ta.Callable, offset=1, *, wrap=True) -> None:
        super().__init__()

        self._fn = fn
        self._offset = offset

        if wrap:
            functools.update_wrapper(self, fn)

    def __get__(self, instance, owner=None):
        return type(self)(self._fn.__get__(instance, owner), self._offset)

    def __call__(self, *args, **kwargs):
        try:
            cls_dct = kwargs.pop('cls_dct')
        except KeyError:
            cls_dct = sys._getframe(self._offset).f_locals
        if not is_possibly_cls_dct(cls_dct):
            raise TypeError(cls_dct)
        return self._fn(cls_dct, *args, **kwargs)


def cls_dct_fn(offset=1, *, wrap=True):
    def outer(fn):
        return ClassDctFn(fn, offset, wrap=wrap)
    return outer


def is_lambda(f: ta.Any) -> bool:
    l = lambda: 0
    return isinstance(f, type(l)) and f.__name__ == l.__name__


def maybe_call(obj: ta.Any, att: str, *args, default: ta.Any = None, **kwargs) -> ta.Any:
    try:
        fn = getattr(obj, att)
    except AttributeError:
        return default
    else:
        return fn(*args, **kwargs)


class staticfunction(staticmethod):
    """
    Allows calling @staticmethods within a classbody. Vanilla @staticmethods are not callable:

        TypeError: 'staticmethod' object is not callable
    """

    def __init__(self, fn: ta.Callable) -> None:
        if isinstance(fn, staticmethod):
            fn = fn.__func__  # type: ignore  # noqa
        super().__init__(fn)
        functools.update_wrapper(self, fn)

    def __repr__(self) -> str:
        return f'{type(self).__name__}({self.__func__})'

    def __call__(self, *args, **kwargs):
        return self.__func__(*args, **kwargs)


def unwrap_func(fn: ta.Callable) -> ta.Callable:
    while True:
        if isinstance(fn, (classmethod, staticmethod)):
            fn = fn.__func__  # type: ignore
        elif isinstance(fn, functools.partial):
            fn = fn.func
        else:
            nxt = getattr(fn, '__wrapped__', None)
            if not callable(nxt):
                return fn
            elif nxt is fn:
                raise TypeError(fn)
            fn = nxt


class _CachedNullary(ta.Generic[T]):

    def __init__(
            self,
            fn: ta.Callable[[], T],
            *,
            value: ta.Any = _MISSING,
            value_fn: ta.Optional[ta.Callable[[], T]] = None,
    ) -> None:
        super().__init__()

        self._fn = fn
        self._value = value
        self._value_fn = value_fn if value_fn is not None else fn
        functools.update_wrapper(self, fn)

    def reset(self) -> None:
        self._value = _MISSING

    def __bool__(self) -> bool:
        raise TypeError

    def __call__(self) -> T:
        if self._value is not _MISSING:
            return self._value
        value = self._value = self._value_fn()
        return value


class _CachedNullaryDescriptor(_CachedNullary[T]):

    def __init__(
            self,
            fn: ta.Callable[[], T],
            scope: ta.Any,
            *,
            instance: ta.Any = None,
            owner: ta.Any = None,
            name: ta.Optional[str] = None,
            **kwargs
    ) -> None:
        super().__init__(fn, **kwargs)

        self._scope = scope
        self._instance = instance
        self._owner = owner
        self._name = name if name is not None else unwrap_func(fn).__name__

    def __get__(self, instance, owner=None):
        scope = self._scope
        if owner is self._owner and (instance is self._instance or scope is classmethod):
            return self
        fn = self._fn
        name = self._name
        bound = self.__class__(
            fn,
            scope,
            instance=instance,
            owner=owner,
            value=_MISSING if scope is classmethod else self._value,
            name=name,
            value_fn=fn.__get__(instance, owner),
        )
        if scope is classmethod and owner is not None:
            setattr(owner, name, bound)
        elif instance is not None:
            instance.__dict__[name] = bound
        return bound


def cached_nullary(fn: ta.Callable[[], T]) -> ta.Callable[[], T]:
    if isinstance(fn, staticmethod):
        return _CachedNullary(fn, value_fn=unwrap_func(fn))  # type: ignore
    scope = classmethod if isinstance(fn, classmethod) else None  # type: ignore
    return _CachedNullaryDescriptor(fn, scope)


def raise_(exc: ta.Union[Exception, ta.Type[Exception]]) -> ta.NoReturn:
    raise exc


def try_(
        exc: ta.Union[Exception, ta.Iterable[Exception]] = Exception,
        default: ta.Optional[T] = None,
) -> ta.Callable[..., T]:
    def outer(fn):
        def inner(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except exct:
                return default
        return inner
    exct = (exc,) if isinstance(exc, type) else tuple(exc)
    return outer


def identity(obj: T) -> T:
    return obj


try:
    from .._ext.cy.lang import identity  # type: ignore  # noqa
except ImportError:
    pass


class constant(ta.Generic[T]):  # noqa

    def __init__(self, obj: T) -> None:
        super().__init__()

        self._obj = obj

    def __call__(self) -> T:
        return self._obj


try:
    from .._ext.cy.lang import constant  # type: ignore  # noqa
except ImportError:
    pass


def cmp(l: ta.Any, r: ta.Any) -> int:
    return (l > r) - (l < r)


def recurse(fn: ta.Callable[..., T], *args, **kwargs) -> T:
    def rec(*args, **kwargs):
        return fn(rec, *args, **kwargs)
    return rec(*args, **kwargs)


def optional_of(fn: ta.Callable[[T], U]) -> ta.Callable[[ta.Optional[T]], ta.Optional[U]]:
    @functools.wraps(fn)
    def inner(o):
        if o is None:
            return None
        else:
            return fn(o)
    return inner
