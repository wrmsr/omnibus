import concurrent.futures
import contextlib
import functools
import time
import typing as ta


T = ta.TypeVar('T')


def sync_await(fn: ta.Callable[..., T], *args, **kwargs) -> T:
    async def gate():
        nonlocal ret
        ret = await fn(*args, **kwargs)
    ret = missing = object()
    cr = gate()
    with contextlib.closing(cr):
        try:
            cr.send(None)
        except StopIteration:
            pass
        if ret is missing or cr.cr_await is not None or cr.cr_running:
            raise TypeError('Not terminated')
    return ret


def sync_list(fn: ta.Callable[..., ta.AsyncIterator[T]], *args, **kwargs) -> ta.List[T]:
    async def inner():
        nonlocal lst
        lst = [v async for v in fn(*args, **kwargs)]
    lst = None
    sync_await(inner)
    if not isinstance(lst, list):
        raise TypeError(lst)
    return lst


async def async_list(fn: ta.Callable[..., ta.AsyncIterator[T]], *args, **kwargs) -> ta.List[T]:
    return [v async for v in fn(*args, **kwargs)]


class SyncableIterable(ta.Generic[T]):

    def __init__(self, obj) -> None:
        super().__init__()
        self._obj = obj

    def __iter__(self) -> ta.Iterator[T]:
        async def inner():
            async for i in self._obj:
                yield i
        return iter(sync_list(inner))

    def __aiter__(self) -> ta.AsyncIterator[T]:
        return self._obj.__aiter__()


def syncable_iterable(fn: ta.Callable[..., ta.AsyncIterator[T]]) -> ta.Callable[..., SyncableIterable[T]]:
    @functools.wraps(fn)
    def inner(*args, **kwargs):
        return SyncableIterable(fn(*args, **kwargs))
    return inner


def await_futures(
        futures: ta.Sequence[concurrent.futures.Future],
        *,
        timeout_s: ta.Union[int, float] = 60,
        timeout_exception: Exception = RuntimeError('Future timeout'),
        tick_interval: ta.Union[int, float] = 0.1,
        tick_fn: ta.Callable[..., bool] = lambda: True,
) -> bool:
    start = time.time()
    pos = 0
    while tick_fn():
        for pos in range(pos, len(futures)):
            if not futures[pos].done():
                break
        else:
            return True
        if time.time() >= (start + timeout_s):
            raise timeout_exception
        time.sleep(tick_interval)
    return False


class ImmediateExecutor(concurrent.futures.Executor):

    def submit(self, fn, *args, **kwargs):
        future = concurrent.futures.Future()
        try:
            result = fn(*args, **kwargs)
            future.set_result(result)
        except Exception as e:
            future.set_exception(e)
        return future
