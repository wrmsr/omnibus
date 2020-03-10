import abc
import itertools
import random
import typing as ta

from .. import lang


T = ta.TypeVar('T')
K = ta.TypeVar('K')
V = ta.TypeVar('V')


class SortedList(lang.Abstract, ta.Generic[T]):

    Comparator = ta.Callable[[T, T], int]

    @staticmethod
    def default_comparator(a: T, b: T) -> int:
        """https://docs.python.org/3.0/whatsnew/3.0.html#ordering-comparisons"""

        return (a > b) - (a < b)

    @abc.abstractmethod
    def __len__(self) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def __iter__(self) -> ta.Iterator[T]:
        raise NotImplementedError

    @abc.abstractmethod
    def __contains__(self, value: T) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def add(self, value: T) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def find(self, value: T) -> ta.Optional[T]:
        raise NotImplementedError

    @abc.abstractmethod
    def remove(self, value: T) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def iter(self, base: T = None) -> ta.Iterable[T]:
        raise NotImplementedError

    @abc.abstractmethod
    def riter(self, base: T = None) -> ta.Iterable[T]:
        raise NotImplementedError


class SkipList(SortedList[T]):
    """https://gist.github.com/icejoywoo/3bf0c54983a725fa3917"""

    class _Node:
        __slots__ = [
            'value',
            'level',
            'next',
            'prev',
        ]

        next: ta.List[ta.Optional['SkipList._Node']]
        prev: ta.Optional['SkipList._Node']

        def __init__(
                self,
                value: T,
                level: int
        ) -> None:
            super().__init__()

            if level <= 0:
                raise TypeError('level must be > 0')

            self.value = value
            self.level = level
            self.next = [None] * level
            self.prev = None

        def __repr__(self) -> str:
            return f'{type(self).__name__}(value={self.value!r})'

    def __init__(
            self,
            *,
            max_height: int = 16,
            comparator: SortedList.Comparator[T] = None,
    ) -> None:
        super().__init__()

        if comparator is None:
            comparator = SortedList.default_comparator
        self._compare = comparator
        self._max_height = max_height
        self._head = SkipList._Node(None, self._max_height)
        self._height = 1
        self._head.next = [None] * self._max_height
        self._length = 0

    def __len__(self) -> int:
        return self._length

    def __iter__(self) -> ta.Iterator[T]:
        return iter(self.iter())

    def __contains__(self, value: T) -> bool:
        return self.find(value) is not None

    def _random_level(self) -> int:
        result = 1
        while random.uniform(0, 1) < 0.5 and result < self._max_height:
            result += 1
        return result

    def add(self, value: T) -> bool:
        if value is None:
            raise TypeError(value)

        node = SkipList._Node(value, self._random_level())
        update = [None] * self._max_height
        cur = self._head

        for i in range(self._height - 1, -1, -1):
            while cur.next[i] is not None and self._compare(value, cur.next[i].value) > 0:
                cur = cur.next[i]
            update[i] = cur

        cur = cur.next[0]
        if cur is not None:
            if self._compare(value, cur.value) == 0:
                return False
            node.prev, cur.prev = cur.prev, node
        else:
            node.prev = update[0]

        if node.level > self._height:
            for i in range(self._height, node.level):
                update[i] = self._head
            self._height = node.level

        for i in range(node.level):
            cur = update[i]
            node.next[i] = cur.next[i]
            cur.next[i] = node

        self._length += 1
        return True

    def _find(self, value: T) -> ta.Optional[_Node]:
        if value is None:
            raise TypeError(value)

        cur = self._head

        for i in range(self._height - 1, -1, -1):
            while cur.next[i] and self._compare(value, cur.next[i].value) > 0:
                cur = cur.next[i]

        return cur.next[0]

    def find(self, value: T) -> ta.Optional[T]:
        node = self._find(value)
        if node is None:
            return None
        if node is None or self._compare(value, node.value) != 0:
            return None
        return node.value

    def remove(self, value: T) -> bool:
        if value is None:
            raise TypeError(value)

        update = [None] * self._max_height
        cur = self._head

        for i in range(self._height - 1, -1, -1):
            while cur.next[i] is not None and self._compare(value, cur.next[i].value) > 0:
                cur = cur.next[i]
            update[i] = cur

        cur = cur.next[0]
        if cur is None or self._compare(value, cur.value) != 0:
            return False
        elif cur.next[0] is not None:
            cur.next[0].prev = cur.prev

        for i in range(self._height):
            if update[i].next[i] is not cur:
                break
            update[i].next[i] = cur.next[i]

        while self._height > 0 and self._head.next[self._height - 1] is None:
            self._height -= 1

        self._length -= 1
        return True

    def iter(self, base: T = None) -> ta.Iterable[T]:
        if base is not None:
            cur = self._find(base)
            while cur is not None and self._compare(base, cur.value) > 0:
                cur = cur.next[0]
        else:
            cur = self._head.next[0]

        while cur is not None:
            yield cur.value
            cur = cur.next[0]

    def riter(self, base: T = None) -> ta.Iterable[T]:
        if base is not None:
            cur = self._find(base)
            while cur is not self._head and self._compare(base, cur.value) < 0:
                cur = cur.prev
        else:
            cur = self._head.next[self._height - 1]
            while True:
                next = cur.next[cur.next.index(None) - 1 if None in cur.next else -1]
                if next is None:
                    break
                cur = next

        while cur is not self._head:
            yield cur.value
            cur = cur.prev


