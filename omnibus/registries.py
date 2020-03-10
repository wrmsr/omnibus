"""
TODO:
 - DictReg.weak? key/val? currently _cannot remove_
"""
import abc
import collections.abc
import threading
import typing as ta
import weakref

from . import check
from . import collections as ocol
from . import lang


lang.warn_unstable()


K = ta.TypeVar('K')
V = ta.TypeVar('V')


class NOT_SET(lang.Marker):
    pass


class AlreadyRegisteredException(Exception):
    pass


class AmbiguouslyRegisteredException(Exception):
    pass


class NotRegisteredException(Exception):
    pass


class FrozenRegistrationException(Exception):
    pass


class Registry(abc.ABC, ta.Mapping[K, V]):

    @abc.abstractproperty
    def version(self) -> ta.Any:
        raise NotImplementedError

    @abc.abstractmethod
    def __setitem__(self, k: K, v: V) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def __getitem__(self, k: K) -> V:
        raise NotImplementedError

    @abc.abstractmethod
    def __len__(self) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def __iter__(self) -> ta.Iterator[K]:
        raise NotImplementedError

    @abc.abstractmethod
    def __contains__(self, o: object) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def items(self) -> ta.AbstractSet[ta.Tuple[K, V]]:
        raise NotImplementedError

    @abc.abstractmethod
    def keys(self) -> ta.AbstractSet[K]:
        raise NotImplementedError

    @abc.abstractmethod
    def values(self) -> ta.ValuesView[V]:
        raise NotImplementedError

    @abc.abstractmethod
    def register_many(self, dct: ta.Mapping[K, V]) -> 'Registry[K, V]':
        raise NotImplementedError

    def register(self, k: K, v: V) -> 'Registry[K, V]':
        check.not_none(k)
        return self.register_many({k: v})

    Listener = ta.Callable[['Registry[K, V]'], None]

    @abc.abstractmethod
    def add_listeners(self, listeners_by_obj: ta.Mapping[ta.Any, Listener]) -> None:
        raise NotImplementedError

    def add_listener(self, obj: ta.Any, listener: Listener) -> None:
        self.add_listeners({obj: listener})

    @abc.abstractmethod
    def remove_listeners(self, objs: ta.Iterable[ta.Any]) -> None:
        raise NotImplementedError

    def remove_listener(self, obj: ta.Any) -> None:
        self.remove_listener([obj])


class MultiRegistry(Registry[K, ta.AbstractSet[V]]):
    pass


class BaseRegistry(Registry[K, V]):

    def __init__(
            self,
            *args,
            lock: ta.Optional[lang.ContextManageable] = NOT_SET,
            listeners_by_obj: ta.Mapping[ta.Any, Registry.Listener] = None,
            **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)

        if lock is NOT_SET:
            self._lock = threading.RLock()
        elif lock is None:
            self._lock = lang.ContextManaged()
        else:
            self._lock = lock

        self._listeners_by_obj: ta.MutableMapping[ta.Any, Registry.Listener] = weakref.WeakKeyDictionary()
        for obj, listener in (listeners_by_obj or {}).items():
            self.add_listener(obj, listener)

    __hash__ = object.__hash__

    def add_listeners(self, listeners_by_obj: ta.Mapping[ta.Any, Registry.Listener]) -> None:
        listeners_by_obj = dict(listeners_by_obj)
        if not listeners_by_obj:
            return
        for obj, listener in listeners_by_obj.items():
            check.not_none(obj)
            check.callable(listener)

        with self._lock:
            for obj in listeners_by_obj.keys():
                if obj in self._listeners_by_obj:
                    raise KeyError(obj)
            for obj, listener in listeners_by_obj.items():
                self._listeners_by_obj[obj] = listener

    def remove_listeners(self, objs: ta.Iterable[ta.Any]) -> None:
        objs = list(objs)
        if not objs:
            return
        for obj in objs:
            check.not_none(obj)

        with self._lock:
            for obj in objs:
                if obj not in objs:
                    raise KeyError(obj)
            for obj in objs:
                del self._listeners_by_obj[obj]

    def _notify_listeners(self) -> None:
        for listener in self._listeners_by_obj.values():
            listener(self)


