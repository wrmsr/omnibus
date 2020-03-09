import abc
import functools
import inspect
import threading
import types
import typing as ta
import weakref

from . import c3
from . import check
from . import lang
from . import properties
from . import reflect as rfl
from . import registries


lang.warn_unstable()


T = ta.TypeVar('T')
R = ta.TypeVar('R')
Impl = ta.TypeVar('Impl')
TypeOrSpec = ta.Union[ta.Type, rfl.Spec]


class NOT_SET(lang.Marker):
    pass


class DispatchError(Exception):
    pass


class AmbiguousDispatchError(DispatchError):
    pass


class UnregisteredDispatchError(DispatchError):
    pass


def generic_issubclass(left: ta.Type, right: ta.Type) -> bool:
    if rfl.is_generic(right):
        right = check.not_none(rfl.erase_generic(right))
    return issubclass(left, right)


def generic_compose_mro(
        cls: T,
        types: ta.Sequence[T] = None,
):
    return c3.compose_mro(
        cls,
        list(types),
        getbases=rfl.generic_bases,
        issubclass=generic_issubclass,
    )


# region Manifests


class Manifest(lang.Final):

    def __init__(
            self,
            _cls: TypeOrSpec,
            _match: TypeOrSpec,
    ) -> None:
        super().__init__()

        self._cls = _cls
        self._match = _match

    @property
    def cls(self) -> TypeOrSpec:
        return self._cls

    @property
    def match(self) -> TypeOrSpec:
        return self._match

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self._cls!r}, {self._match!r})'

    def __iter__(self) -> ta.Iterator[ta.Type]:
        if rfl.is_generic(self._cls):
            return iter(self._cls.__args__)
        else:
            raise TypeError

    def __eq__(self, other):
        return (
            self.__class__ == other.__class__ and
            self._cls == other._type and
            self._match == other._match
        )


def get_manifest_injection_kwargs(impl: ta.Optional[ta.Callable]) -> ta.Optional[ta.Set[str]]:
    if impl is None:
        return None
    try:
        implargspec = inspect.getfullargspec(impl)
    except TypeError:
        return None
    else:
        return {a for a in implargspec.kwonlyargs if implargspec.annotations.get(a) is Manifest}


def inject_manifest(impl: ta.Optional[ta.Callable], manifest: Manifest) -> ta.Callable:
    manifestkw = get_manifest_injection_kwargs(impl)
    if manifestkw:
        impl = functools.partial(impl, **{k: manifest for k in manifestkw})
    return impl


# endregion


# region Dispatchers


class Dispatcher(ta.Generic[Impl]):

    @staticmethod
    def key(obj: ta.Any) -> TypeOrSpec:
        return obj.__class__

    @abc.abstractproperty
    def registry(self) -> registries.Registry[TypeOrSpec, Impl]:
        raise NotImplementedError

    @abc.abstractmethod
    def __setitem__(self, cls: TypeOrSpec, impl: Impl) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def __getitem__(self, key: TypeOrSpec) -> ta.Tuple[ta.Optional[Impl], ta.Optional[Manifest]]:
        raise NotImplementedError

    @abc.abstractmethod
    def __contains__(self, key: TypeOrSpec) -> bool:
        raise NotImplementedError


class ErasingDictDispatcher(Dispatcher[Impl]):

    _dict: ta.Dict[ta.Type, Impl]

    def __init__(self, registry: registries.Registry[ta.Type, Impl] = None) -> None:
        super().__init__()

        if registry is not None:
            self._registry = check.isinstance(registry, registries.Registry)
        else:
            self._registry = registries.DictRegistry()

    def _resolve(self, cls: ta.Type) -> ta.Optional[ta.Tuple[ta.Type, Impl]]:
        mro = generic_compose_mro(cls, list(self._registry.keys()))
        match = None
        for t in mro:
            if match is not None:
                # If *match* is an implicit ABC but there is another unrelated,
                # equally matching implicit ABC, refuse the temptation to guess.
                if (
                        t in self._registry and
                        t not in cls.__mro__ and
                        match not in cls.__mro__ and
                        not issubclass(match, t)
                ):
                    raise AmbiguousDispatchError(match, t)
                break
            if t in self._registry:
                match = t

        try:
            return match, self._registry[match]
        except registries.NotRegisteredException:
            raise UnregisteredDispatchError(match)

    def _erase(self, cls: TypeOrSpec) -> ta.Type:
        return check.isinstance(rfl.erase_generic(cls.erased_cls if isinstance(cls, rfl.TypeSpec) else cls), type)

    def __setitem__(self, cls: TypeOrSpec, impl: Impl) -> None:
        cls = self._erase(cls)
        self._registry[cls] = impl

    def __getitem__(self, cls: TypeOrSpec) -> ta.Tuple[ta.Optional[Impl], ta.Optional[Manifest]]:
        ecls = self._erase(cls)
        try:
            impl = self._registry[ecls]
        except registries.NotRegisteredException:
            match, impl = self._resolve(ecls)
            return impl, Manifest(cls, match)
        else:
            return impl, Manifest(cls, ecls)

    def __contains__(self, cls: TypeOrSpec) -> bool:
        cls = self._erase(cls)
        return cls in self._registry


DefaultDispatcher = ErasingDictDispatcher


# endregion


# region Caching


class CacheGuard(lang.Abstract):

    @abc.abstractmethod
    def update(self, cls: TypeOrSpec) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def maybe_clear(self) -> bool:
        raise NotImplementedError


