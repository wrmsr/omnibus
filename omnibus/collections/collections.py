"""
TODO:
 - **overhaul to conform to _abc**
 - cythonize stuff
  - http://www.cplusplus.com/reference/stl/ for int/long/float/double/ptr/bytes/PyObject
 - Multimap - SetMultimap
 - IdentityWeakKeyDict
 - WeakDict (key and value)
  - weak.py?
 - RingBuffer
 - Persistent (iface + pyrsistent, immutables (magicstack hamt))
 - **KeyValues**
  - old repo, support scalars/slices/tuples/ranges intermixed - spans now?
  - *implemented as a major extension to collections but as a toplevel subpackage, like configs is to dataclasses**
 - boost::MultiIndex - sorted.py?
 - Immutable + Builder (put-once) + ImmutSetMultiMap
 - LinkedList (fexpr stack, dom topo)
 - IndexableSet
 - https://github.com/MagicStack/immutables
"""
import functools
import typing as ta


T = ta.TypeVar('T')


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
