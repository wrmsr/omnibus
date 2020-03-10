import itertools
import typing as ta

from .dicts import yield_dict_init


K = ta.TypeVar('K')
V = ta.TypeVar('V')


class _FrozenDict:
    pass


class FrozenDict(ta.Mapping[K, V], _FrozenDict):

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

    def __repr__(self):
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
