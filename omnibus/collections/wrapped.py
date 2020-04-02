import functools
import itertools
import typing as ta

from .. import check


TF = ta.TypeVar('TF')
TT = ta.TypeVar('TT')
KF = ta.TypeVar('KF')
KT = ta.TypeVar('KT')
VF = ta.TypeVar('VF')
VT = ta.TypeVar('VT')


@functools.total_ordering
class WrappedSequence(ta.MutableSequence[TT], ta.Generic[TF, TT]):
    """
 '__delitem__',
 '__iadd__',
 '__setitem__',
 'append',
 'clear',
 'extend',
 'insert',
 'pop',
 'remove',
    """

    def __init__(
            self,
            encoder: ta.Callable[[TF], TT],
            decoder: ta.Callable[[TT], TF],
            target: ta.Sequence[TF],
    ) -> None:
        super().__init__()

        self._encoder = check.callable(encoder)
        self._decoder = check.callable(decoder)
        self._target = check.not_none(target)

    def __repr__(self) -> str:
        return '%s(%r)' % (type(self).__name__, self._target)

    def __contains__(self, x: object) -> bool:
        return self._encoder(x) in self._target

    def __getitem__(self, i: ta.Union[int, slice]) -> T:
        return self._decoder(self._target[i])

    def __lt__(self, s: ta.AbstractSet[ta.Any]) -> bool:
        missing = object()
        for l, r in itertools.zip_longest(self, s, fillvalue=missing):
            if l is missing:
                return False
            elif r is missing:
                return True
            elif l < r:
                return True
            elif r < l:
                return False
        return False

    def index(self, x: ta.Any, *args, **kwargs) -> int:
        return self._target.index(self._encoder(x), *args, **kwargs)

    def count(self, x: ta.Any) -> int:
        return self._target.count(self._encoder(x))

    def __iter__(self) -> ta.Iterator[TT]:
        return map(self._decoder, self._target)

    def __reversed__(self) -> ta.Iterator[TT]:
        return map(self._decoder, reversed(self._target))

    def __len__(self) -> int:
        return len(self._target)

    def __eq__(self, o: object) -> bool:
        if not len(self._target) == len(o):
            return False
        for l, r in zip(self, o):
            if l != o:
                return False
        return True

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)


@functools.total_ordering
class WrappedSet(ta.MutableSet[TT], ta.Generic[TF, TT]):
    """
 '__and__',
 '__contains__',
 '__eq__',
 '__iand__',
 '__ior__',
 '__isub__',
 '__iter__',
 '__ixor__',
 '__len__',
 '__ne__',
 '__new__',
 '__or__',
 '__rand__',
 '__repr__',
 '__ror__',
 '__rsub__',
 '__rxor__',
 '__sub__',
 '__xor__',
 'add',
 'clear',
 'discard',
 'isdisjoint',
 'pop',
 'remove',
    """

    def __init__(
            self,
            encoder: ta.Callable[[TF], TT],
            decoder: ta.Callable[[TT], TF],
            target: ta.Sequence[TF],
    ) -> None:
        super().__init__()

        self._encoder = check.callable(encoder)
        self._decoder = check.callable(decoder)
        self._target = check.not_none(target)

    def __repr__(self) -> str:
        return '%s(%r)' % (type(self).__name__, self._target)

    def __contains__(self, x: object) -> bool:
        return self._encoder(x) in self._target

    def __lt__(self, s: ta.AbstractSet[ta.Any]) -> bool:
        missing = object()
        for l, r in itertools.zip_longest(self, s, fillvalue=missing):
            if l is missing:
                return False
            elif r is missing:
                return True
            elif l < r:
                return True
            elif r < l:
                return False
        return False

    def __and__(self, s: ta.AbstractSet[ta.Any]) -> ta.AbstractSet[T]:
        return self._target & s

    def __or__(self, s: ta.AbstractSet[T]) -> ta.AbstractSet[T]:
        return self._target | s

    def __sub__(self, s: ta.AbstractSet[ta.Any]) -> ta.AbstractSet[T]:
        return self._target - s

    def __xor__(self, s: ta.AbstractSet[T]) -> ta.AbstractSet[T]:
        return self._target ^ s

    def __len__(self) -> int:
        return len(self._target)

    def __iter__(self) -> ta.Iterator[T]:
        return iter(self._target)

    def __eq__(self, o: object) -> bool:
        return self._target == o

    def __ne__(self, o: object) -> bool:
        return self._target != o

    def isdisjoint(self, s: ta.Iterable[ta.Any]) -> bool:
        return self._target.isdisjoint(s)


class WrappedMapping(ta.MutableMapping[K, V]):
    """
 '__contains__',
 '__delitem__',
 '__eq__',
 '__getitem__',
 '__iter__',
 '__len__',
 '__ne__',
 '__reversed__',
 '__setitem__',
 'clear',
 'get',
 'items',
 'keys',
 'pop',
 'popitem',
 'setdefault',
 'update',
 'values',
    """

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
