import concurrent.futures
import time

from .. import asyncs as asyncs_
from ... import toolz


def test_await_futures():
    def fn() -> float:
        time.sleep(.2)
        return time.time()

    tp: concurrent.futures.Executor
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as tp:
        futures = [tp.submit(fn) for _ in range(10)]
        assert not asyncs_.await_futures(futures, tick_fn=iter([True, False]).__next__)
        assert asyncs_.await_futures(futures)

    def pairs(l):
        return [set(p) for p in toolz.partition_all(2, l)]

    idxs = [t[0] for t in sorted(list(enumerate(futures)), key=lambda t: t[1].result())]
    assert pairs(idxs) == pairs(range(10))


def test_syncable_iterable():
    async def f():
        return 1

    @asyncs_.syncable_iterable
    async def g():
        yield await f()

    assert list(g()) == [1]
