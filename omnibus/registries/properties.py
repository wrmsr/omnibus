import typing as ta
import weakref

from .. import check
from .. import lang
from .. import properties
from .composites import CompositeMultiRegistry
from .composites import CompositeRegistry
from .dicts import DictMultiRegistry
from .dicts import DictRegistry
from .types import Registry


K = ta.TypeVar('K')
V = ta.TypeVar('V')


class Property(properties.Property[Registry[K, V]]):

    def __init__(
            self,
            *,
            bind: bool = None,
            lock: lang.DefaultLockable = None,
            policy: CompositeRegistry.Policy = None,
    ) -> None:
        super().__init__()

        if policy is None:
            policy = CompositeRegistry.FIRST_ONE

        self._bind = bind
        self._lock = lang.default_lock(lock, True)
        self._policy = check.callable(policy)

        self._name: str = None
        self._registrations_attr_name = '__%s_%x_registrations' % (type(self).__name__, id(self))

        self._immediate_registries_by_cls: ta.MutableMapping[ta.Type, Registry[K, V]] = weakref.WeakKeyDictionary()  # noqa
        self._registries_by_cls: ta.MutableMapping[ta.Type, Registry[K, V]] = weakref.WeakKeyDictionary()

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

    def _build_immediate_registry(self, items: ta.Iterable[ta.Tuple[K, V]]) -> DictRegistry[K, V]:
        return DictRegistry(items)

    def _get_immediate_registry(self, cls: ta.Type) -> Registry[K, V]:
        try:
            return self._immediate_registries_by_cls[cls]

        except KeyError:
            items = []

            registrations: Property.Registrations
            try:
                registrations = cls.__dict__[self._registrations_attr_name]
            except KeyError:
                pass

            else:
                check.isinstance(registrations, Property.Registrations)
                check.state(not registrations._consumed)

                for value, keys in registrations._key_sets_by_value.items():
                    for key in keys:
                        items.append((key, value))

                registrations._consumed = True

            registry = self._build_immediate_registry(items)
            registry.freeze()

            self._immediate_registries_by_cls[cls] = registry
            return registry

    def _build_composite_registry(self, regs: ta.Iterable[Registry[K, V]]) -> Registry[K, V]:
        return CompositeRegistry(regs, policy=self._policy)

    def get_registry(self, cls: ta.Type) -> Registry[K, V]:
        with self._lock():
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
            self.registering = self._owner.registering

        @property
        def registry(self) -> Registry[K, V]:
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

        def register(self, value, keys):
            raise TypeError

        def registering(self, *keys):
            raise TypeError

    def __get__(self, obj, cls=None) -> Accessor[K, V]:
        if cls is None:
            return self

        accessor = self.Accessor(self, obj, cls)

        if obj is not None and self._name is not None:
            obj.__dict__[check.not_empty(self._name)] = accessor

        return accessor

    def _register(self, cls_dct, value, keys):
        with self._lock():
            registrations: Property.Registrations
            try:
                registrations = cls_dct[self._registrations_attr_name]
            except KeyError:
                registrations = cls_dct[self._registrations_attr_name] = Property.Registrations()

            check.isinstance(registrations, Property.Registrations)
            check.state(not registrations._consumed)

            try:
                key_set = registrations._key_sets_by_value[value]
            except KeyError:
                key_set = registrations._key_sets_by_value[value] = set()

            key_set.update(keys)

    @lang.cls_dct_fn()
    def register(self, cls_dct, value, keys):
        self._register(cls_dct, value, keys)
        return value

    @lang.cls_dct_fn()
    def registering(self, cls_dct, *keys):
        def inner(value):
            self._register(cls_dct, value, keys)
            return value

        return inner


def property_(
        *,
        bind: bool = None,
        lock: lang.DefaultLockable = None,
        policy: CompositeRegistry.Policy = None,
) -> Property:
    return Property(
        bind=bind,
        lock=lock,
        policy=policy,
    )


# FIXME: class MultiProperty(Property[MultiRegistry[K, V]], Property[K, ta.AbstractSet[V]]):
class MultiProperty(Property):

    def __init__(
            self,
            *,
            bind: bool = None,
            lock: lang.DefaultLockable = None,
            policy: CompositeRegistry.Policy = None,
    ) -> None:
        if policy is None:
            policy = CompositeMultiRegistry.MERGE
        super().__init__(bind=bind, lock=lock, policy=policy)

    def _build_immediate_registry(self, items: ta.Iterable[ta.Tuple[K, V]]) -> DictMultiRegistry[K, V]:
        dct = {}
        for k, v in items:
            dct.setdefault(k, set()).add(v)
        return DictMultiRegistry(dct)

    def _build_composite_registry(self, regs: ta.Iterable[Registry[K, V]]) -> Registry[K, V]:
        return CompositeMultiRegistry(regs, policy=self._policy)


def multi_property(
        *,
        bind: bool = None,
        lock: lang.DefaultLockable = None,
        policy: CompositeRegistry.Policy = None,
) -> Property:
    return MultiProperty(
        bind=bind,
        lock=lock,
        policy=policy,
    )