import pytest

from .. import classes as classes_
from .. import enums as enums_


def test_autoenum():
    class E(enums_.AutoEnum):
        A = ...
        B = ...
        C = ...

    assert E.B.name == 'B'
    assert E.B.value == 2

    class F(enums_.AutoEnum):
        class A:
            thing = 1

        @classes_.instance()
        class B:
            def __init__(self):
                self.thing = 2

            def f(self):
                return 3

    assert F.A.name == 'A'
    assert F.B.name == 'B'
    assert F.A.value.thing == 1
    assert F.B.value.thing == 2
    assert F.B.value.f() == 3


def test_valueenum():
    class E(enums_.ValueEnum):
        X = 0
        Y = 1
        Z = 2

    assert E.Y == 1
    assert len(E._by_name) == 3
    assert E._by_name['Y'] == 1

    assert len(E._by_value) == 3
    assert E._by_value[1] == 'Y'

    with pytest.raises(Exception):
        class F(enums_.ValueEnum, unique=True):
            X = 1
            Y = 1
