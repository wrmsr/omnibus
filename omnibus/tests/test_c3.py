from .. import c3


def test_mro():
    class A:
        pass

    class B(A):
        pass

    class C(A):
        pass

    class D(B, C):
        pass

    assert c3.mro(D, []) == [D, B, C, A, object]
