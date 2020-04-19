import abc
import typing as ta

from .. import lang
from .frozen import FrozenDict


K = ta.TypeVar('K')
T = ta.TypeVar('T')
V = ta.TypeVar('V')


class Persistent(ta.Hashable, lang.Abstract):
    pass


class PersistentSequence(ta.Sequence[T], Persistent):

    @abc.abstractmethod
    def append(self, item: T) -> 'PersistentSequence[T]':
        raise NotImplementedError

    @abc.abstractmethod
    def extend(self, items: ta.Iterable[T]) -> 'PersistentSequence[T]':
        raise NotImplementedError

    @abc.abstractmethod
    def set(self, idx: int, item: T) -> 'PeresistentSequence[T]':
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, idx: int, stop: int = None) -> 'PersistentSequence[T]':
        raise NotImplementedError


class PersistentSet(ta.AbstractSet[T], Persistent):

    @abc.abstractmethod
    def add(self, item: T) -> 'PersistentSet[T]':
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, items: ta.Iterable[T]) -> 'PersistentSet[T]':
        raise NotImplementedError

    @abc.abstractmethod
    def remove(self, item: T) -> 'PeresistentSet[T]':
        raise NotImplementedError


class PersistentMapping(ta.Mapping[K, V], Persistent):

    @abc.abstractmethod
    def set(self, key: K, value: V) -> 'PersistentMapping[K, V]':
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, other: ta.Mapping[K, V]) -> 'PersistentMapping[K, V]':
        raise NotImplementedError

    @abc.abstractmethod
    def remove(self, key: K) -> 'PersistentMapping[K, V]':
        raise NotImplementedError


class SimplePersistentSequence(PersistentSequence[T]):

    def __init__(self, items: ta.Iterable[T] = None) -> None:
        super().__init__()

        if items is None:
            items = ()
        elif not isinstance(items, tuple):
            items = tuple(items)
        self._tuple = items

    def __hash__(self) -> int:
        return hash(self._tuple)

    def append(self, item: T) -> 'PersistentSequence[T]':
        return SimplePersistentSequence(self._tuple + (item,))

    def extend(self, items: ta.Iterable[T]) -> 'PersistentSequence[T]':
        return SimplePersistentSequence(self._tuple + tuple(items))

    def set(self, idx: int, item: T) -> 'PeresistentSequence[T]':
        if idx >= 0:
            t = self._tuple[:idx] + (item,) + self._tuple[idx + 1:]
        else:
            t = self._tuple[:idx] + (item,) + (self._tuple[idx+1:] if idx < -1 else ())
        return SimplePersistentSequence(t)

    def delete(self, idx: int, stop: int = None) -> 'PersistentSequence[T]':
        if stop is not None:
            l = list(self._tuple)
            del l[idx:stop]
            t = tuple(l)
        else:
            if idx >= 0:
                t = self._tuple[:idx] + self._tuple[idx + 1:]
            else:
                t = self._tuple[:idx] + (self._tuple[idx+1:] if idx < -1 else ())
        return SimplePersistentSequence(t)

    def __getitem__(self, i: ta.Union[int, slice]) -> T:
        return self._tuple[i]

    def __len__(self) -> int:
        return len(self._tuple)

    def __contains__(self, x: object) -> bool:
        return x in self._tuple

    def __iter__(self) -> ta.Iterator[T]:
        return iter(self._tuple)

    def __reversed__(self) -> ta.Iterator[T]:
        return reversed(self._tuple)


class SimplePersistentSet(PersistentSet[T]):

    def __init__(self, items: ta.Iterable[T] = None) -> None:
        super().__init__()

        self._set = frozenset(items or ())

    def __hash__(self) -> int:
        return hash(self._set)

    def add(self, item: T) -> 'PersistentSet[T]':
        return SimplePersistentSet(self._set | frozenset([item]))

    def update(self, items: ta.Iterable[T]) -> 'PersistentSet[T]':
        return SimplePersistentSet(self._set | frozenset(items))

    def remove(self, item: T) -> 'PeresistentSet[T]':
        return SimplePersistentSet(self._set - frozenset([item]))

    def __contains__(self, x: object) -> bool:
        return x in self._set

    def __len__(self) -> int:
        return len(self._set)

    def __iter__(self) -> ta.Iterator[T]:
        return iter(self._set)


