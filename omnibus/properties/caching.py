"""
TODO:
 - properties.init? eager cached, ~ideally~ automatically on __init__
  - not really possible without explicit help/call or baseclass
"""
import abc
import functools
import typing as ta

from .. import check
from .. import lang
from .. import pydevd
from .base import Property


T = ta.TypeVar('T')


class _GetterProperty(Property[T], lang.Abstract):

    def __new__(
            cls,
            func: ta.Callable[[ta.Any], T],
            *args,
            lock: lang.DefaultLockable = None,
            stateful: bool = False,
            **kwargs
    ):
        func = cls._unwrap(func)
        lock = lang.default_lock(lock, False)
        stateful = bool(stateful)

        __get__ = cls._build_getter(
            func,
            *args,
            lock=lock,
            stateful=stateful,
            **kwargs
        )

        bcls = type(
            cls.__name__,
            (cls,),
            {
                '__get__': __get__,
                '__new__': super().__new__,
            },
        )

        return bcls(
            func,
            *args,
            lock=lock,
            stateful=stateful,
            **kwargs
        )

    def __init__(
            self,
            func: ta.Callable[[ta.Any], T],
            *,
            lock: lang.DefaultLockable = None,
            stateful: bool = False,
    ) -> None:
        super().__init__()

        functools.update_wrapper(self, func)
        self._func = func
        self._lock = lock
        self._stateful = stateful

        self._name: ta.Optional[str] = None

    def __set_name__(self, owner, name):
        if self._name is None:
            self._name = name
        elif name != self._name:
            raise TypeError(f'Cannot assign the two different names ({self._name!r} and {name!r}).')

    @abc.abstractclassmethod
    def _build_getter(
            cls,
            func: ta.Callable[[ta.Any], T],
            *args,
            lock: lang.DefaultLockable = None,
            stateful: bool = False,
            **kwargs
    ) -> ta.Callable[[object, object], T]:
        raise NotImplementedError


class CachedProperty(_GetterProperty[T]):

    @classmethod
    def _build_getter(
            cls,
            func: ta.Callable[[ta.Any], T],
            *,
            lock: lang.DefaultLockable = None,
            stateful: bool = False,
    ) -> ta.Callable[[object, object], T]:
        def __get__(self, instance, owner=None) -> T:
            if instance is None:
                return self

            if stateful:
                pydevd.forbid_debugger_call()

            if self._name is None:
                raise TypeError('Need name assigned')

            with lock():
                try:
                    value = instance.__dict__[self._name]
                except KeyError:
                    value = instance.__dict__[self._name] = func(instance)

            return value

        return __get__


def cached(fn: ta.Callable[..., T]) -> T:
    return CachedProperty(fn)


def locked_cached(fn: ta.Callable[..., T]) -> T:
    return CachedProperty(fn, lock=True)


def stateful_cached(fn: ta.Callable[..., T]) -> T:
    return CachedProperty(fn, stateful=True)


class CachedClassProperty(Property[T]):

    def __init__(
            self,
            func: ta.Callable[[ta.Any], T],
            *,
            lock: lang.DefaultLockable = None,
            stateful: bool = False,
    ) -> None:
        super().__init__()

        functools.update_wrapper(self, func)
        self._func = self._unwrap(func)
        self._lock = lang.default_lock(lock, False)
        self._stateful = bool(stateful)
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

        if self._stateful:
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


def stateful_cached_class(fn: ta.Callable[..., T]) -> T:
    return CachedClassProperty(fn, stateful=True)
