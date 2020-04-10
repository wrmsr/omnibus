import abc
import typing as ta

from .. import lang


K = ta.TypeVar('K')
V = ta.TypeVar('V')


class OverweightException(Exception):
    pass


class Cache(ta.MutableMapping[K, V]):
    """
    https://google.github.io/guava/releases/16.0/api/docs/com/google/common/cache/CacheBuilder.html
    """

    Eviction = ta.Callable[['Cache'], None]

    @lang.staticfunction
    def LRU(cache: 'Cache') -> None:
        cache._kill(cache._root.lru_next)

    @lang.staticfunction
    def LRI(cache: 'Cache') -> None:
        cache._kill(cache._root.ins_next)

    @abc.abstractmethod
    def reap(self) -> None:
        pass

    class Stats(ta.NamedTuple):
        seq: int
        size: int
        weight: float
        hits: int
        misses: int
        max_size_ever: int
        max_weight_ever: float

    @abc.abstractproperty
    def stats(self) -> Stats:
        raise NotImplementedError
