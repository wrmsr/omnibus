import abc
import typing as ta
import weakref

from .. import lang
from .. import reflect as rfl
from .. import registries
from .types import CacheGuard
from .types import Dispatcher
from .types import Impl
from .types import Manifest
from .types import TypeOrSpec


class AbcCacheGuard(CacheGuard):

    def __init__(
            self,
            lock: lang.DefaultLockable,
            clear: ta.Callable,
    ) -> None:
        super().__init__()

        self._lock = lang.default_lock(lock, True)
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
                with self._lock():
                    current_token = abc.get_cache_token()
                    if self._cache_token != current_token:
                        self._clear()
                        self._cache_token = current_token
                        return True

        return False


class CachingDispatcher(Dispatcher[Impl]):

    def __init__(
            self,
            child: Dispatcher[Impl],
            guard: CacheGuard = None,
            *,
            lock: lang.DefaultLockable = None,
    ) -> None:
        super().__init__()

        self._cache = weakref.WeakKeyDictionary()
        self._lock = lang.default_lock(lock, True)

        self._child = child
        self._guard = guard if guard is not None else AbcCacheGuard(self._lock, self.clear)

    def key(self, obj: ta.Any) -> TypeOrSpec:
        return self._child.key(obj)

    @property
    def child(self) -> Dispatcher[Impl]:
        return self._child

    @property
    def registry(self) -> registries.Registry[TypeOrSpec, Impl]:
        return self._child.registry

    @property
    def guard(self) -> CacheGuard:
        return self._guard

    def clear(self) -> None:
        with self._lock():
            self._cache.clear()

    def register_many(self, keys: ta.Iterable[TypeOrSpec], impl: Impl) -> 'CachingDispatcher[Impl]':
        keys = list(keys)
        self._child.register_many(keys, impl)
        for key in keys:
            self._guard.update(key)
        self.clear()
        return self

    def dispatch(self, key: TypeOrSpec) -> ta.Tuple[ta.Optional[Impl], ta.Optional[Manifest]]:
        self._guard.maybe_clear()
        try:
            impl, manifest = self._cache[key]
        except KeyError:
            with self._lock():
                impl, manifest = self._child.dispatch(key)
                self._cache[key] = (impl, manifest)
        return impl, manifest

    def __contains__(self, key: TypeOrSpec) -> bool:
        return key in self._child
