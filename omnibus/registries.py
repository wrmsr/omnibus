import abc
import threading
import typing as ta
import weakref

from . import check
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


class Registry(abc.ABC, ta.Mapping[K, V]):

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
    ) -> None:
        super().__init__()

        self._children = list(children)

    @property
    def children(self) -> ta.List[Registry[K, V]]:
        return self._children

    @abc.abstractmethod
    def compose(self) -> ta.Mapping[K, V]:
        raise NotImplementedError

    def __setitem__(self, k: K, v: V) -> None:
        raise TypeError

    def __iter__(self) -> ta.Iterator[K]:
        return iter(self.keys())

    def __len__(self) -> int:
        return len(self.compose())

    def __contains__(self, k: K) -> bool:
        return any(k in c for c in self._children)

    def items(self) -> ta.AbstractSet[ta.Tuple[K, V]]:
        return self.compose().items()

    def keys(self) -> ta.AbstractSet[K]:
        return self.compose().keys()

    def values(self) -> ta.ValuesView[V]:
        return self.compose().values()

    def register_many(self, dct: ta.Mapping[K, V]) -> 'Registry[K, V]':
        raise TypeError


class FirstOneCompositeRegistry(CompositeRegistry[K, V]):

    def compose(self) -> ta.Mapping[K, V]:
        ret = {}
        for child in self._children:
            for k, v in child.items():
                if k not in ret:
                    ret[k] = v
        return ret

    def __getitem__(self, k: K) -> V:
        for child in self._children:
            try:
                return child[k]
            except KeyError:
                pass
        raise NotRegisteredException(k)


class OnlyOneCompositeRegistry(CompositeRegistry[K, V]):

    def compose(self) -> ta.Mapping[K, V]:
        ret = {}
        for child in self._children:
            for k, v in child.items():
                if k in ret:
                    raise AmbiguouslyRegisteredException(k, ret[k])
                ret[k] = v
        return ret

    def __getitem__(self, k: K) -> V:
        hits = []
        for child in self._children:
            try:
                hits.append(child[k])
            except NotRegisteredException:
                pass
        if len(hits) == 1:
            return hits[0]
        elif hits:
            raise AmbiguouslyRegisteredException(k, hits)
        else:
            raise NotRegisteredException(k)


class DictRegistry(Registry[K, V]):

    def __init__(
            self,
            *,
            lock: ta.Optional[lang.ContextManageable] = NOT_SET,
            weak: bool = False,
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
        with self._lock:
            for k, v in dct.items():
                check.not_none(k)

                try:
                    ov = self._dct[k]
                except KeyError:
                    pass
                else:
                    raise AlreadyRegisteredException(k, v, ov)

                self._dct[k] = v

        return self
