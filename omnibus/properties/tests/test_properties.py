from .. import caching as caching_
from .. import simple as simple_


def test_caching_property():
    count = 0

    class C:

        @caching_.cached
        def cached(self) -> str:
            nonlocal count
            count += 1
            return 'cached'

        @caching_.locked_cached
        def locked_cached(self) -> str:
            nonlocal count
            count += 1
            return 'locked_cached'

    c = C()

    for _ in range(2):
        assert c.cached == 'cached'
    assert count == 1

    for _ in range(2):
        assert c.locked_cached == 'locked_cached'
    assert count == 2


def test_caching_class_property():
    count = 0

    class C:

        @caching_.cached_class
        def cached(cls) -> str:
            nonlocal count
            count += 1
            return 'cached'

        @caching_.locked_cached_class
        def locked_cached(cls) -> str:
            nonlocal count
            count += 1
            return 'locked_cached'

    for _ in range(2):
        assert C.cached == 'cached'
    assert count == 1

    for _ in range(2):
        assert C.locked_cached == 'locked_cached'
    assert count == 2


def test_set_once_property():
    class A:
        value = simple_.set_once()

    a = A()
    try:
        a.value
    except ValueError:
        pass
    else:
        raise ValueError('Expected exception')
    a.value = 1
    assert a.value == 1


def test_unwrapping():
    class C:
        @caching_.cached
        @property
        def s(self) -> str:
            nonlocal i
            i += 1
            return 'barf'

    i = 0
    c = C()
    assert c.s == 'barf'
    assert i == 1
    assert c.s == 'barf'
    assert i == 1
