import functools
import typing as ta

from .. import lang
from .. import pydevd
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
        self._func = self._unwrap(func)
        self._lock = lang.default_lock(lock, False)
        self._pure = bool(pure)

        self._name: ta.Optional[str] = None

    def __set_name__(self, owner, name):
        if self._name is None:
            self._name = name
        elif name != self._name:
            raise TypeError(f'Cannot assign the two different names ({self._name!r} and {name!r}).')

    def __get__(self, instance, cls=None) -> T:
        if instance is None:
            return self

        if not self._pure:
            pydevd.forbid_debugger_call()

        if self._name is None:
            raise TypeError('Need name assigned')

        with self._lock():
            try:
                value = instance.__dict__[self._name]
            except KeyError:
                value = instance.__dict__[self._name] = self._func(instance)

        return value


def cached(fn: ta.Callable[..., T]) -> T:
    return CachedProperty(fn)


def locked_cached(fn: ta.Callable[..., T]) -> T:
    return CachedProperty(fn, lock=True)


def pure_cached(fn: ta.Callable[..., T]) -> T:
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
        self._func = self._unwrap(func)
        self._lock = lang.default_lock(lock, False)
        self._pure = bool(pure)
        self._name: ta.Optional[str] = None

    def __set_name__(self, owner, name):
        if self._name is None:
            self._name = name
        elif name != self._name:
            raise TypeError(f'Cannot assign the two different names ({self._name!r} and {name!r}).')

    class Bound:

        def __init__(self, owner: 'CachedClassProperty[T]', cls: type, value: T) -> None:
            super().__init__()

            functools.update_wrapper(self, owner._func)
            self._cls = cls
            self._value = value
            self._delegate = owner.__get__

        def __get__(self, obj, cls=None) -> T:
            if cls is self._cls:
                return self._value
            else:
                return self._delegate(obj, cls)

    def __get__(self, obj, cls=None) -> T:
        if cls is None:
            return self._func(cls)

        if not self._pure:
            pydevd.forbid_debugger_call()

        with self._lock():
            try:
                bound = cls.__dict__[self._name]
            except KeyError:
                bound = None
            if bound is None or bound is self:
                bound = self.Bound(self, cls, self._func(cls))
                setattr(cls, self._name, bound)

        return bound._value


def cached_class(fn: ta.Callable[..., T]) -> T:
    return CachedClassProperty(fn)


def locked_cached_class(fn: ta.Callable[..., T]) -> T:
    return CachedClassProperty(fn, lock=True)


def pure_cached_class(fn: ta.Callable[..., T]) -> T:
    return CachedClassProperty(fn, pure=True)
