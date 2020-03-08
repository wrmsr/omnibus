import typing as ta

import pytest

from .. import dispatch


K = ta.TypeVar('K')
V = ta.TypeVar('V')
T0 = ta.TypeVar('T0')
T1 = ta.TypeVar('T1')


def test_erasing_dispatch():
    disp = dispatch.ErasingDictDispatcher()
    disp[ta.Dict[K, V]] = 'dict'
    impl, manifest = disp[ta.Dict[int, str]]
    assert isinstance(manifest, dispatch.Manifest)


def test_dispatch():
    disp = dispatch.DefaultDispatcher()
    disp[ta.Dict[K, V]] = 'dict'
    impl, manifest = disp[ta.Dict[int, str]]
    assert isinstance(manifest, dispatch.Manifest)


@pytest.mark.parametrize('nolock', [False, True])
def test_function(nolock):
    @dispatch.function(nolock=nolock)
    def f(val):
        return 'default'

    assert f(()) == 'default'
    assert f(1) == 'default'
    assert f('1') == 'default'
    assert f(b'1') == 'default'

    @f.register(int)  # noqa
    def _(val):
        return 'int'

    assert f(()) == 'default'
    assert f(1) == 'int'
    assert f('1') == 'default'
    assert f(b'1') == 'default'

    @f.register(str, bytes)  # noqa
    def _(val):
        return 'str/bytes'

    assert f(()) == 'default'
    assert f(1) == 'int'
    assert f('1') == 'str/bytes'
    assert f(b'1') == 'str/bytes'


def test_registry_property():
    class A:
        fn = dispatch.registry_property()

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

    a = A()
    for _ in range(3):
        assert a.fn(6) == 'int'
        assert a.fn(6.) == 'object'
        assert a.fn('hi') == 'object'

    assert B().fn(6) == 'int'
    assert B().fn(6.) == 'object'
    assert B().fn('hi') == 'Bstr'

    assert C().fn(6) == 'int'
    assert C().fn(6.) == 'object'
    assert C().fn('hi') == 'Cstr'

    assert D().fn(6) == 'int'
    assert D().fn(6.) == 'Dfloat'
    assert D().fn('hi') == 'Dstr'


def test_registry_class():
    class A(dispatch.RegistryClass):
        fn = dispatch.registry_property()

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
