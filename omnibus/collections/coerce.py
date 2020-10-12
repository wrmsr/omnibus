import typing as ta

from .frozen import FrozenDict
from .frozen import FrozenList


T = ta.TypeVar('T')
T2 = ta.TypeVar('T2')
K = ta.TypeVar('K')
K2 = ta.TypeVar('K2')
V = ta.TypeVar('V')
V2 = ta.TypeVar('V2')


_map = map


# region seq


def seq(it: ta.Iterable[T]) -> ta.Sequence[T]:
    if isinstance(it, str):
        raise TypeError(it)
    elif isinstance(it, FrozenList):
        return it
    else:
        return FrozenList(it)


def optional_seq(it: ta.Optional[ta.Iterable[T]]) -> ta.Optional[ta.Sequence[T]]:
    if it is None:
        return None
    else:
        return seq(it)


def seq_or_none(it: ta.Optional[ta.Iterable[T]]) -> ta.Optional[ta.Sequence[T]]:
    ret = optional_seq(it)
    if ret:
        return ret
    else:
        return None


def seq_of(fn: ta.Callable[[T], T2]) -> ta.Callable[[ta.Iterable[T]], ta.Sequence[T2]]:
    def inner(it):
        return seq(fn(e) for e in it)
    return inner


def optional_seq_of(fn: ta.Callable[[T], T2]) -> ta.Callable[[ta.Optional[ta.Iterable[T]]], ta.Optional[ta.Sequence[T2]]]:  # noqa
    def inner(it):
        if it is None:
            return None
        else:
            return seq(fn(e) for e in it)
    return inner


def seq_of_or_none(fn: ta.Callable[[T], T2]) -> ta.Callable[[ta.Optional[ta.Iterable[T]]], ta.Optional[ta.Sequence[T2]]]:  # noqa
    def inner(it):
        if it is None:
            return None
        else:
            ret = seq(fn(e) for e in it)
            if ret:
                return ret
            else:
                return None
    return inner


# endregion


# region abs_set


def abs_set(it: ta.Iterable[T]) -> ta.AbstractSet[T]:  # noqa
    if isinstance(it, str):
        raise TypeError(it)
    elif isinstance(it, frozenset):
        return it
    else:
        return frozenset(it)


def optional_abs_set(it: ta.Optional[ta.Iterable[T]]) -> ta.Optional[ta.AbstractSet[T]]:  # noqa
    if it is None:
        return None
    else:
        return abs_set(it)


def abs_set_or_none(it: ta.Optional[ta.Iterable[T]]) -> ta.Optional[ta.AbstractSet[T]]:  # noqa
    ret = optional_abs_set(it)
    if ret:
        return ret
    else:
        return None


def abs_set_of(fn: ta.Callable[[T], T2]) -> ta.Callable[[ta.Iterable[T]], ta.AbstractSet[T2]]:
    def inner(it):
        return abs_set(fn(e) for e in it)
    return inner


def optional_abs_set_of(fn: ta.Callable[[T], T2]) -> ta.Callable[[ta.Optional[ta.Iterable[T]]], ta.Optional[ta.AbstractSet[T2]]]:  # noqa
    def inner(it):
        if it is None:
            return None
        else:
            return abs_set(fn(e) for e in it)
    return inner


def abs_set_of_or_none(fn: ta.Callable[[T], T2]) -> ta.Callable[[ta.Optional[ta.Iterable[T]]], ta.Optional[ta.AbstractSet[T2]]]:  # noqa
    def inner(it):
        if it is None:
            return None
        else:
            ret = abs_set(fn(e) for e in it)
            if ret:
                return ret
            else:
                return None
    return inner


# endregion


# region map


def map(src: ta.Union[ta.Mapping[K, V], ta.Iterable[ta.Tuple[K, V]]]) -> ta.Mapping[K, V]:  # noqa
    return FrozenDict(src)


def optional_map(src: ta.Optional[ta.Union[ta.Mapping[K, V], ta.Iterable[ta.Tuple[K, V]]]]) -> ta.Optional[ta.Mapping[K, V]]:  # noqa
    if src is None:
        return None
    else:
        return map(src)


def map_or_none(src: ta.Optional[ta.Union[ta.Mapping[K, V], ta.Iterable[ta.Tuple[K, V]]]]) -> ta.Optional[ta.Mapping[K, V]]:  # noqa
    ret = optional_map(src)
    if ret:
        return ret
    else:
        return None


def map_of(
        key_fn: ta.Callable[[K], K2],
        value_fn: ta.Callable[[V], V2],
) -> ta.Callable[
     [ta.Union[ta.Mapping[K, V], ta.Iterable[ta.Tuple[K, V]]]],
     ta.Mapping[K2, V2],
]:
    def inner(src):
        return map((key_fn(k), value_fn(v)) for k, v in dict(src).items())
    return inner


def optional_map_of(
        key_fn: ta.Callable[[K], K2],
        value_fn: ta.Callable[[V], V2],
) -> ta.Callable[
    [ta.Optional[ta.Union[ta.Mapping[K, V], ta.Iterable[ta.Tuple[K, V]]]]],
    ta.Optional[ta.Mapping[K2, V2]],
]:
    def inner(src):
        if src is None:
            return None
        else:
            return map((key_fn(k), value_fn(v)) for k, v in dict(src).items())
    return inner


def map_of_or_none(
        key_fn: ta.Callable[[K], K2],
        value_fn: ta.Callable[[V], V2],
) -> ta.Callable[
    [ta.Optional[ta.Union[ta.Mapping[K, V], ta.Iterable[ta.Tuple[K, V]]]]],
    ta.Optional[ta.Mapping[K2, V2]],
]:
    def inner(src):
        if src is None:
            return None
        else:
            ret = map((key_fn(k), value_fn(v)) for k, v in dict(src).items())
            if ret:
                return ret
            else:
                return None
    return inner


# endregion
