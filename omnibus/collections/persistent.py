import abc
import typing as ta

from .. import lang


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
    def delete(self, index: int, stop: int = None) -> 'PersistentSequence[T]':
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
    pass


class SimplePersistentSet(PersistentSet[T]):
    pass


class SimplePersistentMapping(PersistentMapping[K, V]):
    pass


pyrsistent = lang.lazy_import('pyrsistent')


class PyrsistentSequence(PersistentSequence[T]):
    pass


class PyrsistentSet(PersistentSet[T]):
    pass


class PyrsistentMapping(PersistentMapping[K, V]):
    pass
