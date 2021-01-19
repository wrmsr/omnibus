"""
TODO:
 - indexable retaining iterator (window? abs/rel?)
"""
import collections
import functools
import typing as ta


T = ta.TypeVar('T')


_MISSING = object()


class PeekIterator(ta.Iterator[T]):

    def __init__(self, it: ta.Iterator[T]) -> None:
        super().__init__()

        self._it = it
        self._pos = -1
        self._next_item: ta.Any = _MISSING

    _item: T

    def __iter__(self) -> ta.Iterator[T]:
        return self

    @property
    def done(self) -> bool:
        try:
            self.peek()
            return False
        except StopIteration:
            return True

    def __next__(self) -> T:
        if self._next_item is not _MISSING:
            self._item = ta.cast(T, self._next_item)
            self._next_item = _MISSING
        else:
            try:
                self._item = next(self._it)
            except StopIteration:
                raise
        self._pos += 1
        return self._item

    def peek(self) -> T:
        if self._next_item is not _MISSING:
            return ta.cast(T, self._next_item)
        try:
            self._next_item = next(self._it)
        except StopIteration:
            raise
        return self._next_item

    def next_peek(self) -> T:
        next(self)
        return self.peek()

    def takewhile(self, fn):
        while fn(self.peek()):
            yield next(self)

    def skipwhile(self, fn):
        while fn(self.peek()):
            next(self)

    def takeuntil(self, fn):
        return self.takewhile(lambda e: not fn(e))

    def skipuntil(self, fn):
        self.skipwhile(lambda e: not fn(e))

    def takethrough(self, pos):
        return self.takewhile(lambda _: self._pos < pos)

    def skipthrough(self, pos):
        self.skipwhile(lambda _: self._pos < pos)

    def taketo(self, pos):
        return self.takethrough(pos - 1)

    def skipto(self, pos):
        self.skipthrough(pos - 1)


class ProxyIterator(ta.Iterator[T]):

    def __init__(self, fn) -> None:
        self._fn = fn

    def __iter__(self) -> ta.Iterator[T]:
        return self

    def __next__(self) -> T:
        return self._fn()


class PrefetchIterator(ta.Iterator[T]):

    def __init__(self, fn: ta.Optional[ta.Callable[[], T]] = None) -> None:
        super().__init__()

        self._fn = fn
        self._deque: ta.Deque[T] = collections.deque()

    def __iter__(self) -> ta.Iterator[T]:
        return self

    def push(self, item) -> None:
        self._deque.append(item)

    def __next__(self) -> T:
        try:
            return self._deque.popleft()
        except IndexError:
            if self._fn is None:
                raise StopIteration
        return self._fn()


class RetainIterator(ta.Iterator[T]):

    def __init__(self, fn: ta.Callable[[], T]) -> None:
        super().__init__()

        self._fn = fn
        self._deque: ta.Deque[T] = collections.deque()

    def __iter__(self) -> ta.Iterator[T]:
        return self

    def pop(self) -> None:
        self._deque.popleft()

    def __next__(self) -> T:
        item = self._fn()
        self._deque.append(item)
        return item


def unzip(it: ta.Iterable[T], width: ta.Optional[int] = None) -> ta.List:
    if width is None:
        if not isinstance(it, PeekIterator):
            it = PeekIterator(iter(it))
        try:
            width = len(it.peek())
        except StopIteration:
            return []

    its: ta.List[PrefetchIterator[T]] = []

    def next_fn(idx):
        if not next_fn.running:
            raise StopIteration
        try:
            items = next(it)
        except StopIteration:
            next_fn.running = False
            raise
        for item_idx, item in enumerate(items):
            its[item_idx].push(item)
        return next(its[idx])

    next_fn.running = True  # type: ignore
    its.extend(PrefetchIterator(functools.partial(next_fn, idx)) for idx in range(width))
    return its
