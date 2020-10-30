import typing as ta

import pytest

from .. import annotations
from .. import nodal


class Annotation(annotations.Annotation):
    pass


class A(nodal.Nodal['A', Annotation]):
    pass


def test_nodal():
    class B(A):
        pass

    B()

    class C(A):
        al: ta.Sequence[A]

    C([])

    with pytest.raises(TypeError):
        class D(A):
            al: ta.AbstractSet[A]

        D(set())
