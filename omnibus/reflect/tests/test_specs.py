import gc
import typing as ta
import weakref

from ... import caches
from .. import specs as specs_


T = ta.TypeVar('T')
T0, T1, T2, T3 = map(ta.TypeVar, ['T0', 'T1', 'T2', 'T3'])
K = ta.TypeVar('K')
V = ta.TypeVar('V')

gs = specs_.spec
gts = specs_.type_spec


def test_specs():
    ts = gts(int)
    assert ts.cls is int
    assert ts.erased_cls is int

    ts = gts(ta.Dict)
    assert ts.erased_cls is dict
    assert len(ts.bases) > 0
    assert len(ts.vars) > 0
    assert specs_.spec_has_placeholders(ts)

    ts = gts(ta.Dict[str, int])
    assert ts.erased_cls is dict
    assert len(ts.bases) > 0
    assert not specs_.spec_has_placeholders(ts)

    class A(ta.Dict[int, str]):
        pass

    ts = gts(A)
    assert ts.cls is A

    t = ta.Dict[ta.FrozenSet[K], ta.Set[V]]
    ts = gts(t)
    assert ts.cls is t

    ts = gts(ta.Tuple[int, str, ta.Dict[K, V]])
    assert ts.erased_cls is tuple

    nts = gs(ta.Optional[int])
    assert isinstance(nts, specs_.UnionSpec)
    assert all(isinstance(s, specs_.Spec) for s in nts)

    assert len(list(gs(int))) == 2

    class C(ta.Generic[T]):
        pass

    ts = gts(C)
    assert isinstance(ts, specs_.ExplicitParameterizedGenericTypeSpec)
    assert ts.args == [specs_.ANY]

    class D(ta.Generic[K, V]):
        pass

    ts = gts(D)
    assert isinstance(ts, specs_.ExplicitParameterizedGenericTypeSpec)
    assert ts.args == [specs_.ANY, specs_.ANY]

    ts = gts(D[int, str])
    assert isinstance(ts, specs_.ExplicitParameterizedGenericTypeSpec)
    assert ts.args == [gs(int), gs(str)]

    ts = gts(D[T, T][int])
    assert isinstance(ts, specs_.ExplicitParameterizedGenericTypeSpec)
    assert ts.args == [gs(int), gs(int)]


def test_weak_cache():
    cref = None
    stats0: caches.Cache.Stats = None
    stats1: caches.Cache.Stats = None
    stats2: caches.Cache.Stats = None

    def f():
        nonlocal cref, stats1

        class C:
            pass

        cref = weakref.ref(C)
        ts = gts(C)  # noqa
        stats1 = specs_.spec._static.stats
        del C
        return cref

    gc.collect()
    specs_.spec._static.reap()
    stats0 = specs_.spec._static.stats

    cref = f()

    gc.collect()
    specs_.spec._static.reap()
    stats2 = specs_.spec._static.stats

    # refs = list(gc.get_referrers(cref()))

    assert stats1.size == stats0.size + 1
    assert stats2.size == stats0.size


def test_var():
    assert gs(ta.TypeVar('T')).variance == specs_.Variance.INVARIANT
    assert gs(ta.TypeVar('T', covariant=True)).variance == specs_.Variance.COVARIANT
    assert gs(ta.TypeVar('T', contravariant=True)).variance == specs_.Variance.CONTRAVARIANT


def test_tc():
    class C(ta.Generic[T]):
        pass

    class D(C[T0]):
        pass

    class E(C[T1]):
        pass

    class F(D[T2], E[T3]):
        pass

    ts_c = gts(C)  # noqa
    ts_c_i: specs_.ParameterizedGenericTypeSpec = gts(C[int])  # noqa
    ts_c_s: specs_.ParameterizedGenericTypeSpec = gts(C[str])  # noqa
    ts_d = gts(D)  # noqa
    ts_d_i: specs_.ParameterizedGenericTypeSpec = gts(D[int])  # noqa
    ts_d_s: specs_.ParameterizedGenericTypeSpec = gts(D[str])  # noqa
    ts_e = gts(E)  # noqa
    ts_f = gts(F)  # noqa
    ts_f_is: specs_.ParameterizedGenericTypeSpec = gts(F[int, str])  # noqa
    ts_f_si: specs_.ParameterizedGenericTypeSpec = gts(F[str, int])  # noqa

    assert ts_c_i.vars[T] == gts(int)
    assert ts_c_s.vars[T] == gts(str)

    assert ts_f_is.bases == [gts(D[int]), gts(E[str])]
    assert ts_f_si.bases == [gts(D[str]), gts(E[int])]
