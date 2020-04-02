"""
TODO:
 - dict update w policy (replace, check, raise)
"""
import collections.abc
import typing as ta


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
