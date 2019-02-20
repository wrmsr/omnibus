import collections
import contextlib
import enum
import functools
import logging
import threading
import time
import typing as ta
import weakref

from . import lang


C = ta.TypeVar('C', bound=ta.Callable)
CC = ta.Callable[[C], C]
K = ta.TypeVar('K')
V = ta.TypeVar('V')


log = logging.getLogger(__name__)


class OverweightException(Exception):
    pass


class Cache(ta.MutableMapping[K, V]):
    """
    https://google.github.io/guava/releases/16.0/api/docs/com/google/common/cache/CacheBuilder.html
    """

    try:
        from ._ext.cy.caches import CacheLink as Link

    except ImportError:
        class Link:
            __slots__ = [
                'seq',
                'ins_prev',
                'ins_next',
                'lru_prev',
                'lru_next',
                'key',
                'value',
                'weight',
                'written',
                'accessed',
                'unlinked',
            ]

            seq: int
            ins_prev: 'Cache.Link'
            ins_next: 'Cache.Link'
            lru_prev: 'Cache.Link'
            lru_next: 'Cache.Link'
            key: ta.Union[K, weakref.ref]
            value: ta.Union[V, weakref.ref]
            weight: float
            written: float
            accessed: float
            unlinked: bool

            def __repr__(self) -> str:
                return (
                    f'Link@{str(self.seq)}('
                    f'ins_prev={("@" + str(self.ins_prev.seq)) if self.ins_prev is not None else None}, '
                    f'ins_next={("@" + str(self.ins_next.seq)) if self.ins_next is not None else None}, '
                    f'lru_prev={("@" + str(self.lru_prev.seq)) if self.lru_prev is not None else None}, '
                    f'lru_next={("@" + str(self.lru_next.seq)) if self.lru_next is not None else None}, '
                    f'key={self.key!r}, '
                    f'value={self.value!r}, '
                    f'weight={self.weight}, '
                    f'written={self.written}, '
                    f'accessed={self.accessed}, '
                    f'unlinked={self.unlinked})'
                )

    Eviction = ta.Callable[['Cache'], None]

    @lang.staticfunction
    def LRU(cache: 'Cache') -> None:
        cache._kill(cache._root.lru_next)

    @lang.staticfunction
    def LRI(cache: 'Cache') -> None:
        cache._kill(cache._root.ins_next)

    _cache: ta.MutableMapping[ta.Union[K, int], Link]

    DEFAULT_MAX_SIZE = 256

    def __init__(
            self,
            *,
            max_size: int = DEFAULT_MAX_SIZE,
            max_weight: float = None,
            identity_keys: bool = False,
            expire_after_access: float = None,
            expire_after_write: float = None,
            removal_listener: ta.Callable[[ta.Union[K, weakref.ref], ta.Union[V, weakref.ref]], None] = None,
            clock: ta.Callable[[], float] = None,
            weak_keys: bool = False,
            weak_values: bool = False,
            weigher: ta.Callable[[V], float] = lambda _: 1.,
            nolock: bool = False,
            raise_overweight: bool = False,
            eviction: Eviction = LRU,
    ) -> None:
        super().__init__()

        if clock is None:
            if expire_after_access is not None or expire_after_write is not None:
                clock = time.time
            else:
                clock = lambda: 0.  # noqa

        self._max_size = max_size
        self._max_weight = max_weight
        self._identity_keys = identity_keys
        self._expire_after_access = expire_after_access
        self._expire_after_write = expire_after_write
        self._removal_listener = removal_listener
        self._clock = clock
        self._weak_keys = weak_keys
        self._weak_values = weak_values
        self._weigher = weigher
        self._raise_overweight = raise_overweight
        self._eviction = eviction

        if not nolock:
            self._lock = threading.RLock()
        else:
            self._lock = None

        if weak_keys and not identity_keys:
            self._cache = weakref.WeakKeyDictionary()
        else:
            self._cache = {}

        self._root = Cache.Link()
        self._root.seq = 0
        self._root.ins_next = self._root.ins_prev = self._root
        self._root.lru_next = self._root.lru_prev = self._root

        if weak_keys or weak_values:
            self._weak_dead = collections.deque()
            self._weak_dead_ref = weakref.ref(self._weak_dead)
        else:
            self._weak_dead = self._weak_dead_ref = None

        self._seq = 0
        self._size = 0
        self._weight = 0.
        self._hits = 0
        self._misses = 0
        self._max_size_ever = 0
        self._max_weight_ever = 0.

    @contextlib.contextmanager
    def _locked(self):
        """Too slow for the hot methods, do not use."""

        if self._lock is not None:
            with self._lock:
                yield
        else:
            yield

    def _unlink(self, link: Link) -> None:
        if link is self._root:
            raise TypeError
        if link.unlinked:
            return

        link.ins_prev.ins_next = link.ins_next
        link.ins_next.ins_prev = link.ins_prev
        link.ins_next = link.ins_prev = link

        link.lru_prev.lru_next = link.lru_next
        link.lru_next.lru_prev = link.lru_prev
        link.lru_next = link.lru_prev = link

        if self._removal_listener is not None:
            try:
                self._removal_listener(link.key, link.value)
            except Exception:
                log.exception('Removal listener raised exception')

        link.key = link.value = None
        self._size -= 1
        self._weight -= link.weight
        link.unlinked = True

    _SKIP = object()

    def _kill(self, link) -> None:
        if link is self._root:
            raise RuntimeError

        key = link.key
        if self._weak_keys:
            key = key()
            if key is None:
                key = self._SKIP

        if key is not self._SKIP:
            cache_key = id(key) if self._identity_keys else key
            cache_link = self._cache.get(cache_key)
            if cache_link is link:
                del self._cache[cache_key]

        self._unlink(link)

    def _reap(self) -> None:
        if self._weak_dead is not None:
            while True:
                try:
                    link = self._weak_dead.popleft()
                except IndexError:
                    break
                self._unlink(link)

        clock = None

        if self._expire_after_write is not None:
            clock = self._clock()
            deadline = clock - self._expire_after_write

            while self._root.ins_next is not self._root:
                link = self._root.ins_next
                if link.written > deadline:
                    break
                self._kill(link)

        if self._expire_after_access is not None:
            if clock is None:
                clock = self._clock()
            deadline = clock - self._expire_after_access

            while self._root.lru_next is not self._root:
                link = self._root.lru_next
                if link.accessed > deadline:
                    break
                self._kill(link)

    def reap(self) -> None:
        with self._locked():
            self._reap()

    def _get_link(self, key: K) -> ta.Tuple[Link, V]:
        cache_key = id(key) if self._identity_keys else key

        link = self._cache[cache_key]

        def fail():
            try:
                del self._cache[cache_key]
            except KeyError:
                pass
            self._unlink(link)
            raise KeyError(key)

        if self._identity_keys:
            link_key = link.key
            if self._weak_keys:
                link_key = link_key()
                if link_key is None:
                    fail()
            if key is not link_key:
                fail()

        value = link.value
        if self._weak_values:
            value = value()
            if value is None:
                fail()

        return link, value

    def __getitem__(self, key: K) -> V:
        try:
            if self._lock is not None:
                self._lock.acquire()

            self._reap()

            try:
                link, value = self._get_link(key)
            except KeyError:
                self._misses += 1
                raise KeyError(key)

            link.lru_prev.lru_next = link.lru_next
            link.lru_next.lru_prev = link.lru_prev

            lru_last = self._root.lru_prev
            lru_last.lru_next = self._root.lru_prev = link
            link.lru_prev = lru_last
            link.lru_next = self._root

            link.accessed = self._clock()
            self._hits += 1
            return value

        finally:
            if self._lock is not None:
                self._lock.release()

    @staticmethod
    def _weak_die(dead_ref: weakref.ref, link: Link, key_ref: weakref.ref) -> None:
        dead = dead_ref()
        if dead is not None:
            dead.append(link)

    @property
    def _full(self) -> bool:
        if self._max_size is not None and self._size >= self._max_size:
            return True
        if self._max_weight is not None and self._weight >= self._max_weight:
            return True
        return False

    def clear(self) -> None:
        try:
            if self._lock is not None:
                self._lock.acquire()

            self._cache.clear()
            while True:
                link = self._root.ins_prev
                if link is self._root:
                    break
                if link.unlinked:
                    raise TypeError
                self._unlink(link)

        finally:
            if self._lock is not None:
                self._lock.release()

    def __setitem__(self, key: K, value: V) -> None:
        weight = self._weigher(value)

        try:
            if self._lock is not None:
                self._lock.acquire()

            self._reap()

            if self._max_weight is not None and weight > self._max_weight:
                if self._raise_overweight:
                    raise OverweightException
                else:
                    return

            try:
                existing_link, existing_value = self._get_link(key)
            except KeyError:
                pass
            else:
                self._unlink(existing_link)

            while self._full:
                self._eviction(self)

            link = Cache.Link()
            self._seq += 1
            link.seq = self._seq
            link.key = weakref.ref(key, functools.partial(Cache._weak_die, self._weak_dead_ref, link)) if self._weak_keys else key  # noqa
            link.value = weakref.ref(value, functools.partial(Cache._weak_die, self._weak_dead_ref, link)) if self._weak_values else value  # noqa
            link.weight = weight
            link.written = link.accessed = self._clock()
            link.unlinked = False

            ins_last = self._root.ins_prev
            ins_last.ins_next = self._root.ins_prev = link
            link.ins_prev = ins_last
            link.ins_next = self._root

            lru_last = self._root.lru_prev
            lru_last.lru_next = self._root.lru_prev = link
            link.lru_prev = lru_last
            link.lru_next = self._root

            self._weight += weight
            self._size += 1
            self._max_size_ever = max(self._size, self._max_size_ever)
            self._max_weight_ever = max(self._weight, self._max_weight_ever)

            cache_key = id(key) if self._identity_keys else key
            self._cache[cache_key] = link

        finally:
            if self._lock is not None:
                self._lock.release()

    def __delitem__(self, key: K) -> None:
        try:
            if self._lock is not None:
                self._lock.acquire()

            self._reap()

            link, value = self._get_link(key)

            cache_key = id(key) if self._identity_keys else key
            del self._cache[cache_key]

            self._unlink(link)

        finally:
            if self._lock is not None:
                self._lock.release()

    def __len__(self) -> int:
        try:
            if self._lock is not None:
                self._lock.acquire()

            self._reap()

            return self._size

        finally:
            if self._lock is not None:
                self._lock.release()

    def __contains__(self, key: K) -> bool:
        try:
            if self._lock is not None:
                self._lock.acquire()

            self._reap()

            try:
                self._get_link(key)
            except KeyError:
                raise False
            else:
                return True

        finally:
            if self._lock is not None:
                self._lock.release()

    def __iter__(self) -> ta.Iterator[K]:
        with self._locked():
            self._reap()

            link = self._root.ins_prev
            while link is not self._root:
                yield link
                next = link.ins_prev
                if next is link:
                    raise ValueError
                link = next

    class Stats(ta.NamedTuple):
        seq: int
        size: int
        weight: float
        hits: int
        misses: int
        max_size_ever: int
        max_weight_ever: float

    @property
    def stats(self) -> Stats:
        with self._locked():
            return Cache.Stats(
                self._seq,
                self._size,
                self._weight,
                self._hits,
                self._misses,
                self._max_size_ever,
                self._max_weight_ever,
            )


