"""
TODO:
 - clean tf up lol
"""
import typing as ta


T = ta.TypeVar('T')


class OrderedSet(ta.MutableSet[T]):

    def __init__(self, iterable=None):
        super().__init__()
        self._end = end = []
        end += [None, end, end]  # sentinel node for doubly linked list
        self._map = {}  # item --> [item, prev, next]
        if iterable is not None:
            self |= iterable

    def __len__(self) -> int:
        return len(self._map)

    def __contains__(self, item: T) -> bool:
        return item in self._map

    def add(self, item: T) -> None:
        if item not in self._map:
            end = self._end
            curr = end[1]
            curr[2] = end[1] = self._map[item] = [item, curr, end]

    def discard(self, item: T) -> None:
        if item in self._map:
            item, prev, next = self._map.pop(item)
            prev[2] = next
            next[1] = prev

    def __iter__(self) -> ta.Iterator[T]:
        end = self._end
        curr = end[2]
        while curr is not end:
            yield curr[0]
            curr = curr[2]

    def __reversed__(self):
        end = self._end
        curr = end[1]
        while curr is not end:
            yield curr[0]
            curr = curr[1]

    def pop(self, last=True):
        if not self:
            raise KeyError('set is empty')
        item = self._end[1][0] if last else self._end[2][0]
        self.discard(item)
        return item

    def __repr__(self):
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, list(self))

    def __eq__(self, other) -> bool:
        if isinstance(other, OrderedSet):
            return len(self) == len(other) and list(self) == list(other)
        return set(self) == set(other)


class OrderedFrozenSet(ta.FrozenSet[T]):

    def __new__(cls, items: ta.Iterable[T]) -> ta.FrozenSet[T]:
        item_set = set()
        item_list = []
        for item in items:
            if item not in item_set:
                item_set.add(item)
                item_list.append(item)
        obj = super(cls, OrderedFrozenSet).__new__(cls, item_set)
        obj._list = item_list
        return obj

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}([{", ".join(map(repr, self))}])'

    def __iter__(self) -> ta.Iterator[T]:
        return iter(self._list)

    def __sub__(self, other: ta.Iterable[T]) -> ta.FrozenSet[T]:
        s = set(other)
        return type(self)(i for i in self if i not in s)
