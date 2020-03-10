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


class RegistryProperty(Property[ta.Callable]):

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
        self._registry: registries.MultiRegistry[ta.Callable, ta.Any] = registries.MultiDictRegistry()
        self._lookup_cache: ta.MutableMapping[ta.Type, ta.Mapping[ta.Any, ta.Callable]] = weakref.WeakKeyDictionary()

    def __set_name__(self, owner, name):
        if self._name is None:
            self._name = check.not_empty(name)
        else:
            check.state(self._name == name)

    def get_lookup(self, cls: ta.Type) -> ta.Mapping[ta.Any, ta.Callable]:
        try:
            return self._lookup_cache[cls]

        except KeyError:
            lookup = {}

            for mcls in reversed(cls.__mro__):
                for att in mcls.__dict__.values():
                    # FIXME: $ invert
                    # FIXME: o shit lol, don't have class ref and THIS IS GLOBAL FOR PROP (SINGLETON FOR ALL SUBCLASSES)
                    # FIX: type -> frozenset, put meta back here, meta defers
                    #  alt fix: MultiRegistry? ew..?
                    try:
                        keys = self._registry[att]
                    except registries.NotRegisteredException:
                        continue

                    for key in keys:
                        lookup[key] = att

            self._lookup_cache[cls] = lookup

            return lookup

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


"""
class _RegistryClassMeta(abc.ABCMeta):

    class RegisteringNamespace:

        def __init__(self, regs: ta.Mapping[str, RegistryProperty]) -> None:
            super().__init__()
            self._dict = {}
            self._regs = dict(regs)

        def __contains__(self, item):
            return item in self._dict

        def __getitem__(self, item):
            return self._dict[item]

        def __setitem__(self, key, value):
            try:
                reg = self._regs[key]

            except KeyError:
                self._dict[key] = value
                if isinstance(value, RegistryProperty):
                    self._regs[key] = value

            else:
                reg.register(value)
                self._dict[f'__{hex(id(value))}'] = value

        def __delitem__(self, key):
            del self._dict[key]

        def get(self, k, d=None):
            try:
                return self[k]
            except KeyError:
                return d

        def setdefault(self, k, d=None):
            try:
                return self[k]
            except KeyError:
                self[k] = d
                return d

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        regs = {}
        mro = c3.merge([list(b.__mro__) for b in bases])
        for bmro in reversed(mro):
            for k, v in bmro.__dict__.items():
                if isinstance(v, RegistryProperty):
                    regs[k] = v

        return cls.RegisteringNamespace(regs)

    def __new__(mcls, name, bases, namespace, **kwargs):
        if not isinstance(namespace, mcls.RegisteringNamespace):
            raise TypeError(namespace)

        namespace = namespace._dict
        return super().__new__(mcls, name, bases, namespace, **kwargs)


class RegistryClass(metaclass=_RegistryClassMeta):
    pass
"""