class Scope(enum.Enum):
    INSTANCE = 'INSTANCE'
    CLASS = 'CLASS'
    STATIC = 'STATIC'


class _HashedSeq(list):
    __slots__ = ['hash_value']

    def __init__(
            self,
            tup: ta.Tuple,
            hasher: ta.Callable[[ta.Any], int] = hash
    ) -> None:
        super().__init__()

        self[:] = tup
        self.hash_value = hasher(tup)

    def __hash__(self):
        return self.hash_value


def _make_key(
        args: ta.Tuple,
        kwargs: ta.Dict[str, ta.Any],
        typed: bool,
        kwd_mark=(object(),),
        fasttypes={int, str, frozenset, type(None)},
        tuple=tuple,
        type=type,
        len=len
) -> ta.Any:
    key = args
    if kwargs:
        key += kwd_mark
        for item in kwargs.items():
            key += item
    if typed:
        key += tuple(type(v) for v in args)
        if kwargs:
            key += tuple(type(v) for v in kwargs.values())
    elif len(key) == 1 and type(key[0]) in fasttypes:
        return key[0]
    return _HashedSeq(key)


class _CacheDescriptor:

    def __init__(
            self,
            fn: ta.Callable,
            scope: Scope,
            typed: bool,
            **kwargs
    ) -> None:
        super().__init__()

        self._fn = fn
        functools.update_wrapper(self, fn)
        self._scope = scope
        self._typed = typed
        self._kwargs = kwargs
        self.__static: Cache = None
        self._by_class: ta.MutableMapping[ta.Type, Cache] = weakref.WeakKeyDictionary() if scope == Scope.CLASS else None  # noqa
        self._name = None
        self._unary = kwargs.get('identity_keys', False) or kwargs.get('weak_keys', False)

    def __set_name__(self, owner, name):
        if self._name is None:
            self._name = name

    @property
    def _static(self) -> Cache:
        if self.__static is None:
            self.__static = Cache(**self._kwargs)
        return self.__static

    def _build(self, fn: ta.Callable, cache: Cache):
        if self._unary:
            @functools.wraps(fn)
            def inner(key):
                try:
                    return cache[key]
                except KeyError:
                    pass
                result = cache[key] = fn(key)
                return result

        else:
            @functools.wraps(fn)
            def inner(*args, **kwargs):
                key = _make_key(args, kwargs, self._typed)
                try:
                    return cache[key]
                except KeyError:
                    pass
                result = cache[key] = fn(*args, **kwargs)
                return result

        return inner

    def __get__(self, instance, owner):
        if self._scope == Scope.STATIC:
            cache = self._static
        elif self._scope == Scope.CLASS:
            if owner is None:
                raise TypeError
            try:
                cache = self._by_class[owner]
            except KeyError:
                cache = self._by_class[owner] = Cache(**self._kwargs)
        elif self._scope == Scope.INSTANCE:
            if instance is not None:
                cache = Cache()
            else:
                @functools.wraps(self._fn)
                def trampoline(this, *args, **kwargs):
                    return self.__get__(this, owner)(*args, **kwargs)
                return trampoline
        else:
            raise TypeError

        fn = self._build(self._fn.__get__(instance, owner), cache)

        if self._scope == Scope.CLASS:
            setattr(owner, self._name, fn)
        elif self._scope == Scope.INSTANCE:
            setattr(instance, self._name, fn)

        return fn

    def __call__(self, *args, **kwargs):
        self.__call__ = self._build(self._fn, self._static)
        return self.__call__(*args, **kwargs)


def cache(
        scope: ta.Union[Scope, str] = Scope.INSTANCE,
        typed: bool = False,
        **kwargs
) -> CC:
    if not isinstance(scope, Scope):
        scope = getattr(Scope, scope.upper())

    def inner(fn):
        return _CacheDescriptor(fn, scope, typed, **kwargs)
    return ta.cast(CC, inner)
