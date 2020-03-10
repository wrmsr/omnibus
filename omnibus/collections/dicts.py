import collections.abc
import typing as ta

from .. import lang


K = ta.TypeVar('K')
V = ta.TypeVar('V')


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
