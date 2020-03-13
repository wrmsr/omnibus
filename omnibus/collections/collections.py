"""
TODO:
 - IdentityWeakKeyDict
 - WeakDict (key and value)
  - weak.py?
 - RingBuffer
 - FrozenList (backed by tuple)
 - kvs
 - Unmodifiable - java-style proxies, not copies
  - just views?
 - boost::MultiIndex - sorted.py?
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