class AbcCacheGuard(CacheGuard):

    def __init__(self, lock: ta.Any, clear: ta.Callable) -> None:
        super().__init__()

        self._lock = lock
        self._clear = clear

        self._cache_token = abc.get_cache_token()

    def update(self, cls: TypeOrSpec) -> bool:
        if isinstance(cls, type):
            if not hasattr(cls, '__abstractmethods__'):
                return False
        elif isinstance(cls, rfl.Spec):
            if not any(hasattr(t.erased_cls, '__abstractmethods__') for t in cls.all_types):
                return False
        else:
            return False
        self._cache_token = abc.get_cache_token()
        return True

    def maybe_clear(self) -> bool:
        if self._cache_token is not None:
            if self._cache_token != abc.get_cache_token():
                with self._lock:
                    current_token = abc.get_cache_token()
                    if self._cache_token != current_token:
                        self._clear()
                        self._cache_token = current_token
                        return True

        return False


DefaultCacheGuard = AbcCacheGuard


class CachingDispatcher(Dispatcher[Impl]):

    def __init__(
            self,
            child: Dispatcher[Impl],
            guard: CacheGuard = None,
            *,
            lock: lang.ContextManageable = NOT_SET,
    ) -> None:
        super().__init__()

        self._cache = weakref.WeakKeyDictionary()

        if lock is NOT_SET:
            self._lock = threading.RLock()
        elif lock is None:
            self._lock = lang.ContextManaged()
        else:
            self._lock = lock

        self._child = child
        self._guard = guard if guard is not None else DefaultCacheGuard(self._lock, self.clear)

    @property
    def child(self) -> Dispatcher[Impl]:
        return self._child

    @property
    def guard(self) -> CacheGuard:
        return self._guard

    def clear(self) -> None:
        with self._lock:
            self._cache.clear()

    def __setitem__(self, key: TypeOrSpec, value: Impl):
        self._child[key] = value
        self._guard.update(key)
        self.clear()

    def __getitem__(self, key: TypeOrSpec) -> ta.Tuple[ta.Optional[Impl], ta.Optional[Manifest]]:
        self._guard.maybe_clear()
        try:
            impl, manifest = self._cache[key]
        except KeyError:
            with self._lock:
                impl, manifest = self._child[key]
                self._cache[key] = (impl, manifest)
        return impl, manifest

    def __contains__(self, key: TypeOrSpec) -> bool:
        return key in self._child


# endregion


# region function


def function(
        *,
        guard: CacheGuard = None,
        lock: lang.ContextManageable = NOT_SET,
        **kwargs
) -> ta.Callable[[ta.Callable[..., R]], ta.Callable[..., R]]:
    dispatcher = CachingDispatcher(
        DefaultDispatcher(**kwargs),
        guard,
        lock=lock,
    )

    def register(*clss, impl=None):
        if impl is None:
            return lambda _impl: register(*clss, impl=_impl)
        for cls in clss:
            dispatcher[cls] = impl
        return impl

    def wrapper(arg, *args, **kw):
        impl, manifest = dispatcher[dispatcher.key(arg)]
        impl = inject_manifest(impl, manifest)
        return impl(arg, *args, **kw)

    def inner(func):
        functools.update_wrapper(wrapper, func)
        argspec = inspect.getfullargspec(func)
        try:
            wrapper.__annotations__ = {'return': argspec.annotations['return']}
        except KeyError:
            pass

        wrapper.Dispatcher = Dispatcher
        wrapper.register = register
        wrapper.dispatcher = dispatcher
        wrapper.clear_cache = dispatcher.clear

        register(object, impl=func)
        return wrapper

    return inner


# endregion


# region Registry


class RegistryProperty(properties.RegistryProperty):

    def __init__(self) -> None:
        super().__init__(descriptor=True)

        self._dispatcher_cache: ta.MutableMapping[ta.Type, Dispatcher] = weakref.WeakKeyDictionary()

    def get_dispatcher(self, cls: ta.Type) -> Dispatcher:
        try:
            return self._dispatcher_cache[cls]

        except KeyError:
            lookup = self.get_lookup(cls)

            dispatcher = CachingDispatcher(DefaultDispatcher())

            for k, v in lookup.items():
                dispatcher[k] = v

            self._dispatcher_cache[cls] = dispatcher

            return dispatcher

    class DescriptorAccessor(properties.RegistryProperty.DescriptorAccessor):

        def __init__(self, owner, obj, cls):
            super().__init__(owner, obj, cls)

            self._dispatcher = owner.get_dispatcher(cls)
            self._bound_cache: ta.Dict[ta.Any, callable] = {}

        def __call__(self, arg, *args, **kwargs):
            key = self._dispatcher.key(arg)
            try:
                bound = self._bound_cache[key]
            except KeyError:
                impl, manifest = self._dispatcher[key]
                impl = inject_manifest(impl, manifest)
                bound = self._bound_cache[key] = impl.__get__(self._obj, self._cls)

            return bound(arg, *args, **kwargs)

        def dispatch(self, cls: ta.Any) -> ta.Callable:
            return self._dispatcher[cls]

    def register(self, *keys):
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

        return super().register(*keys)

    def invalidate(self):
        super().invalidate()

        self._dispatcher_cache = weakref.WeakKeyDictionary()


def registry_property() -> RegistryProperty:
    return RegistryProperty()


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


# endregion
