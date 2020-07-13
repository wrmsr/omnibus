import typing as ta

import pytest

from .. import generic as generic_


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
def test_generic():
    disp = generic_.GenericDispatcher()
    disp[ta.Dict[A, A]] = 'aa'
    disp[ta.Dict[A, B]] = 'ab'

    impl, manifest = disp.dispatch(ta.Dict[A, B])
    assert manifest.spec.erased_cls is dict
    assert manifest.spec.args[0].cls is A
    assert manifest.spec.args[1].cls is B

    impl, manifest = disp.dispatch(ta.Dict[C, B])
    assert manifest.spec.erased_cls is dict
    assert manifest.spec.args[0].cls is C
    assert manifest.spec.args[1].cls is B

    disp = generic_.GenericDispatcher()
    disp[ta.Dict[K, V]] = 'kv'

    impl, manifest = disp.dispatch(ta.Dict[A, B])
    assert manifest.spec.erased_cls is dict
    assert manifest[K] is A
    assert manifest[V] is B
    assert manifest.spec.args[0].cls is A
    assert manifest.spec.args[1].cls is B

    disp = generic_.GenericDispatcher()
    disp[int] = 'int'
    disp[ta.Optional[T]] = 'Optional[T}'

    impl, manifest = disp.dispatch(int)  # noqa
    impl, manifest = disp.dispatch(ta.Optional[int])  # noqa