class SortedMapping(ta.Mapping[K, V]):

    @abc.abstractmethod
    def items(self) -> ta.Iterator[ta.Tuple[K, V]]:
        raise NotImplementedError

    @abc.abstractmethod
    def ritems(self) -> ta.Iterator[ta.Tuple[K, V]]:
        raise NotImplementedError

    @abc.abstractmethod
    def itemsfrom(self, key: K) -> ta.Iterator[ta.Tuple[K, V]]:
        raise NotImplementedError

    @abc.abstractmethod
    def ritemsfrom(self, key: K) -> ta.Iterator[ta.Tuple[K, V]]:
        raise NotImplementedError


class SortedMutableMapping(ta.MutableMapping[K, V], SortedMapping[K, V]):
    pass


class SortedListDict(SortedMutableMapping[K, V]):

    Item = ta.Tuple[K, V]
    _impl: SortedList[Item]

    @staticmethod
    def _item_comparator(a: Item, b: Item) -> int:
        return SortedList.default_comparator(a[0], b[0])

    def __init__(self, impl: SortedList[Item], *args, **kwargs) -> None:
        self._impl = impl

        super().__init__(*args, **kwargs)

    def __getitem__(self, key: K) -> V:
        item = self._impl.find((key, None))
        if item is None:
            raise KeyError(key)
        return item[1]

    def __setitem__(self, key: K, value: V) -> None:
        self._impl.remove((key, None))
        self._impl.add((key, value))

    def __delitem__(self, key: K) -> None:
        self._impl.remove((key, None))

    def __len__(self) -> int:
        return len(self._impl)

    def __iter__(self) -> ta.Iterator[K]:
        for k, v in self._impl:
            yield k

    def items(self) -> ta.Iterator[Item]:
        yield from self._impl.iter()

    def ritems(self) -> ta.Iterator[Item]:
        yield from self._impl.riter()

    def itemsfrom(self, key: K) -> ta.Iterator[Item]:
        yield from self._impl.iter((key, None))

    def ritemsfrom(self, key: K) -> ta.Iterator[Item]:
        yield from self._impl.riter((key, None))


class SkipListDict(SortedListDict[K, V]):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(SkipList(comparator=SortedListDict._item_comparator), *args, **kwargs)


sortedcontainers = lang.lazy_import('sortedcontainers')


class SortedContainersDict(SortedMutableMapping[K, V]):

    Item = ta.Tuple[K, V]

    @classmethod
    def new(cls, *args, **kwargs) -> 'SortedContainersDict':
        return cls(sortedcontainers().SortedDict(), *args, **kwargs)

    def __init__(self, tree: ta.Any, *args, **kwargs) -> None:
        self._tree = tree

        super().__init__(*args, **kwargs)

    def __getitem__(self, key: K) -> V:
        return self._tree[key]

    def __setitem__(self, key: K, value: V) -> None:
        self._tree[key] = value

    def __delitem__(self, key: K) -> None:
        del self._tree[key]

    def __len__(self) -> int:
        return len(self._tree)

    def __iter__(self) -> ta.Iterator[K]:
        return iter(self._tree)

    def items(self) -> ta.Iterator[Item]:
        return iter(self._tree.items())

    def ritems(self) -> ta.Iterator[Item]:
        return reversed(self._tree.items())

    def itemsfrom(self, key: K) -> ta.Iterator[Item]:
        yield from itertools.islice(self._tree.items(), self._tree.bisect_left(key), None)

    def ritemsfrom(self, key: K) -> ta.Iterator[Item]:
        yield from itertools.islice(reversed(self._tree.items()), len(self._tree) - self._tree.bisect_right(key), None)
