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
    m = next(cmp_._issubclass(specs_.spec(ta.Dict[int, str]), specs_.spec(ta.Dict[K, V])))
    assert m.vars[K].sub.cls is int
    assert m.vars[V].sub.cls is str

    assert isc(int, ta.Optional[int])
    assert not isc(ta.Optional[int], int)

    assert isc(int, ta.Union[int, str])
    assert not isc(list, ta.Union[int, str])
    assert not isc(ta.Union[int, str], int)

    assert not isc(object, ta.Union)
    assert not isc(ta.Union, object)

    assert isc(ta.Union, ta.Union)
    assert isc(ta.Union[int, str], ta.Union)
    assert isc(ta.Union[int, str], ta.Union[int, str])
    assert not isc(ta.Union, ta.Union[int, str])

    assert not isc(ta.Union, ta.Union[int, str])
    assert isc(ta.Union[int, str], ta.Union[int, str, list])
    assert not isc(ta.Union[int, str, list], ta.Union[int, str])

    assert isc(ta.Dict[int, int], ta.Dict[T, T])
    assert not isc(ta.Dict[int, object], ta.Dict[T, T])

    assert isc(ta.Dict[int, ta.Dict[int, int]], ta.Dict[T, ta.Dict[T, T]])
    assert not isc(ta.Dict[str, ta.Dict[int, int]], ta.Dict[T, ta.Dict[T, T]])
