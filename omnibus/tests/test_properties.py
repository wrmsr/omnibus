import pytest

from .. import properties


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
        fns = properties.registry(descriptor=True)

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

    assert C().fns['a']() == 0
    assert C().fns['b']() == 1
    with pytest.raises(KeyError):
        C().fns['c']()
    assert D().fns['b']() == 1
    assert D().fns['c']() == 2


# def test_registry_class():
#     class A(properties.RegistryClass):
#         fn = properties.registry()
#
#         def fn(self, o: object):  # noqa
#             return 'object'
#
#         def fn(self, o: int):  # noqa
#             return 'int'
#
#     class B(A):
#
#         def fn(self, o: str):
#             return 'str'
#
#     assert A().fn(0) == 'int'
#     assert A().fn('') == 'object'
#
#     assert B().fn(0) == 'int'
#     assert B().fn('') == 'str'
