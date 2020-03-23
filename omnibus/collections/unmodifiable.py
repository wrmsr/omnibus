import typing as ta

from .. import check


T = ta.TypeVar('T')
K = ta.TypeVar('K')
V = ta.TypeVar('V')


class UnmodifiableSequence(ta.Sequence[T]):

    def __init__(self, target: ta.Sequence[T]) -> None:
        super().__init__()

        self._target = check.not_none(target)

    def __repr__(self) -> str:
        return '%s(%r)' % (type(self).__name__, self._target)

    def __getitem__(self, i: ta.Union[int, slice]) -> T:
        return self._target[i]

    def index(self, x: ta.Any, *args, **kwargs) -> int:
        return self._target.index(x, *args, **kwargs)

    def count(self, x: ta.Any) -> int:
        return self._target.count(x)

    def __contains__(self, x: object) -> bool:
        return x in self._target

    def __iter__(self) -> ta.Iterator[T]:
        return iter(self._target)

    def __reversed__(self) -> ta.Iterator[T]:
        return reversed(self._target)

    def __len__(self) -> int:
        return len(self._target)

    def __eq__(self, o: object) -> bool:
        return self._target == o

    def __ne__(self, o: object) -> bool:
        return self._target != o


class UnmodifiableSet(ta.AbstractSet[T]):

    def __init__(self, target: ta.AbstractSet[T]) -> None:
        super().__init__()

        self._target = check.not_none(target)

    def __repr__(self) -> str:
        return '%s(%r)' % (type(self).__name__, self._target)

    def __contains__(self, x: object) -> bool:
        return x in self._target

    def __le__(self, s: ta.AbstractSet[ta.Any]) -> bool:
        return self._target <= s

    def __lt__(self, s: ta.AbstractSet[ta.Any]) -> bool:
        return self._target > s

    def __gt__(self, s: ta.AbstractSet[ta.Any]) -> bool:
        return self._target > s

    def __ge__(self, s: ta.AbstractSet[ta.Any]) -> bool:
        return self._target >= s

    def __and__(self, s: ta.AbstractSet[ta.Any]) -> ta.AbstractSet[T]:
        return self._target & s

    def __or__(self, s: ta.AbstractSet[T]) -> ta.AbstractSet[T]:
        return self._target | s

    def __sub__(self, s: ta.AbstractSet[ta.Any]) -> ta.AbstractSet[T]:
        return self._target - s

    def __xor__(self, s: ta.AbstractSet[T]) -> ta.AbstractSet[T]:
        return self._target ^ s

    def isdisjoint(self, s: ta.Iterable[ta.Any]) -> bool:
        return self._target.isdisjoint(s)

    def __len__(self) -> int:
        return len(self._target)

    def __iter__(self) -> ta.Iterator[T]:
        return iter(self._target)

    def __eq__(self, o: object) -> bool:
        return self._target == o

    def __ne__(self, o: object) -> bool:
        return self._target != o


class UnmodifiableMapping(ta.Mapping[K, V]):

    def __init__(self, target: ta.Mapping[K, V]) -> None:
        super().__init__()

        self._target = check.not_none(target)

    def __repr__(self) -> str:
        return '%s(%r)' % (type(self).__name__, self._target)

    def __getitem__(self, k: K) -> V:
        return self._target[k]

    def get(self, k: K, default=None) -> ta.Optional[V]:
        return self._target.get(k)

    def items(self) -> ta.AbstractSet[ta.Tuple[K, V]]:
        return self._target.items()

    def keys(self) -> ta.AbstractSet[K]:
        return self._target.keys()

    def values(self) -> ta.ValuesView[V]:
        return self._target.values()

    def __contains__(self, o: object) -> bool:
        return o in self._target

    def __len__(self) -> int:
        return len(self._target)

    def __iter__(self) -> ta.Iterator[T]:
        return iter(self._target)

    def __eq__(self, o: object) -> bool:
        return self._target == o

    def __ne__(self, o: object) -> bool:
        return self._target != o
