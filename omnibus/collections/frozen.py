"""
TODO:
 - dict operators
 - list operators
 - views, slices
"""
import collections.abc
import itertools
import typing as ta

from .dicts import yield_dict_init


T = ta.TypeVar('T')
K = ta.TypeVar('K')
V = ta.TypeVar('V')


class Frozen:
    pass


class FrozenDict(ta.Mapping[K, V], Frozen):

    def __new__(cls, *args, **kwargs) -> 'FrozenDict[K, V]':
        if len(args) == 1 and _FrozenDict in type(args[0]).__bases__:
            return args[0]
        return super().__new__(cls, dict(*args, **kwargs))

    def __init__(self, *args, **kwargs):
        super().__init__()
        self._hash = None
        if len(args) > 1:
            raise TypeError(args)
        self._dct = {}
        self._dct.update(yield_dict_init(*args, **kwargs))

    def __repr__(self) -> str:
        return '%s(%r)' % (type(self).__name__, self._dct)

    def __getitem__(self, key: K) -> V:
        return self._dct[key]

    def __len__(self) -> int:
        return len(self._dct)

    def __iter__(self) -> ta.Iterator[K]:
        return iter(self._dct)

    def __hash__(self) -> int:
        if self._hash is None:
            self._hash = hash((k, self[k]) for k in sorted(self))
        return self._hash

    def __eq__(self, other) -> bool:
        return type(self) == type(other) and self._dct == other._dct

    def __ne__(self, other) -> bool:
        return not (self == other)

    def __getstate__(self):
        return tuple(self.items())

    def __setstate__(self, t):
        self.__init__(t)

    def drop(self, *keys):
        keys = frozenset(keys)
        return type(self)((k, self[k]) for k in self if k not in keys)

    def set(self, *args, **kwargs):
        new = type(self)(*args, **kwargs)
        return type(self)(itertools.chain(self.items(), new.items()))


class FrozenList(ta.Sequence[T], Frozen):

    def __init__(self, it: ta.Iterable[T] = None) -> None:
        super().__init__()

        self._tup: tuple = tuple(it) if it is not None else ()

    def __repr__(self) -> str:
        return '%s(%r)' % (type(self).__name__, self._tup)

    def __getitem__(self, idx: ta.Union[int, slice]) -> 'FrozenList[T]':
        return FrozenList(self._tup[idx])

    def __len__(self) -> int:
        return len(self._tup)

    def index(self, x: ta.Any, start: int = ..., end: int = ...) -> int:
        return self._tup.index(x, start, end)

    def count(self, x: ta.Any) -> int:
        return super().count(x)

    def __contains__(self, x: object) -> bool:
        return x in self._tup

    def __iter__(self) -> ta.Iterator[T]:
        return iter(self._tup)

    def __reversed__(self) -> ta.Iterator[T]:
        return reversed(self._tup)

    def __eq__(self, o: object) -> bool:
        if isinstance(o, FrozenList):
            return self._tup == o._tup
        elif isinstance(o, collections.abc.Sequence):
            return len(self) == len(o) and all(l == r for l, r in zip(self, o))
        else:
            return False

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

    def __add__(self, o) -> 'FrozenList[T]':
        if isinstance(o, FrozenList):
            return FrozenList(self._tup + o._tup)
        elif isinstance(o, collections.abc.Sequence):
            return FrozenList(self._tup + tuple(o))
        else:
            return NotImplemented

    def __radd__(self, o) -> 'FrozenList[T]':
        if isinstance(o, FrozenList):
            return FrozenList(o._tup + self._tup)
        elif isinstance(o, collections.abc.Sequence):
            return FrozenList(tuple(o) + self._tup)
        else:
            return NotImplemented