class SimplePersistentMapping(PersistentMapping[K, V]):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self._dct = FrozenDict(*args, **kwargs)

    def __hash__(self) -> int:
        return hash(self._dct)

    def set(self, key: K, value: V) -> 'PersistentMapping[K, V]':
        return SimplePersistentMapping({**self._dct, **{key: value}})

    def update(self, other: ta.Mapping[K, V]) -> 'PersistentMapping[K, V]':
        return SimplePersistentMapping({**self._dct, **other})

    def remove(self, key: K) -> 'PersistentMapping[K, V]':
        return SimplePersistentMapping({k: v for k, v in self._dct.items() if k != key})

    def __getitem__(self, k: K) -> V:
        return self._dct[k]

    def __len__(self) -> int:
        return len(self._dct)

    def __iter__(self) -> ta.Iterator[K]:
        return iter(self._dct)

    def items(self) -> ta.AbstractSet[ta.Tuple[K, V]]:
        return self._dct.items()

    def keys(self) -> ta.AbstractSet[K]:
        return self._dct.keys()

    def values(self) -> ta.ValuesView[V]:
        return self._dct.values()

    def __contains__(self, o: object) -> bool:
        return o in self._dct


if ta.TYPE_CHECKING:
    import pyrsistent
else:
    pyrsistent = lang.proxy_import('pyrsistent')


class PyrsistentSequence(PersistentSequence[T]):

    def __init__(self, items: ta.Iterable[T] = None) -> None:
        super().__init__()
        if isinstance(items, pyrsistent.PVector):
            self._p = items
        else:
            self._p = pyrsistent.pvector(*((items,) if items else ()))

    def __hash__(self) -> int:
        return hash(self._p)

    def append(self, item: T) -> 'PersistentSequence[T]':
        return PyrsistentSequence(self._p.append(item))

    def extend(self, items: ta.Iterable[T]) -> 'PersistentSequence[T]':
        if isinstance(items, PyrsistentSequence):
            items = items._p
        return PyrsistentSequence(self._p.extend(items))

    def set(self, idx: int, item: T) -> 'PeresistentSequence[T]':
        return PyrsistentSequence(self._p.set(idx, item))

    def delete(self, idx: int, stop: int = None) -> 'PersistentSequence[T]':
        return PyrsistentSequence(self._p.delete(idx, stop))

    def __getitem__(self, i: int) -> T:
        return self._p[i]

    def __len__(self) -> int:
        return len(self._p)

    def __contains__(self, x: object) -> bool:
        return x in self._p

    def __iter__(self) -> ta.Iterator[T]:
        return iter(self._p)

    def __reversed__(self) -> ta.Iterator[T]:
        return reversed(self._p)


class PyrsistentSet(PersistentSet[T]):

    def __init__(self, items: ta.Iterable[T] = None) -> None:
        super().__init__()
        if isinstance(items, pyrsistent.PSet):
            self._p = items
        else:
            self._p = pyrsistent.pset(*((items,) if items else ()))

    def __hash__(self) -> int:
        return hash(self._p)

    def add(self, item: T) -> 'PersistentSet[T]':
        return PyrsistentSet(self._p.add(item))

    def update(self, items: ta.Iterable[T]) -> 'PersistentSet[T]':
        if isinstance(items, PyrsistentSet):
            items = items._p
        return PyrsistentSet(self._p.update(items))

    def remove(self, item: T) -> 'PeresistentSet[T]':
        return PyrsistentSet(self._p.remove(item))

    def __contains__(self, x: object) -> bool:
        return x in self._p

    def __len__(self) -> int:
        return len(self._p)

    def __iter__(self) -> ta.Iterator[T]:
        return iter(self._p)


class PyrsistentMapping(PersistentMapping[K, V]):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self._p = pyrsistent.pmap(*args, **kwargs)

    def __hash__(self) -> int:
        return hash(self._p)

    def set(self, key: K, value: V) -> 'PersistentMapping[K, V]':
        return PyrsistentMapping(self._p.set(key, value))

    def update(self, other: ta.Mapping[K, V]) -> 'PersistentMapping[K, V]':
        if isinstance(other, PyrsistentMapping):
            other = other._p
        return PyrsistentMapping(self._p.update(other))

    def remove(self, key: K) -> 'PersistentMapping[K, V]':
        return PyrsistentMapping(self._p.remove(key))

    def __getitem__(self, k: K) -> V:
        return self._p[k]

    def __len__(self) -> int:
        return len(self._p)

    def __iter__(self) -> ta.Iterator[K]:
        return iter(self._p)

    def items(self) -> ta.AbstractSet[ta.Tuple[K, V]]:
        return self._p.items()

    def keys(self) -> ta.AbstractSet[K]:
        return self._p.keys()

    def values(self) -> ta.ValuesView[V]:
        return self._p.values()

    def __contains__(self, o: object) -> bool:
        return o in self._p
