import time
import uuid

import pytest


def timeit(fn, n=100_000):
    s = time.time()
    for _ in range(n):
        fn()
    e = time.time()
    return e - s


@pytest.mark.xfail()
def test_uuid():
    from .. import uuid as uuid_

    s = '37b96676-18ff-4642-b818-a5b0f85cceef'

    for i in range(1, 5):
        assert uuid.UUID(s, version=i) == uuid_.new(s, version=i)

    print(timeit(lambda: uuid.UUID(s)))
    print(timeit(lambda: uuid_.new(s)))
