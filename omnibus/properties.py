"""
TODO:
 - allow_debugger as a lock CM?
"""
import functools
import typing as ta
import weakref

from . import check
from . import lang
from . import pydevd
from . import registries


T = ta.TypeVar('T')
K = ta.TypeVar('K')
V = ta.TypeVar('V')


class CONSUMED(lang.Marker):
    pass


class Property(ta.Generic[T]):
    pass


class CachedProperty(Property[T]):

    def __init__(
            self,
            func: ta.Callable[[ta.Any], T],
            *,
            lock: lang.DefaultLockable = None,
            allow_debugger: bool = False,
    ) -> None:
        super().__init__()

        functools.update_wrapper(self, func)
        self._func = check.callable(func)
        self._lock = lang.default_lock(lock, False)
        self._allow_debugger = bool(allow_debugger)

    def __get__(self, obj, cls) -> T:
        if obj is None:
            return self

        if not self._allow_debugger:
            pydevd.forbid_debugger_call()

        with self._lock:
            try:
                value = obj.__dict__[self._func.__name__]
            except KeyError:
                value = obj.__dict__[self._func.__name__] = self._func(obj)

        return value


def cached(fn: ta.Callable[..., T]) -> T:
    return CachedProperty(fn)


def locked_cached(fn: ta.Callable[..., T]) -> T:
    return CachedProperty(fn, lock=True)


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

    def __init__(
            self,
            func: ta.Callable[[ta.Any], T],
    ) -> None:
        super().__init__()

        functools.update_wrapper(self, func)
        self._func = check.callable(func)

    def __get__(self, obj, cls=None) -> T:
        return self._func(cls)


def class_(fn: ta.Callable[..., T]) -> T:
    return ClassProperty(fn)


class CachedClassProperty(Property[T]):

    def __init__(
            self,
            func: ta.Callable[[ta.Any], T],
            *,
            lock: lang.DefaultLockable = None,
            allow_debugger: bool = False,
    ) -> None:
        super().__init__()

        functools.update_wrapper(self, func)
        self._func = check.callable(func)
        self._lock = lang.default_lock(lock, False)
        self._allow_debugger = bool(allow_debugger)

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

        if not self._allow_debugger:
            pydevd.forbid_debugger_call()

        with self._lock:
            try:
                return self._values[cls]
            except KeyError:
                value = self._values[cls] = self._func(cls)

        return value


def cached_class(fn: ta.Callable[..., T]) -> T:
    return CachedClassProperty(fn)


def locked_cached_class(fn: ta.Callable[..., T]) -> T:
    return CachedClassProperty(fn, lock=True)


