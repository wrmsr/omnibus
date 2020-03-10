import abc
import collections.abc
import functools
import threading
import typing as ta
import weakref

from . import c3
from . import check
from . import lang
from . import registries


T = ta.TypeVar('T')
K = ta.TypeVar('K')
V = ta.TypeVar('V')


class Property(ta.Generic[T]):
    pass


class CachedProperty(Property[T]):

    def __init__(
            self,
            func: ta.Callable[[ta.Any], T],
            *,
            lock: lang.ContextManageable = lang.ContextManaged(),
    ) -> None:
        super().__init__()

        functools.update_wrapper(self, func)
        self._func = func
        self._lock = lock

        name = func.__name__

        def __get__(obj, cls) -> T:
            if obj is None:
                return self

            value = obj.__dict__[name] = func(obj)
            return value

        self.__get__ = __get__

    def __get__(self, obj, cls) -> T:
        if obj is None:
            return self

        with self._lock:
            try:
                value = obj.__dict__[self._func.__name__]
            except KeyError:
                value = obj.__dict__[self._func.__name__] = self._func(obj)

        return value


def cached(fn: ta.Callable[..., T]) -> T:
    return CachedProperty(fn)


def locked_cached(fn: ta.Callable[..., T]) -> T:
    return CachedProperty(fn, lock=threading.RLock())


class ValueNotSetException(ValueError):
    pass


class ValueAlreadySetException(ValueError):
    pass


class SetOnceProperty(Property[T]):

    def __init__(self, attr_name: str = None) -> None:
        super().__init__()

        self._attr_name = attr_name or '__%s_%x_value' % (type(self).__name__, id(self))

    def __get__(self, instance, owner):
        if instance is None:
            return self
        try:
            return getattr(instance, self._attr_name)
        except AttributeError:
            raise ValueNotSetException

    def __set__(self, instance, value):
        try:
            getattr(instance, self._attr_name)
        except AttributeError:
            setattr(instance, self._attr_name, value)
        else:
            raise ValueAlreadySetException

    def __delete__(self, instance):
        raise TypeError('Operation not supported')


set_once = SetOnceProperty


class ClassProperty(Property[T]):

    def __init__(self, func: ta.Callable[[ta.Any], T]) -> None:
        super().__init__()

        self._func = func

    def __get__(self, obj, cls=None) -> T:
        return self._func(cls)


def class_(fn: ta.Callable[..., T]) -> T:
    return ClassProperty(fn)


class CachedClassProperty(Property[T]):

    def __init__(self, func: ta.Callable[[ta.Any], T]) -> None:
        super().__init__()

        self._func = func
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

        value = self._values[cls] = self._func(cls)
        return value


def cached_class(fn: ta.Callable[..., T]) -> T:
    return CachedClassProperty(fn)


class RegistryProperty(Property[registries.Registry[K, V]]):

    def __init__(
            self,
            *,
            descriptor: bool = None,
            raw: bool = False,
    ) -> None:
        super().__init__()

        self._descriptor = descriptor
        self._raw = raw

        self._name: str = None

        self._key_sets_by_value: ta.MutableMapping[V, ta.AbstractSet[K]] = weakref.WeakKeyDictionary()

        self._immediate_registries_by_cls: ta.MutableMapping[ta.Type, registries.Registry[K, V]] = weakref.WeakKeyDictionary()  # noqa
        self._registries_by_cls: ta.MutableMapping[ta.Type, registries.Registry[K, V]] = weakref.WeakKeyDictionary()

    def __set_name__(self, owner, name):
        if self._name is None:
            self._name = check.not_empty(name)
        else:
            check.state(self._name == name)

    def _get_immediate_registry(self, cls: ta.Type) -> registries.Registry[K, V]:
        try:
            return self._immediate_registries_by_cls[cls]

        except KeyError:
            registry = registries.DictRegistry()

            for att in cls.__dict__.values():
                try:
                    keys = self._key_sets_by_value[att]
                except KeyError:
                    continue
                else:
                    for key in keys:
                        registry[key] = att

            registry.freeze()
            self._immediate_registries_by_cls = registry
            return registry

    def get_registry(self, cls: ta.Type) -> registries.Registry[K, V]:
        try:
            return self._registries_by_cls[cls]

        except KeyError:
            mro_registries = [self._get_immediate_registry(mcls) for mcls in reversed(cls.__mro__)]

            registry = registries.CompositeRegistry(mro_registries)

            self._registries_by_cls[cls] = registry

            return registry

    class DescriptorAccessor(collections.abc.Mapping):

        def __init__(self, owner, obj, cls):
            super().__init__()

            self._owner = owner
            self._obj = obj
            self._cls = cls

            self._lookup = owner.get_lookup(cls)

        def __getitem__(self, key):
            ret = self._lookup[key]

            if self._owner._descriptor:
                ret = ret.__get__(self._obj, self._cls)

            return ret

        def __iter__(self):
            return iter(self._lookup)

        def __len__(self):
            return len(self._lookup)

        def register(self, *keys):
            return self._owner.register(*keys)

        def invalidate(self):
            return self._owner.invalidate()

    def __get__(self, obj, cls=None):
        if cls is None:
            return self

        if not self._raw:
            ret = self.DescriptorAccessor(self, obj, cls)
        else:
            ret = self.get_lookup(cls)

        if obj is not None and self._name is not None:
            obj.__dict__[check.not_empty(self._name)] = ret

        return ret

    def register(self, *keys):
        def inner(meth):
            self._registry[meth] = keys
            return meth

        return inner

    def invalidate(self):
        self._lookup_cache = weakref.WeakKeyDictionary()


def registry(
        *,
        descriptor: bool = None,
        raw: bool = False,
) -> RegistryProperty:
    return RegistryProperty(
        descriptor=descriptor,
        raw=raw,
    )
