import pytest

from .. import properties


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


def test_method_registry_property():
    class C:
        fns = properties.method_registry()

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


def test_method_registry_dispatch():
    class A:
        fn = properties.method_registry(singledispatch=True)

        @fn.register(object)
        def fn_object(self, o):
            return 'object'

        @fn.register(int)
        def fn_int(self, o):
            return 'int'

    class B(A):

        @A.fn.register
        def fn_str(self, o: str):
            return 'Bstr'

    class C(A):

        @A.fn.register(str)
        def fn_str(self, o):
            return 'Cstr'

    class D(C):

        @A.fn.register(str)
        def fn_str(self, o):
            return 'Dstr'

        @A.fn.register
        def fn_float(self, o: float):
            return 'Dfloat'

    assert A().fn(6) == 'int'
    assert A().fn(6.) == 'object'
    assert A().fn('hi') == 'object'

    assert B().fn(6) == 'int'
    assert B().fn(6.) == 'object'
    assert B().fn('hi') == 'Bstr'

    assert C().fn(6) == 'int'
    assert C().fn(6.) == 'object'
    assert C().fn('hi') == 'Cstr'

    assert D().fn(6) == 'int'
    assert D().fn(6.) == 'Dfloat'
    assert D().fn('hi') == 'Dstr'


def test_method_registry_class():
    class A(properties.MethodRegistryClass):
        fn = properties.method_registry(singledispatch=True)

        def fn(self, o: object):  # noqa
            return 'object'

        def fn(self, o: int):  # noqa
            return 'int'

    class B(A):

        def fn(self, o: str):
            return 'str'

    assert A().fn(0) == 'int'
    assert A().fn('') == 'object'

    assert B().fn(0) == 'int'
    assert B().fn('') == 'str'
