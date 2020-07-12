import typing as ta

import pytest

from .. import cmp as cmp_
from .. import specs as specs_


T = ta.TypeVar('T')
U = ta.TypeVar('U')
K = ta.TypeVar('K')
V = ta.TypeVar('V')


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
        return cmp_.issubclass_(specs_.spec(sub), specs_.spec(sup))

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
    assert isc(list, ta.Sequence[ta.Any])
    assert isc(ta.List[ta.Any], ta.List[ta.Any])
    assert isc(ta.List[ta.Any], ta.Sequence[ta.Any])
    assert isc(ta.List[ta.Any], list)
    assert isc(ta.List[int], ta.List[ta.Any])
    assert isc(ta.List[int], ta.Sequence[ta.Any])
    assert isc(ta.List[int], ta.Sequence[object])
    assert isc(ta.List[int], ta.Sequence[int])
    assert not isc(ta.List[ta.Any], ta.List[int])

    assert isc(ta.Dict[int, object], ta.Dict[object, object])
    assert isc(ta.Dict[object, int], ta.Dict[object, object])
    assert not isc(ta.Dict[int, object], ta.Dict[object, int])
    assert not isc(ta.Dict[object, int], ta.Dict[int, object])

    assert isc(ta.Dict[int, str], ta.Dict[K, V])
