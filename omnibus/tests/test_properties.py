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

    assert D().vals['a'] == 'C.a'
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


def test_multi_registry_property():
    class C:
        vals = properties.multi_registry()

        vals.register('a')(0)
        vals.register('a')(1)
        vals.register('b')(2)

    class D(C):

        C.vals.register('a')(3)
        C.vals.register('b')(4)

    class E(C):

        C.vals.register('a')(5)
        C.vals.register('b')(6)

    class F(D, E):

        C.vals.register('a')(7)
        C.vals.register('b')(8)

    assert C().vals['a'] == {0, 1}
    assert C().vals['b'] == {2}

    assert D().vals['a'] == {0, 1, 3}
    assert D().vals['b'] == {2, 4}

    assert E().vals['a'] == {0, 1, 5}
    assert E().vals['b'] == {2, 6}

    assert F().vals['a'] == {0, 1, 3, 5, 7}
    assert F().vals['b'] == {2, 4, 6, 8}
