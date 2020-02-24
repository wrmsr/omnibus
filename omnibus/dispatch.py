import abc
import functools
import inspect
import threading
import typing as ta
import weakref

from . import c3
from . import check
from . import lang
from . import reflect as rfl


T = ta.TypeVar('T')
R = ta.TypeVar('R')
Impl = ta.TypeVar('Impl')
TypeOrSpec = ta.Union[ta.Type, rfl.Spec]
TypeVars = ta.Mapping[ta.Any, TypeOrSpec]


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


class Dispatcher(ta.Generic[Impl]):

    @staticmethod
    def key(obj: ta.Any) -> TypeOrSpec:
        return obj.__class__

    @abc.abstractmethod
    def __setitem__(self, key: TypeOrSpec, value: Impl):
        raise NotImplementedError

    @abc.abstractmethod
    def __getitem__(self, key: TypeOrSpec) -> ta.Tuple[ta.Optional[Impl], ta.Optional[Manifest]]:
        raise NotImplementedError

    @abc.abstractmethod
    def __contains__(self, key: TypeOrSpec) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def items(self) -> ta.Iterable[ta.Tuple[TypeOrSpec, Impl]]:
        raise NotImplementedError


class CompositeDispatcher(Dispatcher[Impl]):

    class Mode(lang.AutoEnum):
        FIRST = ...
        ONE = ...

    def __init__(
            self,
            children: ta.Iterable[Dispatcher[Impl]],
            *,
            mode: ta.Union[Mode, str] = Mode.ONE,
    ) -> None:
        super().__init__()

        self._children = list(children)
        self._mode = lang.parse_enum(mode, CompositeDispatcher.Mode)

    @property
    def children(self) -> ta.List[Dispatcher[Impl]]:
        return self._children

    @property
    def mode(self) -> 'CompositeDispatcher.Mode':
        return self._mode

    def __setitem__(self, key: TypeOrSpec, value: Impl):
        raise TypeError

    def __getitem__(self, key: TypeOrSpec) -> ta.Tuple[ta.Optional[Impl], ta.Optional[Manifest]]:
        hits = []
        for child in self._children:
            try:
                hit = child[key]
            except AmbiguousDispatchError:
                raise
            if self._mode == CompositeDispatcher.Mode.FIRST:
                return hit
            hits.append(hit)
        if len(hits) == 1:
            return hits[0]
        elif hits:
            raise AmbiguousDispatchError(key, hits)
        else:
            raise UnregisteredDispatchError(key)

    def __contains__(self, key: TypeOrSpec) -> bool:
        return any(key in c for c in self._children)

    def items(self) -> ta.Iterable[ta.Tuple[TypeOrSpec, Impl]]:
        for child in self._children:
            yield from child.items()


class ErasingDictDispatcher(Dispatcher[Impl]):

    _dict: ta.Dict[ta.Type, Impl]

    def __init__(self, dict: ta.Dict[ta.Type, Impl] = None) -> None:
        super().__init__()

        if dict is not None:
            self._dict = dict
        else:
            self._dict = {}

    def _resolve(self, cls: ta.Type) -> ta.Optional[ta.Tuple[ta.Type, Impl]]:
        mro = generic_compose_mro(cls, list(self._dict.keys()))
        match = None
        for t in mro:
            if match is not None:
                # If *match* is an implicit ABC but there is another unrelated,
                # equally matching implicit ABC, refuse the temptation to guess.
                if (
                        t in self._dict and
                        t not in cls.__mro__ and
                        match not in cls.__mro__ and
                        not issubclass(match, t)
                ):
                    raise AmbiguousDispatchError(match, t)
                break
            if t in self._dict:
                match = t
        try:
            return match, self._dict[match]
        except KeyError:
            raise UnregisteredDispatchError(match)

    def _erase(self, cls: TypeOrSpec) -> ta.Type:
        return check.isinstance(rfl.erase_generic(cls.erased_cls if isinstance(cls, rfl.TypeSpec) else cls), type)

    def __setitem__(self, cls: TypeOrSpec, impl: Impl) -> None:
        cls = self._erase(cls)
        if cls in self._dict:
            raise KeyError(cls)
        self._dict[cls] = impl

    def __getitem__(self, cls: TypeOrSpec) -> ta.Tuple[ta.Optional[Impl], ta.Optional[Manifest]]:
        ecls = self._erase(cls)
        try:
            impl = self._dict[ecls]
        except KeyError:
            match, impl = self._resolve(ecls)
            return impl, Manifest(cls, match)
        else:
            return impl, Manifest(cls, ecls)

    def __contains__(self, cls: TypeOrSpec) -> bool:
        cls = self._erase(cls)
        return cls in self._dict

    def items(self) -> ta.Iterable[ta.Tuple[TypeOrSpec, Impl]]:
        return self._dict.items()


DefaultDispatcher = ErasingDictDispatcher


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
    ) -> None:
        super().__init__()

        self._cache = weakref.WeakKeyDictionary()
        self._lock = threading.RLock()

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

    def items(self) -> ta.Iterable[ta.Tuple[TypeOrSpec, Impl]]:
        yield from self._child.items()


def function() -> ta.Callable[[ta.Callable[..., R]], ta.Callable[..., R]]:
    dispatcher = CachingDispatcher(DefaultDispatcher())

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
