import pytest

from .. import properties
from .. import registries


def test_cached_property():
    count = 0

    class C:

        @properties.cached
        def cached(self):
            nonlocal count
            count += 1
            return 'cached'

        @properties.locked_cached
        def locked_cached(self):
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


def test_set_once_property():
    class A:
        value = properties.set_once()

    a = A()
    try:
        a.value
    except ValueError:
        pass
    else:
        raise ValueError('Expected exception')
    a.value = 1
    assert a.value == 1


def test_registry_property():
    class C:
        vals = properties.registry()

        vals.register('a')('C.a')
        vals.register('b')('C.b')

    class D(C):

        C.vals.register('c')('D.c')

    class E(D):

        D.vals.register('a')('E.a')

    assert C().vals['a'] == 'C.a'
    assert C().vals['b'] == 'C.b'
    with pytest.raises(registries.NotRegisteredException):
        C().vals['c']
    assert D().vals['a'] == 'C.b'
    assert D().vals['b'] == 'C.b'
    assert D().vals['c'] == 'D.c'
    assert E().vals['c'] == 'D.c'
    assert E().vals['a'] == 'E.a'


def test_binding_registry_property():
    class C:
        fns = properties.registry(bind=True)

        @fns.register('a')
        def _a(self):
            return 0

        @fns.register('b')
        def _b(self):
            return 1

    class D(C):

        @C.fns.register('c')
        def _c(self):
            return 2

    class E(D):

        @D.fns.register('a')
        def _a4(self):
            return 4

    assert C().fns['a']() == 0
    assert C().fns['b']() == 1
    with pytest.raises(registries.NotRegisteredException):
        C().fns['c']()
    assert D().fns['a']() == 0
    assert D().fns['b']() == 1
    assert D().fns['c']() == 2
    assert E().fns['c']() == 2
    assert E().fns['a']() == 4
