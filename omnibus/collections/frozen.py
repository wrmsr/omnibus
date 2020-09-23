"""
TODO:
 - __eq__ consistency
 - hash/total_ordering - FrozenDict retains insertion order honoring, sort keys on demand
 - dict operators (inc __or__ / __ror__ / __ior__)
 - list operators
 - views, slices
 - cy
"""
import collections.abc
import itertools
import typing as ta

from .. import lang
from .maps import yield_dict_init


T = ta.TypeVar('T')
K = ta.TypeVar('K')
V = ta.TypeVar('V')


class Frozen(ta.Hashable, lang.Abstract):
    pass


class FrozenDict(ta.Mapping[K, V], Frozen, lang.Final):

    def __new__(cls, *args, **kwargs) -> 'FrozenDict[K, V]':
        if len(args) == 1 and Frozen in type(args[0]).__bases__:
            return args[0]
        return super().__new__(cls)

    def __init__(self, *args, **kwargs):
        super().__init__()
        self._hash = None
        if len(args) > 1:
            raise TypeError(args)
        self._dct = {}
        self._dct.update(yield_dict_init(*args, **kwargs))

    @property
    def debug(self) -> ta.Mapping[K, V]:
        return dict(self._dct)

    def __repr__(self) -> str:
        return '%s(%r)' % (type(self).__name__, self._dct)

    def __eq__(self, other) -> bool:
        return type(self) == type(other) and self._dct == other._dct

    def __getitem__(self, key: K) -> V:
        return self._dct[key]

    def __getstate__(self):
        return tuple(self.items())

    def __hash__(self) -> int:
        if self._hash is None:
            self._hash = hash((k, self[k]) for k in sorted(self))
        return self._hash

    def __iter__(self) -> ta.Iterator[K]:
        return iter(self._dct)

    def __len__(self) -> int:
        return len(self._dct)

    def __ne__(self, other) -> bool:
        return not (self == other)

    def __setstate__(self, t):
        self.__init__(t)

    def drop(self, *keys):
        keys = frozenset(keys)
        return type(self)((k, self[k]) for k in self if k not in keys)

    def set(self, *args, **kwargs):
        new = type(self)(*args, **kwargs)
        return type(self)(itertools.chain(self.items(), new.items()))


frozendict = FrozenDict


class FrozenList(ta.Sequence[T], Frozen, lang.Final):

    def __init__(self, it: ta.Iterable[T] = None) -> None:
        super().__init__()

        self._tup: tuple = tuple(it) if it is not None else ()
        self._hash = None

    @property
    def debug(self) -> ta.Sequence[T]:
        return list(self)

    def __repr__(self) -> str:
        return '%s([%s])' % (type(self).__name__, ', '.join(map(repr, self._tup)))

    def __add__(self, o) -> 'FrozenList[T]':
        if isinstance(o, FrozenList):
            return FrozenList(self._tup + o._tup)
        elif isinstance(o, collections.abc.Sequence):
            return FrozenList(self._tup + tuple(o))
        else:
            return NotImplemented

    def __contains__(self, x: object) -> bool:
        return x in self._tup

    def __eq__(self, o: object) -> bool:
        if isinstance(o, FrozenList):
            return self._tup == o._tup
        elif isinstance(o, collections.abc.Sequence):
            return len(self) == len(o) and all(l == r for l, r in zip(self, o))
        else:
            return False

    def __hash__(self) -> int:
        if self._hash is None:
            self._hash = hash(self._tup)
        return self._hash

    def __getitem__(self, idx: ta.Union[int, slice]) -> 'FrozenList[T]':
        if isinstance(idx, int):
            return self._tup[idx]
        else:
            return FrozenList(self._tup[idx])

    def __iter__(self) -> ta.Iterator[T]:
        return iter(self._tup)

    def __len__(self) -> int:
        return len(self._tup)

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

    def __radd__(self, o) -> 'FrozenList[T]':
        if isinstance(o, FrozenList):
            return FrozenList(o._tup + self._tup)
        elif isinstance(o, collections.abc.Sequence):
            return FrozenList(tuple(o) + self._tup)
        else:
            return NotImplemented

    def __reversed__(self) -> ta.Iterator[T]:
        return reversed(self._tup)

    def count(self, x: ta.Any) -> int:
        return super().count(x)

    def index(self, x: ta.Any, *args, **kwargs) -> int:
        return self._tup.index(x, *args, **kwargs)


frozenlist = FrozenList
