"""
TODO:
 - cy: retain pycharm dbg output - public prop?
"""
import operator as op
import typing as ta

from .. import lang
from .maps import yield_dict_init


T = ta.TypeVar('T')
K = ta.TypeVar('K')
V = ta.TypeVar('V')


class IdentityWrapper(ta.Generic[T]):

    def __init__(self, value: T):
        super().__init__()
        self._value = value

    def __repr__(self) -> str:
        return lang.attr_repr(self, 'value')

    @property
    def value(self) -> T:
        return self._value

    def __eq__(self, other: T) -> bool:
        return isinstance(other, IdentityWrapper) and other._value is self._value

    def __ne__(self, other: T) -> bool:
        return not (self == other)

    def __hash__(self):
        return id(self._value)


class IdentityKeyDict(ta.MutableMapping[K, V]):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self._dict = {}
        for k, v in yield_dict_init(*args, **kwargs):
            self[k] = v

    @property
    def debug(self) -> ta.Sequence[ta.Tuple[K, V]]:
        return list(self.items())

    def __repr__(self) -> str:
        return lang.attr_repr(self, '_dict')

    def __setitem__(self, k: K, v: V) -> None:
        self._dict[id(k)] = (k, v)

    def __delitem__(self, k: K) -> None:
        del self._dict[id(k)]

    def __getitem__(self, k: K) -> V:
        return self._dict[id(k)][1]

    def __len__(self) -> int:
        return len(self._dict)

    def __iter__(self) -> ta.Iterator[K]:
        return iter(map(op.itemgetter(0), self._dict.values()))

    def clear(self):
        self._dict.clear()


class IdentitySet(ta.MutableSet[T]):

    def __init__(self, init: ta.Iterable[T] = None):
        super().__init__()
        self._dict = {}
        if init is not None:
            for item in init:
                self.add(item)

    @property
    def debug(self) -> ta.Sequence[T]:
        return list(self)

    def __repr__(self) -> str:
        return lang.attr_repr(self, '_dict')

    def add(self, item: T) -> None:
        self._dict[id(item)] = item

    def discard(self, item: T) -> None:
        try:
            del self._dict[id(item)]
        except KeyError:
            pass

    def update(self, items: ta.Iterable[T]) -> None:
        for item in items:
            self.add(item)

    def __contains__(self, item: T) -> bool:
        return id(item) in self._dict

    def __len__(self) -> int:
        return len(self._dict)

    def __iter__(self) -> ta.Iterator[T]:
        return iter(self._dict.values())


class IdentityHashableDict(ta.Dict[K, V]):

    def __hash__(self) -> int:
        return id(self)

    def __eq__(self, other: ta.Any) -> bool:
        return self is other

    def __ne__(self, other: ta.Any) -> bool:
        return self is not other

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({super().__repr__()})'


class IdentityHashableSet(ta.Set[T]):

    def __hash__(self):
        return id(self)

    def __eq__(self, other: ta.Any) -> bool:
        return self is other

    def __ne__(self, other: ta.Any) -> bool:
        return self is not other

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({super().__repr__()})'


class IdentityHashableList(ta.List[T]):

    def __hash__(self):
        return id(self)

    def __eq__(self, other: ta.Any) -> bool:
        return self is other

    def __ne__(self, other: ta.Any) -> bool:
        return self is not other

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({super().__repr__()})'
