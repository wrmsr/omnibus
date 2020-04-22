import typing as ta

import pytest

from .. import restrict as restrict_


def test_interface():
    class I0(restrict_.Interface):
        def f(self):
            pass

    with pytest.raises(TypeError):
        I0()

    class C0(I0):
        pass

    with pytest.raises(TypeError):
        C0()

    class C1(I0):
        def f(self):
            pass

    C1().f()

    class I1(restrict_.Interface, I0):
        def g(self):
            pass

    with pytest.raises(TypeError):
        I1()

    class C2(I1):
        pass

    with pytest.raises(TypeError):
        C2()

    class C3(I1):
        def f(self):
            pass

    with pytest.raises(TypeError):
        C3()

    class C4(I1):
        def f(self):
            pass

        def g(self):
            pass

    C4().f()

    class C5(C1, I1):
        def g(self):
            pass

    C5().g()


def test_final():
    class A:
        pass

    A()

    class B(A, restrict_.Final):
        pass

    B()

    with pytest.raises(restrict_.FinalException):
        class C(B):
            pass

    T = ta.TypeVar('T')

    class D(ta.Generic[T], restrict_.Final):
        pass

    D()
    D[int]

    with pytest.raises(restrict_.FinalException):
        class E(D[int]):
            pass


def test_sealed():
    class A(restrict_.Sealed):
        __module__ = 'a'

    class B(A):
        __module__ = 'a'

    with pytest.raises(restrict_.SealedException):
        class C(A):
            __module__ = 'c'

    class D(B):
        __module__ = 'd'


def test_override():
    class A:
        def f(self):
            pass

    class B(A):
        @restrict_.override
        def f(self):
            pass

    assert B().f() is None

    with pytest.raises(Exception):
        class C(A):
            @restrict_.override
            def g(self):
                pass

    with pytest.raises(Exception):
        class D:
            @restrict_.override
            def g(self):
                pass


def test_abstract():
    class C(restrict_.Abstract):
        pass

    class D(C):
        pass

    class E(D, restrict_.Abstract):
        pass

    class F(E):
        pass

    with pytest.raises(TypeError):
        C()
    D()
    with pytest.raises(TypeError):
        E()
    F()


def test_marker():
    class M(restrict_.Marker):
        pass

    with pytest.raises(restrict_.FinalException):
        class N(M):
            pass
    with pytest.raises(TypeError):
        M()

    assert repr(M) == '<M>'


def test_access_forbidden():
    class C:
        f = restrict_.AccessForbiddenDescriptor()

    try:
        C.f
    except restrict_.AttrAccessForbiddenException as e:
        assert e.name == 'f'


def test_is_abstract():
    class A(restrict_.Abstract):
        pass

    assert restrict_.is_abstract(A)

    class B(A):
        pass

    assert not restrict_.is_abstract(B)

    class C(restrict_.Abstract):

        def __init_subclass__(cls, **kwargs):
            super().__init_subclass__(**kwargs)
            if cls.__name__ == 'D':
                assert restrict_.is_abstract(cls)
            else:
                assert not restrict_.is_abstract(cls)

    class D(C, restrict_.Abstract):
        pass

    class E(D):
        pass