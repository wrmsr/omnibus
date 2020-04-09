import functools
import typing as ta
import weakref

from .. import check
from .. import lang
from .. import pydevd
from .base import _global_property
from .base import Property


T = ta.TypeVar('T')


class CachedProperty(Property[T]):

    def __init__(
            self,
            func: ta.Callable[[ta.Any], T],
            *,
            lock: lang.DefaultLockable = None,
            pure: bool = False,
    ) -> None:
        super().__init__()

        functools.update_wrapper(self, func)
        self._func = check.callable(func)
        self._lock = lang.default_lock(lock, False)
        self._pure = bool(pure)

    def __get__(self, obj, cls) -> T:
        if obj is None:
            return self

        if not self._pure:
            pydevd.forbid_debugger_call()

        with self._lock:
            try:
                value = obj.__dict__[self._func.__name__]
            except KeyError:
                value = obj.__dict__[self._func.__name__] = self._func(obj)

        return value


cached = property
locked_cached = property
pure_cached = property


@_global_property
def _cached(fn: ta.Callable[..., T]) -> T:
    return CachedProperty(fn)


@_global_property
def _locked_cached(fn: ta.Callable[..., T]) -> T:
    return CachedProperty(fn, lock=True)


@_global_property
def _pure_cached(fn: ta.Callable[..., T]) -> T:
    return CachedProperty(fn, pure=True)


class CachedClassProperty(Property[T]):

    def __init__(
            self,
            func: ta.Callable[[ta.Any], T],
            *,
            lock: lang.DefaultLockable = None,
            pure: bool = False,
    ) -> None:
        super().__init__()

        functools.update_wrapper(self, func)
        self._func = check.callable(func)
        self._lock = lang.default_lock(lock, False)
        self._pure = bool(pure)

        self._values = weakref.WeakKeyDictionary()

    def clear(self):
        self._values.clear()

    def __get__(self, obj, cls=None) -> T:
        if cls is None:
            return self._func(cls)

        try:
            return self._values[cls]
        except KeyError:
            pass

        if not self._pure:
            pydevd.forbid_debugger_call()

        with self._lock:
            try:
                return self._values[cls]
            except KeyError:
                value = self._values[cls] = self._func(cls)

        return value


cached_class = property
locked_cached_class = property
pure_cached_class = property


@_global_property
def _cached_class(fn: ta.Callable[..., T]) -> T:
    return CachedClassProperty(fn)


@_global_property
def _locked_cached_class(fn: ta.Callable[..., T]) -> T:
    return CachedClassProperty(fn, lock=True)


@_global_property
def _pure_cached_class(fn: ta.Callable[..., T]) -> T:
    return CachedClassProperty(fn, pure=True)