class RegistryProperty(Property[registries.Registry[K, V]]):

    def __init__(
            self,
            *,
            bind: bool = None,
            lock: lang.DefaultLockable = None,
            policy: registries.CompositeRegistry.Policy = registries.CompositeRegistry.FIRST_ONE,
    ) -> None:
        super().__init__()

        self._bind = bind
        self._lock = lang.default_lock(lock, True)
        self._policy = check.callable(policy)

        self._name: str = None
        self._registrations_attr_name = '__%s_%x_registrations' % (type(self).__name__, id(self))

        self._immediate_registries_by_cls: ta.MutableMapping[ta.Type, registries.Registry[K, V]] = weakref.WeakKeyDictionary()  # noqa
        self._registries_by_cls: ta.MutableMapping[ta.Type, registries.Registry[K, V]] = weakref.WeakKeyDictionary()

    def __set_name__(self, owner, name):
        if self._name is None:
            self._name = check.not_empty(name)
        else:
            check.state(self._name == name)

    class Registrations:

        def __init__(self) -> None:
            super().__init__()

            self._consumed = False
            self._key_sets_by_value = {}

    def _build_immediate_registry(self, items: ta.Iterable[ta.Tuple[K, V]]) -> registries.DictRegistry[K, V]:
        return registries.DictRegistry(items)

    def _get_immediate_registry(self, cls: ta.Type) -> registries.Registry[K, V]:
        try:
            return self._immediate_registries_by_cls[cls]

        except KeyError:
            items = []

            registrations: RegistryProperty.Registrations
            try:
                registrations = cls.__dict__[self._registrations_attr_name]
            except KeyError:
                pass

            else:
                check.isinstance(registrations, RegistryProperty.Registrations)
                check.state(not registrations._consumed)

                for value, keys in registrations._key_sets_by_value.items():
                    for key in keys:
                        items.append((key, value))

                registrations._consumed = True

            registry = self._build_immediate_registry(items)
            registry.freeze()

            self._immediate_registries_by_cls[cls] = registry
            return registry

    def _build_composite_registry(self, regs: ta.Iterable[registries.Registry[K, V]]) -> registries.Registry[K, V]:
        return registries.CompositeRegistry(regs, policy=self._policy)

    def get_registry(self, cls: ta.Type) -> registries.Registry[K, V]:
        with self._lock:
            try:
                return self._registries_by_cls[cls]

            except KeyError:
                mro_registries = [self._get_immediate_registry(mcls) for mcls in cls.__mro__]

                registry = self._build_composite_registry(mro_registries)

                self._registries_by_cls[cls] = registry
                return registry

    class Accessor(ta.Mapping[K, V]):

        def __init__(self, owner, obj, cls):
            super().__init__()

            self._owner = owner
            self._obj = obj
            self._cls = cls

            self._registry = owner.get_registry(cls)

            self.register = self._owner.register

        @property
        def registry(self) -> registries.Registry[K, V]:
            return self._registry

        def __getitem__(self, key):
            ret = self._registry[key]

            if self._owner._bind:
                ret = ret.__get__(self._obj, self._cls)

            return ret

        def __iter__(self):
            return iter(self._registry)

        def __len__(self):
            return len(self._registry)

        def register(self, *keys):
            raise TypeError

    def __get__(self, obj, cls=None) -> Accessor[K, V]:
        if cls is None:
            return self

        accessor = self.Accessor(self, obj, cls)

        if obj is not None and self._name is not None:
            obj.__dict__[check.not_empty(self._name)] = accessor

        return accessor

    def _register(self, cls_dct, value, keys):
        with self._lock:
            registrations: RegistryProperty.Registrations
            try:
                registrations = cls_dct[self._registrations_attr_name]
            except KeyError:
                registrations = cls_dct[self._registrations_attr_name] = RegistryProperty.Registrations()

            check.isinstance(registrations, RegistryProperty.Registrations)
            check.state(not registrations._consumed)

            try:
                key_set = registrations._key_sets_by_value[value]
            except KeyError:
                key_set = registrations._key_sets_by_value[value] = set()

            key_set.update(keys)

    @lang.cls_dct_fn()
    def register(self, cls_dct, *keys):
        def inner(value):
            self._register(cls_dct, value, keys)
            return value

        return inner


def registry(
        *,
        bind: bool = None,
        lock: lang.DefaultLockable = None,
        policy: registries.CompositeRegistry.Policy = registries.CompositeRegistry.FIRST_ONE,
) -> RegistryProperty:
    return RegistryProperty(
        bind=bind,
        lock=lock,
        policy=policy,
    )


# FIXME: class MultiRegistryProperty(Property[registries.MultiRegistry[K, V]], RegistryProperty[K, ta.AbstractSet[V]]):
class MultiRegistryProperty(RegistryProperty):

    def __init__(
            self,
            *,
            bind: bool = None,
            lock: lang.DefaultLockable = None,
            policy: registries.CompositeRegistry.Policy = registries.CompositeMultiRegistry.MERGE,
    ) -> None:
        super().__init__(bind=bind, lock=lock, policy=policy)

    def _build_immediate_registry(self, items: ta.Iterable[ta.Tuple[K, V]]) -> registries.DictMultiRegistry[K, V]:
        dct = {}
        for k, v in items:
            dct.setdefault(k, set()).add(v)
        return registries.DictMultiRegistry(dct)

    def _build_composite_registry(self, regs: ta.Iterable[registries.Registry[K, V]]) -> registries.Registry[K, V]:
        return registries.CompositeMultiRegistry(regs, policy=self._policy)


def multi_registry(
        *,
        bind: bool = None,
        lock: lang.DefaultLockable = None,
        policy: registries.CompositeRegistry.Policy = registries.CompositeMultiRegistry.MERGE,
) -> RegistryProperty:
    return MultiRegistryProperty(
        bind=bind,
        lock=lock,
        policy=policy,
    )
