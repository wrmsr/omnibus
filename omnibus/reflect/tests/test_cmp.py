import typing as ta

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


def test_is_subclass():
    def isc(sub, sup):
        return specs_.spec(sup).accept(cmp_.IsSubclassVisitor(specs_.spec(sub)))

    assert isc(int, int)
    assert isc(int, object)
    assert isc(int, ta.Any)
