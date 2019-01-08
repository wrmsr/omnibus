import abc
import collections.abc
import enum
import functools
import itertools
import operator as op
import random
import typing as ta

from . import lang
from . import properties


T = ta.TypeVar('T')
K = ta.TypeVar('K')
V = ta.TypeVar('V')


def toposort(data: ta.Dict[T, ta.Set[T]]) -> ta.Iterator[ta.Set[T]]:
    for k, v in data.items():
        v.discard(k)
    extra_items_in_deps = functools.reduce(set.union, data.values()) - set(data.keys())
    data.update(dict((item, set()) for item in extra_items_in_deps))
    while True:
        ordered = set(item for item, dep in data.items() if not dep)
        if not ordered:
            break
        yield ordered
        data = dict((item, (dep - ordered)) for item, dep in data.items() if item not in ordered)
    if data:
        raise ValueError('Cyclic dependencies exist among these items: ' + ' '.join(repr(x) for x in data.items()))


def histogram(seq: ta.Iterable[ta.Any]) -> ta.Dict[ta.Any, int]:
    ret = {}
    for item in seq:
        try:
            ret[item] += 1
        except KeyError:
            ret[item] = 1
    return ret


def multikey_dict(dct: ta.Dict[ta.Union[ta.Iterable[K], K], V], *, deep: bool = False) -> ta.Dict[K, V]:
    ret = {}
    for k, v in dct.items():
        if deep and isinstance(v, dict):
            v = multikey_dict(v, deep=True)
        if isinstance(k, tuple):
            for k in k:
                ret[k] = v
        else:
            ret[k] = v
    return ret


def guarded_dict_update(dst: ta.Dict[ta.Any, ta.Any], *srcs: ta.Dict[ta.Any, ta.Any]) -> ta.Dict[ta.Any, ta.Any]:
    for src in srcs:
        for k, v in src.items():
            if k in dst:
                raise KeyError(k)
            dst[k] = v
    return dst


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


def yield_dict_init(*args, **kwargs) -> ta.Iterable[ta.Tuple[ta.Any, ta.Any]]:
    if len(args) > 1:
        raise TypeError
    if args:
        [src] = args
        if isinstance(src, collections.abc.Mapping):
            for k in src:
                yield (k, src[k])
        else:
            for k, v in src:
                yield (k, v)
    for k, v in kwargs.items():
        yield (k, v)


class WrappedKeyDict(ta.MutableMapping[K, V]):

    def __init__(self, wrapper: ta.Callable[[K], ta.Any], unwrapper: ta.Callable[[ta.Any], K], *args, **kwargs) -> None:
        super().__init__()
        self._dct = {}
        self._wrapper = wrapper
        self._unwrapper = unwrapper
        for k, v in yield_dict_init(*args, **kwargs):
            self[k] = v

    def __repr__(self) -> str:
        return lang.attr_repr(self, '_dct')

    def __setitem__(self, k: K, v: V) -> None:
        self._dct[self._wrapper(k)] = v

    def __delitem__(self, k: K) -> None:
        del self._dct[self._wrapper(k)]

    def __getitem__(self, k: K) -> V:
        return self._dct[self._wrapper(k)]

    def __len__(self) -> int:
        return len(self._dct)

    def __iter__(self) -> ta.Iterator[K]:
        return iter(map(self._unwrapper, self._dct))

    def clear(self):
        self._dct.clear()


class IdentityKeyDict(ta.MutableMapping[K, V]):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self._dict = {}
        for k, v in yield_dict_init(*args, **kwargs):
            self[id(k)] = (k, v)

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


class FrozenDict(ta.Mapping[K, V]):
    __slots__ = ('_dct', '_hash')

    def __new__(cls, *args, **kwargs):
        if len(args) == 1:
            [arg] = args
            if isinstance(arg, cls):
                return arg
        return super().__new__(cls)

    def __init__(self, *args, **kwargs):
        super().__init__()
        self._hash = None
        if len(args) > 1:
            raise TypeError()
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
            self._hash = hash(frozenset(self._dct.items()))
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


bintrees = lang.lazy_import('bintrees')


class BintreesDict(SortedMutableMapping[K, V]):

    Item = ta.Tuple[K, V]

    class Impl(enum.Enum):
        RB = 'RB'
        AVL = 'AVL'

    @properties.class_
    def _impls(cls) -> ta.Mapping[Impl, ta.Type]:
        return {
            BintreesDict.Impl.RB: bintrees().FastRBTree,
            BintreesDict.Impl.AVL: bintrees().FastAVLTree,
        }

    @classmethod
    def new(cls, impl: ta.Union[Impl, str] = Impl.RB, *args, **kwargs) -> 'BintreesDict':
        return cls(cls._impls[BintreesDict.Impl(impl)](), *args, **kwargs)

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
        return self._tree.items()

    def ritems(self) -> ta.Iterator[Item]:
        return self._tree.items(reverse=True)

    def itemsfrom(self, key: K) -> ta.Iterator[Item]:
        return self._tree.iter_items(key)

    def ritemsfrom(self, key: K) -> ta.Iterator[Item]:
        try:
            yield (key, self._tree[key])
        except KeyError:
            pass
        yield from self._tree.iter_items(None, key, reverse=True)


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
        return itertools.islice(self._tree.items(), self._tree.bisect_left(key), None)

    def ritemsfrom(self, key: K) -> ta.Iterator[Item]:
        try:
            yield (key, self._tree[key])
        except KeyError:
            pass
        yield from self._tree.iter_items(None, key, reverse=True)
