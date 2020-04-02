"""
TODO:
 - **overhaul to conform to _abc**
 - cythonize stuff
 - Multimap - SetMultimap
 - IdentityWeakKeyDict
 - WeakDict (key and value)
  - weak.py?
 - RingBuffer
 - Persistent (iface + pyrsistent, immutables (magicstack hamt))
 - **KeyValues**
 - boost::MultiIndex - sorted.py?
 - Immutable + Builder (put-once) + ImmutSetMultiMap
 - LinkedList (fexpr stack, dom topo)
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


"""
    public static <T> List<Set<T>> unify(Iterable<Set<T>> sets)
    {
        List<Set<T>> rem = newArrayList(sets);
        List<Set<T>> ret = new ArrayList<>();
        while (!rem.isEmpty()) {
            Set<T> cur = rem.remove(rem.size() - 1);
            boolean moved;
            do {
                moved = false;
                for (int i = rem.size() - 1; i >= 0; --i) {
                    if (rem.get(i).stream().anyMatch(cur::contains)) {
                        cur.addAll(rem.remove(i));
                        moved = true;
                    }
                }
            }
            while (moved);
            ret.add(cur);
        }
        if (!ret.isEmpty()) {
            Set<T> all = ret.stream().flatMap(Set::stream).collect(toImmutableSet());
            int num = ret.stream().map(Set::size).reduce(Integer::sum).get();
            checkState(all.size() == num);
        }
        return ret;
    }
"""