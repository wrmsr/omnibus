import abc
import collections.abc
import functools
import types
import typing as ta
import weakref

from . import c3


T = ta.TypeVar('T')
K = ta.TypeVar('K')
V = ta.TypeVar('V')


class Property(ta.Generic[T]):
    pass


class CachedProperty(Property[T]):

    def __init__(self, func: ta.Callable[[ta.Any], T]) -> None:
        super().__init__()

        functools.update_wrapper(self, func)
        self._func = func

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
        value = obj.__dict__[self._func.__name__] = self._func(obj)
        return value


def cached(fn: ta.Callable[..., T]) -> T:
    return CachedProperty(fn)


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
            singledispatch: bool = False,
            unbound: bool = False,
    ) -> None:
        super().__init__()

        if unbound and singledispatch:
            raise TypeError
        if singledispatch:
            if descriptor is not None and descriptor is not True:
                raise ValueError(descriptor)
            self._descriptor = self._singledispatch = True
        else:
            self._descriptor = descriptor
            self._singledispatch = False
        self._unbound = unbound
        self._registry: ta.MutableMapping[ta.Callable, ta.Set[ta.Any]] = {}
        self._cache: ta.MutableMapping[ta.Type, ta.Mapping[ta.Any, ta.Callable]] = weakref.WeakKeyDictionary()

    @property
    def singledispatch(self) -> bool:
        return self._singledispatch

    class DescriptorAccessor(collections.abc.Mapping):

        def __init__(self, owner, lookup, obj, cls):
            super().__init__()

            self._owner = owner
            self._lookup = lookup
            self._obj = obj
            self._cls = cls

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

        @cached
        def _singledispatch(self):
            if not self._owner._singledispatch:
                raise TypeError(self._owner)

            def default(arg, *args, **kwargs):
                raise TypeError(arg)
            sd = functools.singledispatch(default)
            for k, v in self.items():
                sd.register(k)(v.__get__(self._obj, self._cls))
            return sd

        def __call__(self, *args, **kwargs):
            return self._singledispatch(*args, **kwargs)

        def dispatch(self, cls: ta.Any) -> ta.Callable:
            return self._singledispatch.dispatch(cls)

    def __get__(self, obj, cls=None):
        if cls is None:
            return self
        try:
            lookup = self._cache[cls]
        except KeyError:
            lookup = {}
            for mcls in reversed(cls.__mro__):
                for att in mcls.__dict__.values():
                    try:
                        keys = self._registry[att]
                    except KeyError:
                        continue
                    for key in keys:
                        lookup[key] = att
            self._cache[cls] = lookup
        if not self._unbound:
            return self.DescriptorAccessor(self, lookup, obj, cls)
        else:
            return lookup

    def register(self, *keys):
        if self._singledispatch:
            if len(keys) == 1 and not isinstance(keys[0], type):
                [meth] = keys
                if not isinstance(meth, types.FunctionType):
                    raise TypeError(meth)
                ann = getattr(meth, '__annotations__', {})
                if not ann:
                    raise TypeError
                _, key = next(iter(ta.get_type_hints(meth).items()))
                if not isinstance(key, type):
                    raise TypeError(key)
                self._registry.setdefault(meth, set()).add(key)
                return meth
            else:
                for key in keys:
                    if not isinstance(key, type):
                        raise TypeError(key)

        def inner(meth):
            self._registry.setdefault(meth, set()).update(keys)
            return meth
        return inner

    def invalidate(self):
        self._cache = weakref.WeakKeyDictionary()


def registry(
        *,
        descriptor: bool = None,
        singledispatch: bool = False,
        unbound: bool = False,
) -> RegistryProperty:
    return RegistryProperty(
        descriptor=descriptor,
        singledispatch=singledispatch,
        unbound=unbound,
    )


class RegistryMeta(abc.ABCMeta):

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
                if not callable(value) or not reg.singledispatch:
                    raise TypeError(value)
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


class RegistryClass(metaclass=RegistryMeta):
    pass
