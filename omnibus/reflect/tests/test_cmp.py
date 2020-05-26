import typing as ta

import pytest

from .. import cmp as cmp_
from .. import specs as specs_


class A:
    pass


class B:
    pass


class C(A):
    pass


class D(A):
    pass


class E(D):
    pass


@pytest.mark.xfail()
def test_is_subclass():
    def isc(sub, sup):
        return specs_.spec(sup).accept(cmp_.IsSubclassVisitor(specs_.spec(sub)))

    assert isc(int, int)
    assert isc(int, object)
    assert isc(int, ta.Any)
    assert not isc(object, int)
    assert isc(A, A)
    assert not isc(A, B)
    assert not isc(B, A)
    assert isc(C, A)
    assert not isc(A, C)
    assert isc(E, D)
    assert isc(E, A)
    assert not isc(D, E)

    assert isc(list, ta.List[ta.Any])
    assert isc(ta.List[ta.Any], ta.List[ta.Any])
    assert isc(ta.List[ta.Any], list)
    assert isc(ta.List[int], ta.List[ta.Any])
    assert not isc(ta.List[ta.Any], ta.List[int])
