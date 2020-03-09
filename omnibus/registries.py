import abc
import threading
import typing as ta
import weakref

from . import check
from . import collections
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


class CompositeRegistry(Registry[K, V]):

    def __init__(
            self,
            children: ta.Iterable[Registry[K, V]],
            *,
            lock: ta.Optional[lang.ContextManageable] = NOT_SET,
    ) -> None:
        super().__init__()

        self._children = list(children)

        if lock is NOT_SET:
            self._lock = threading.RLock()
        elif lock is None:
            self._lock = lang.ContextManaged()
        else:
            self._lock = lock

        self._version = self._build_version()
        self._composed = self._build_composed()

    def _build_version(self) -> ta.Tuple:
        return tuple(c.version for c in self._children)

    @property
    def version(self) -> ta.Tuple:
        return self._build_version()

    @property
    def children(self) -> ta.List[Registry[K, V]]:
        return self._children

    @abc.abstractmethod
    def _build_composed(self) -> ta.Mapping[K, V]:
        raise NotImplementedError

    @property
    def composed(self) -> ta.Mapping[K, V]:
        with self._lock:
            version = self._build_version()
            if version != self._version:
                self._composed = self._build_composed()
                self._version = version
            return self._composed

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


class FirstOneCompositeRegistry(CompositeRegistry[K, V]):

    def _build_composed(self) -> ta.Mapping[K, V]:
        ret = {}
        for child in self._children:
            for k, v in child.items():
                if k not in ret:
                    ret[k] = v
        return ret


class OnlyOneCompositeRegistry(CompositeRegistry[K, V]):

    def _build_composed(self) -> ta.Mapping[K, V]:
        ret = {}
        for child in self._children:
            for k, v in child.items():
                if k in ret:
                    raise AmbiguouslyRegisteredException(k, ret[k])
                ret[k] = v
        return ret


class DictRegistry(Registry[K, V]):

    def __init__(
            self,
            *args,
            lock: ta.Optional[lang.ContextManageable] = NOT_SET,
            weak: bool = False,
            frozen: bool = False,
    ) -> None:
        super().__init__()

        self._weak = bool(weak)

        if lock is NOT_SET:
            self._lock = threading.RLock()
        elif lock is None:
            self._lock = lang.ContextManaged()
        else:
            self._lock = lock

        dct: ta.MutableMapping[K, V]
        if self._weak:
            dct = weakref.WeakValueDictionary()
        else:
            dct = {}
        self._dct = dct

        self._version = 0

        self._frozen = False
        for k, v in collections.yield_dict_init(*args):
            self[k] = v
        self._frozen = bool(frozen)

    @property
    def weak(self) -> bool:
        return self._weak

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

    def register_many(self, dct: ta.Mapping[K, V]) -> 'Registry[K, V]':
        if self._frozen:
            raise FrozenRegistrationException(self)

        if not dct:
            return self

        with self._lock:
            for k, v in dct.items():
                check.not_none(k)

                try:
                    ov = self._dct[k]
                except KeyError:
                    pass
                else:
                    raise AlreadyRegisteredException(k, v, ov)

            for k, v in dct.items():
                self._dct[k] = v

            self._version += 1

        return self
