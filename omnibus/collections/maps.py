"""
TODO:
 - dict update w policy (replace, check, raise)
  - generic? mutating vs immut?
  - cats/tcs/dispatch powered?
 - set_once_mapping
  - whatever guava haas
"""
import collections.abc
import typing as ta
import weakref


T = ta.TypeVar('T')
K = ta.TypeVar('K')
V = ta.TypeVar('V')


def multikey_dict(dct: ta.Mapping[ta.Union[ta.Iterable[K], K], V], *, deep: bool = False) -> ta.Dict[K, V]:
    ret = {}
    for k, v in dct.items():
        if deep and isinstance(v, dict):
            v = multikey_dict(v, deep=True)  # type: ignore
        if isinstance(k, tuple):
            for sk in k:
                ret[sk] = v
        else:
            ret[k] = v
    return ret


def guarded_map_update(
        dst: ta.MutableMapping[ta.Any, ta.Any],
        *srcs: ta.Mapping[ta.Any, ta.Any]
) -> ta.MutableMapping[ta.Any, ta.Any]:
    for src in srcs:
        for k, v in src.items():
            if k in dst:
                raise KeyError(k)
            dst[k] = v
    return dst


def traverse_links(data: ta.Mapping[T, ta.Iterable[T]], keys: ta.Iterable[T]) -> ta.Set[T]:
    keys = set(keys)
    todo = set(keys)
    seen: ta.Set[T] = set()
    while todo:
        key = todo.pop()
        seen.add(key)
        cur = data.get(key, [])
        todo.update(set(cur) - seen)
    return seen - keys


def invert_set_map(src: ta.Mapping[K, ta.Iterable[V]], *, symmetric: bool = False) -> ta.Dict[V, ta.Set[K]]:
    dst: ta.Dict[V, ta.Set[K]]
    if symmetric:
        dst = {ta.cast(V, l): set() for l in src}
    else:
        dst = {}
    for l, rs in src.items():
        for r in rs:
            dst.setdefault(r, set()).add(l)
    return dst


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


class ItemSeqTypeMap(ta.Generic[T]):

    def __init__(self, items: ta.Iterable[T], *, weak: bool = False) -> None:
        super().__init__()

        self._items = list(items)
        self._weak = bool(weak)

        self._cache: ta.MutableMapping[ta.Type[T], ta.Sequence[T]] = weakref.WeakKeyDictionary() if weak else {}  # type: ignore  # noqa

    @property
    def items(self) -> ta.Sequence[T]:
        return self._items

    @property
    def weak(self) -> bool:
        return self._weak

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self) -> ta.Iterable[T]:
        return iter(self._items)

    def __getitem__(self, cls: ta.Type[T]) -> ta.Sequence[T]:
        try:
            return self._cache[cls]
        except KeyError:
            ret = []
            for item in self._items:
                if isinstance(item, cls):
                    ret.append(item)
            self._cache[cls] = ret
            return ret
