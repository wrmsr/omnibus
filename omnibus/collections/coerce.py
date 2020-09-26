import typing as ta

from .frozen import FrozenDict
from .frozen import FrozenList


T = ta.TypeVar('T')
T2 = ta.TypeVar('T2')
K = ta.TypeVar('K')
K2 = ta.TypeVar('K2')
V = ta.TypeVar('V')
V2 = ta.TypeVar('V2')


def seq(it: ta.Iterable[T]) -> ta.Sequence[T]:
    return FrozenList(it)


def seq_of(fn: ta.Callable[[T], T2]) -> ta.Callable[[ta.Iterable[T]], ta.Sequence[T2]]:
    def inner(it):
        if isinstance(it, str):
            raise TypeError(it)
        return seq(fn(e) for e in it)
    return inner


def set(it: ta.Iterable[T]) -> ta.AbstractSet[T]:  # noqa
    return frozenset(it)


def set_of(fn: ta.Callable[[T], T2]) -> ta.Callable[[ta.Iterable[T]], ta.AbstractSet[T2]]:
    def inner(it):
        if isinstance(it, str):
            raise TypeError(it)
        return set(fn(e) for e in it)
    return inner


def map(src: ta.Union[ta.Mapping[K, V], ta.Iterable[ta.Tuple[K, V]]]) -> ta.Mapping[K, V]:  # noqa
    return FrozenDict(src)


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
