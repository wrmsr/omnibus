import pytest

from .. import box as bx


def test_box():
    class StrBox(bx.Box[str]):
        pass

    assert StrBox('abc').value == 'abc'

    class A(bx.Box[str], abstract=True):
        pass

    with pytest.raises(TypeError):
        A('hi')

    class B(A):
        pass

    assert B('hi').value == 'hi'

    class C(A, final=True):
        pass

    assert C('hi').value == 'hi'

    with pytest.raises(TypeError):
        class D(C):  # noqa
            pass

    class V(bx.Box[str]):
        @classmethod
        def is_valid(cls, val: str) -> bool:
            return val[0] == 'a'

    assert V('ahi').value == 'ahi'
    with pytest.raises(ValueError):
        V('bhi')

    with pytest.raises(TypeError):
        class X(bx.Box[int]):
            def is_valid(self, val: int) -> bool:
                return True
