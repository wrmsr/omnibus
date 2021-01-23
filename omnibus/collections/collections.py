"""
TODO:
 - **overhaul to conform to _abc**
 - cythonize stuff
  - http://www.cplusplus.com/reference/stl/ for int/long/float/double/ptr/bytes/PyObject
 - Multimap - SetMultimap
 - IdentityWeakKeyDict
 - WeakDict (key and value)
  - weak.py?
 - OneForAllWeakSet
 - RingBuffer
 - Persistent (iface + pyrsistent, immutables (magicstack hamt))
  - old repo, support scalars/slices/tuples/ranges intermixed - spans now?
  - *implemented as a major extension to collections but as a toplevel subpackage, like configs is to dataclasses**
  - interops:
   - sql
   - sqlite
   - redis
   - dynamo
   - rocksdb
   - leveldb (btc)
   - bsddb3 (btc)
 - Immutable + Builder (put-once) + ImmutSetMultiMap
 - LinkedList (fexpr stack, dom topo)
 - IndexableSet
 - https://github.com/MagicStack/immutables
 - null policy? reject like guava?
 - interops:
  - MagicStack/immutables
  - blist
  - bitarray
  - pyroaring
  - pyhash
  - preshed (mph)
  - tdigest (move to math/, with stats.py)
 - bidir map
 - guava table (graph in graph pkg)
 - https://github.com/rust-lang/ena
 - https://github.com/aio-libs/multidict
 - indexable OrderedSet - + back by dict? OrderedIdentitySet?
"""
import functools
import typing as ta

from .. import lang
from .identity import IdentityKeyDict
from .identity import IdentitySet
from .ordered import OrderedFrozenSet
from .ordered import OrderedSet


T = ta.TypeVar('T')
T2 = ta.TypeVar('T2')
K = ta.TypeVar('K')
K2 = ta.TypeVar('K2')
V = ta.TypeVar('V')
V2 = ta.TypeVar('V2')


ORDERING_TYPES = (ta.Sequence, OrderedSet, OrderedFrozenSet)
OrderingT = ta.Union[ta.Sequence[T], OrderedSet[T], OrderedFrozenSet[T]]


def mut_toposort(data: ta.Dict[T, ta.Set[T]]) -> ta.Iterator[ta.Set[T]]:
    for k, v in data.items():
        v.discard(k)
    extra_items_in_deps = functools.reduce(set.union, data.values()) - set(data.keys())
    data.update({item: set() for item in extra_items_in_deps})
    while True:
        ordered = set(item for item, dep in data.items() if not dep)
        if not ordered:
            break
        yield ordered
        data = {item: (dep - ordered) for item, dep in data.items() if item not in ordered}
    if data:
        raise ValueError('Cyclic dependencies exist among these items: ' + ' '.join(repr(x) for x in data.items()))


def toposort(data: ta.Mapping[T, ta.AbstractSet[T]]) -> ta.Iterator[ta.Set[T]]:
    return mut_toposort({k: set(v) for k, v in data.items()})


def histogram(seq: ta.Iterable[ta.Any]) -> ta.Dict[ta.Any, int]:
    ret: ta.Dict[ta.Any, int] = {}
    for item in seq:
        try:
            ret[item] += 1
        except KeyError:
            ret[item] = 1
    return ret


def unify(sets: ta.Iterable[ta.AbstractSet[T]]) -> ta.List[ta.Set[T]]:
    rem: ta.List[ta.Set[T]] = [set(s) for s in sets]
    ret: ta.List[ta.Set[T]] = []

    while rem:
        cur = rem.pop()
        while True:
            moved = False
            i = len(rem) - 1
            while i >= 0:
                if any(e in cur for e in rem[i]):
                    cur |= rem[i]
                    del rem[i]
                    moved = True
                i -= 1
            if not moved:
                break
        ret.append(cur)

    if ret:
        ret_set = {e for s in ret for e in s}
        ret_len = sum(map(len, ret))
        if ret_len != len(ret_set):
            raise ValueError(ret)

    return ret


def partition(items: ta.Iterable[T], pred: ta.Callable[[T], bool]) -> ta.Tuple[ta.List[T], ta.List[T]]:
    t, f = [], []
    for e in items:
        if pred(e):
            t.append(e)
        else:
            f.append(e)
    return t, f


def list_dict(
        items: ta.Iterable[T],
        key: ta.Callable[[V], K],
        map: ta.Callable[[T], V] = lang.identity,
        *,
        identity_dict: bool = False,
) -> ta.Dict[K, ta.List[V]]:
    dct = IdentityKeyDict() if identity_dict else {}
    for e in items:
        k = key(e)
        v = map(e)
        dct.setdefault(k, []).append(v)
    return dct


def set_dict(
        items: ta.Iterable[T],
        key: ta.Callable[[T], K],
        map: ta.Callable[[T], V] = lang.identity,
        *,
        identity_dict: bool = False,
        identity_set: bool = False,
) -> ta.Dict[K, ta.Set[V]]:
    dct = IdentityKeyDict() if identity_dict else {}
    for e in items:
        k = key(e)
        v = map(e)
        dct.setdefault(k, IdentitySet() if identity_set else set()).add(v)
    return dct


def unique(it: ta.Iterable[T]) -> ta.Sequence[T]:
    if isinstance(it, str):
        raise TypeError(it)
    ret = []
    seen: ta.Set[T] = set()
    for e in it:
        if e not in seen:
            seen.add(e)
            ret.append(e)
    return ret


def unique_dict(items: ta.Iterable[ta.Tuple[K, V]], *, identity: bool = False) -> ta.Dict[K, V]:
    dct = IdentityKeyDict() if identity else {}
    for k, v in items:
        if k in dct:
            raise KeyError(k)
        dct[k] = v
    return dct


def order_values(values: ta.Container[T], ordering: OrderingT) -> ta.List[T]:
    if not isinstance(ordering, ORDERING_TYPES):
        raise TypeError(ordering)
    lst = []
    seen = set()
    for v in ordering:
        if v in values and v not in seen:
            lst.append(v)
            seen.add(v)
    return lst


def order_set(values: ta.Container[T], ordering: OrderingT) -> OrderedSet[T]:
    return OrderedSet(order_values(values, ordering))


def order_frozen_set(values: ta.Container[T], ordering: OrderingT) -> OrderedFrozenSet[T]:
    return OrderedFrozenSet(order_values(values, ordering))
