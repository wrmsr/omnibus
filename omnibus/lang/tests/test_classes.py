import typing as ta

import pytest

from .. import classes as classes_


def test_protocol():
    class P(classes_.Protocol):
        @classes_.abstract
        def f(self):
            raise NotImplementedError()

    class A:
        def f(self):
            pass

    class B:
        def g(self):
            pass

    assert issubclass(A, P)
    assert not issubclass(B, P)
    assert isinstance(A(), P)
    assert not isinstance(B(), P)

    @P
    class C:
        def f(self):
            pass

    with pytest.raises(classes_.ProtocolException):
        @P
        class D:
            pass


def test_interface():
    class I0(classes_.Interface):
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

    class I1(classes_.Interface, I0):
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

    class B(A, classes_.Final):
        pass

    B()

    with pytest.raises(classes_.FinalException):
        class C(B):
            pass

    T = ta.TypeVar('T')

    class D(ta.Generic[T], classes_.Final):
        pass

    D()
    D[int]

    with pytest.raises(classes_.FinalException):
        class E(D[int]):
            pass


def test_sealed():
    class A(classes_.Sealed):
        __module__ = 'a'

    class B(A):
        __module__ = 'a'

    with pytest.raises(classes_.SealedException):
        class C(A):
            __module__ = 'c'

    class D(B):
        __module__ = 'd'


def test_extension():
    class A:
        pass

    class _(classes_.Extension[A]):  # noqa
        def f(self):
            return 1

    assert A().f() == 1

    with pytest.raises(NameError):
        class _(classes_.Extension[A]):  # noqa
            def f(self):
                pass

    class C:
        def f(self):
            return 1

    assert C().f() == 1

    class D(C):
        pass

    assert D().f() == 1

    class _(classes_.Extension[D]):  # noqa
        def f(self):
            return super(D, self).f() + 1

    assert D().f() == 2


def test_override():
    class A:
        def f(self):
            pass

    class B(A):
        @classes_.override
        def f(self):
            pass

    assert B().f() is None

    with pytest.raises(Exception):
        class C(A):
            @classes_.override
            def g(self):
                pass

    with pytest.raises(Exception):
        class D:
            @classes_.override
            def g(self):
                pass


def test_mixin():
    class M0(classes_.Mixin):
        classes_.Mixin.capture()

        def f(self):
            return 1

    class C:
        M0()

    assert C().f() == 1

    class M1(classes_.Mixin):
        classes_.Mixin.capture()

        def f(self):
            return str(super().f())

    class D(C):
        M1()

    assert D().f() == '1'


def test_abstract():
    class C(classes_.Abstract):
        pass

    class D(C):
        pass

    class E(D, classes_.Abstract):
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
    class M(classes_.Marker):
        pass

    with pytest.raises(classes_.FinalException):
        class N(M):
            pass
    with pytest.raises(TypeError):
        M()

    assert repr(M) == '<M>'


def test_init_subclass():
    l = []

    class A:
        def __init_subclass__(cls):
            l.append((A, cls))
            super(A, cls).__init_subclass__()
    assert l == []

    class B(A):
        def __init_subclass__(cls):
            l.append((B, cls))
            super(B, cls).__init_subclass__()
    assert l == [(A, B)]
    l.clear()

    class C(B):
        def __init_subclass__(cls):
            l.append((C, cls))
            super(C, cls).__init_subclass__()
    assert l == [(B, C), (A, C)]


def test_access_forbidden():
    class C:
        f = classes_.AccessForbiddenDescriptor()

    try:
        C.f
    except classes_.AttrAccessForbiddenException as e:
        assert e.name == 'f'


def test_is_abstract():
    class A(classes_.Abstract):
        pass

    assert classes_.is_abstract(A)

    class B(A):
        pass

    assert not classes_.is_abstract(B)

    class C(classes_.Abstract):

        def __init_subclass__(cls, **kwargs):
            super().__init_subclass__(**kwargs)
            if cls.__name__ == 'D':
                assert classes_.is_abstract(cls)
            else:
                assert not classes_.is_abstract(cls)

    class D(C, classes_.Abstract):
        pass

    class E(D):
        pass


def test_inner():
    class A:

        def __init__(self, x):
            super().__init__()

            self.x = x

        class B(classes_.Inner['A']):

            def __init__(self, y):
                super().__init__()

                self.y = y
                self.xy = self._outer.x + y

    a = A(1)
    b = a.B(2)

    assert a.x == 1
    assert b.y == 2
    assert b._outer is a
    assert b.xy == 3