class CompositeRegistry(BaseRegistry[K, V]):

    Policy = ta.Callable[[ta.Iterable[Registry[K, V]]], ta.Mapping[K, V]]

    @staticmethod
    def FIRST_ONE(children):
        ret = {}
        for child in children:
            for k, v in child.items():
                if k not in ret:
                    ret[k] = v
        return ret

    @staticmethod
    def ONLY_ONE(children):
        ret = {}
        for child in children:
            for k, v in child.items():
                if k in ret:
                    raise AmbiguouslyRegisteredException(k, ret[k])
                ret[k] = v
        return ret

    def __init__(
            self,
            children: ta.Iterable[Registry[K, V]],
            policy: Policy = FIRST_ONE,
            **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        self._children = list(children)
        self._policy = check.callable(policy)

        with self._lock:
            def listener(_):
                with self._lock:
                    self._maybe_build()
                    self._notify_listeners()

            for child in self._children:
                child.add_listener(self, listener)

            self._version = NOT_SET
            self._maybe_build()

    @property
    def children(self) -> ta.List[Registry[K, V]]:
        return self._children

    def _maybe_build(self) -> ta.Tuple[ta.Any, ta.Mapping[K, V]]:
        with self._lock:
            version = tuple(c.version for c in self._children)
            if version != self._version:
                composed = self._policy(self._children)
                self._composed, self._version = composed, version
                self._notify_listeners()
            else:
                composed = self._composed
            return version, composed

    @property
    def version(self) -> ta.Tuple:
        return self._maybe_build()[0]

    @property
    def composed(self) -> ta.Mapping[K, V]:
        return self._maybe_build()[1]

    def __setitem__(self, k: K, v: V) -> None:
        raise TypeError

    def __getitem__(self, k: K) -> V:
        try:
            return self.composed[k]
        except KeyError:
            raise NotRegisteredException(k)

    def __iter__(self) -> ta.Iterator[K]:
        return iter(self.keys())

    def __len__(self) -> int:
        return len(self.composed)

    def __contains__(self, k: K) -> bool:
        return any(k in c for c in self._children)

    def items(self) -> ta.AbstractSet[ta.Tuple[K, V]]:
        return self.composed.items()

    def keys(self) -> ta.AbstractSet[K]:
        return self.composed.keys()

    def values(self) -> ta.ValuesView[V]:
        return self.composed.values()

    def register_many(self, dct: ta.Mapping[K, V]) -> 'Registry[K, V]':
        raise TypeError


class CompositeMultiRegistry(MultiRegistry[K, V], CompositeRegistry[K, ta.AbstractSet[V]]):

    @staticmethod
    def MERGE(children):
        ret = {}
        for child in children:
            for k, v in child.items():
                check.isinstance(v, collections.abc.Set)
                try:
                    ret[k].update(v)
                except KeyError:
                    ret[k] = set(v)
        return {k: frozenset(v) for k, v in ret.items()}

    def __init__(
            self,
            children: ta.Iterable[Registry[K, V]],
            *args,
            **kwargs,
    ) -> None:
        children = list(children)
        for child in children:
            check.isinstance(child, MultiRegistry)

        super().__init__(children, *args, **kwargs)


class DictRegistry(BaseRegistry[K, V]):

    def __init__(
            self,
            *args,
            frozen: bool = False,
            **kwargs
    ) -> None:
        super().__init__(**kwargs)

        self._dct: ta.MutableMapping[K, V] = {}

        self._version = 0

        self._frozen = False
        items = list(ocol.yield_dict_init(*args))
        if items:
            self.register_many(dict(items), silent=True)
        self._frozen = bool(frozen)
        if items:
            self._notify_listeners()

    def freeze(self) -> bool:
        with self._lock:
            if not self._frozen:
                self._frozen = True
                return True
            else:
                return False

    @property
    def frozen(self) -> bool:
        return self._frozen

    @property
    def version(self) -> int:
        return self._version

    def __setitem__(self, k: K, v: V) -> None:
        self.register(k, v)

    def __getitem__(self, k: K) -> V:
        try:
            return self._dct[k]
        except KeyError:
            raise NotRegisteredException(k)

    def __len__(self) -> int:
        return len(self._dct)

    def __iter__(self) -> ta.Iterator[K]:
        return iter(self._dct)

    def __contains__(self, o: object) -> bool:
        return o in self._dct

    def items(self) -> ta.AbstractSet[ta.Tuple[K, V]]:
        return self._dct.items()

    def keys(self) -> ta.AbstractSet[K]:
        return self._dct.keys()

    def values(self) -> ta.ValuesView[V]:
        return self._dct.values()

    def _prepare_value(self, k: K, v: V) -> V:
        return v

    def register_many(
            self,
            dct: ta.Mapping[K, V],
            *,
            silent: bool = False,
    ) -> 'Registry[K, V]':
        if self._frozen:
            raise FrozenRegistrationException(self)

        if not dct:
            return self

        with self._lock:
            ndct = {}

            for k, v in dct.items():
                check.not_none(k)

                try:
                    ov = self._dct[k]
                except KeyError:
                    pass
                else:
                    raise AlreadyRegisteredException(k, v, ov)

                ndct[k] = self._prepare_value(k, v)

            for k, v in ndct.items():
                self._dct[k] = v

            self._version += 1

            if not silent:
                self._notify_listeners()

        return self


class MultiDictRegistry(MultiRegistry[K, V], DictRegistry[K, ta.AbstractSet[V]]):

    def _prepare_value(self, k: K, v: V) -> V:
        check.arg(not isinstance(v, str))
        return frozenset(v)
