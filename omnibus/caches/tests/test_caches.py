import gc

import pytest

from .. import descriptor as desc_
from .. import impl as impl_


def test_cache():
    c = impl_.new_cache(max_size=2)
    c[0] = 'foo0'
    assert c[0] == 'foo0'
    c[1] = 'foo1'
    assert c[1] == 'foo1'
    c[2] = 'foo2'
    assert c[2] == 'foo2'
    with pytest.raises(KeyError):
        c.__getitem__(0)
    assert c[2] == 'foo2'

    c = impl_.new_cache(max_size=2)
    c[0] = 'foo0'
    assert c[0] == 'foo0'
    c[1] = 'foo1'
    assert c[1] == 'foo1'
    assert c[0] == 'foo0'
    c[2] = 'foo2'
    assert c[2] == 'foo2'
    with pytest.raises(KeyError):
        c.__getitem__(1)
    assert c[0] == 'foo0'

    c[0] = 'foo4'
    assert c[0] == 'foo4'

    del c[0]
    with pytest.raises(KeyError):
        c.__getitem__(0)


def test_descriptor_static():
    hits = []

    @desc_.cache()
    def f(x):
        hits.append(x)
        return x + 1

    assert f(0) == 1
    assert hits == [0]
    assert f(0) == 1
    assert hits == [0]
    assert f(1) == 2
    assert hits == [0, 1]


def test_descriptor_instance():
    class C:
        def __init__(self):
            self.hits = []

        @desc_.cache()
        def f(self, x):
            self.hits.append(x)
            return x + 1

    c0 = C()
    c1 = C()

    assert c0.f(0) == 1
    assert c0.hits == [0]
    assert c0.f(0) == 1
    assert c0.hits == [0]
    assert c0.f(1) == 2
    assert c0.hits == [0, 1]
    assert c1.hits == []


def test_weak_keys():
    class K:
        pass
    k = K()
    c = impl_.new_cache(weak_keys=True)
    c[k] = 1
    assert c[k] == 1
    assert len(c) == 1
    del k
    gc.collect()
    assert len(c) == 0


def test_expirey():
    clock = 0
    c = impl_.new_cache(expire_after_write=2, clock=lambda: clock)
    c[0] = 'a'
    c[1] = 'b'
    clock = 1
    assert c[0] == 'a'
    clock = 3
    with pytest.raises(KeyError):
        c.__getitem__(0)


def test_lfu():
    c = impl_.new_cache()
    for i in range(10):
        c[i] = i
        for j in range(i):
            c[i]

    c = impl_.new_cache(max_size=5, eviction=impl_.CacheImpl.LFU)
    for i in range(5):
        c[i] = i
    for _ in range(2):
        for i in range(5):
            if i != 2:
                c[i]
    c[2]
    c[6] = 6
