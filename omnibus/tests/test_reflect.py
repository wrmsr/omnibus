import collections.abc
import gc
import typing as ta
import weakref

from .. import caches
from .. import reflect as rfl


T = ta.TypeVar('T')
T0, T1, T2, T3 = map(ta.TypeVar, ['T0', 'T1', 'T2', 'T3'])
K = ta.TypeVar('K')
V = ta.TypeVar('V')

gs = rfl.get_spec
gts = rfl.get_type_spec


def test_is_new_type():
    assert rfl.is_new_type(ta.NewType('Barf', int))
    assert not rfl.is_new_type(5)


def test_generic_bases():
    assert rfl.generic_bases(ta.Dict[int, str]) == [object]

    class A:
        pass

    assert rfl.generic_bases(A) == [object]

    class B(ta.Generic[T], A):
        pass

    assert rfl.generic_bases(B) == [A]
    assert rfl.generic_bases(B[int]) == [A]

    class C:
        pass

    class D(B[str], C):
        pass

    assert rfl.generic_bases(D) == [B[str], C]


def test_specs():
    ts = gts(int)
    assert ts.cls is int
    assert ts.erased_cls is int

    ts = gts(ta.Dict)
    assert ts.erased_cls is dict
    assert len(ts.bases) > 0
    assert len(ts.vars) > 0
    assert rfl.spec_has_placeholders(ts)

    ts = gts(ta.Dict[str, int])
    assert ts.erased_cls is dict
    assert len(ts.bases) > 0
    assert not rfl.spec_has_placeholders(ts)

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
    assert isinstance(nts, rfl.UnionSpec)
    assert all(isinstance(s, rfl.Spec) for s in nts)

    assert len(list(gs(int))) == 2

    class C(ta.Generic[T]):
        pass

    ts = gts(C)
    assert isinstance(ts, rfl.ExplicitParameterizedGenericTypeSpec)
    assert ts.args == [rfl.ANY_SPEC]

    class D(ta.Generic[K, V]):
        pass

    ts = gts(D)
    assert isinstance(ts, rfl.ExplicitParameterizedGenericTypeSpec)
    assert ts.args == [rfl.ANY_SPEC, rfl.ANY_SPEC]

    ts = gts(D[int, str])
    assert isinstance(ts, rfl.ExplicitParameterizedGenericTypeSpec)
    assert ts.args == [gs(int), gs(str)]

    ts = gts(D[T, T][int])
    assert isinstance(ts, rfl.ExplicitParameterizedGenericTypeSpec)
    assert ts.args == [gs(int), gs(int)]


def test_weak_cache():
    cref = None
    stats0: caches.LruCache.Stats = None
    stats1: caches.LruCache.Stats = None
    stats2: caches.LruCache.Stats = None

    def f():
        nonlocal cref, stats1

        class C:
            pass

        cref = weakref.ref(C)
        ts = gts(C)  # noqa
        stats1 = rfl.get_spec._static.stats

    gc.collect()
    rfl.get_spec._static.reap()
    stats0 = rfl.get_spec._static.stats

    f()

    gc.collect()
    rfl.get_spec._static.reap()
    stats2 = rfl.get_spec._static.stats

    assert stats1.size == stats0.size + 1
    assert stats2.size == stats0.size


def test_instance_dependents():
    assert not rfl.is_instance_dependent(int)

    class A(type):
        def __instancecheck__(self, instance):
            return True

    class B(metaclass=A):
        pass

    assert isinstance(5, B)
    assert rfl.is_instance_dependent(B)

    class C:
        pass

    assert not rfl.is_instance_dependent(C)


def test_subclass_dependents():
    assert not rfl.is_dependent(int)
    assert not rfl.is_subclass_dependent(collections.abc.Mapping)
    assert rfl.is_abc_dependent(collections.abc.Mapping)

    class A(type):
        def __subclasscheck__(self, instance):
            return True

    class B(metaclass=A):
        pass

    assert issubclass(int, B)
    assert rfl.is_subclass_dependent(B)

    class C:
        pass

    assert not rfl.is_subclass_dependent(C)


def test_var():
    assert gs(ta.TypeVar('T')).variance == rfl.Variance.INVARIANT
    assert gs(ta.TypeVar('T', covariant=True)).variance == rfl.Variance.COVARIANT
    assert gs(ta.TypeVar('T', contravariant=True)).variance == rfl.Variance.CONTRAVARIANT


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
    ts_c_i: rfl.ParameterizedGenericTypeSpec = gts(C[int])  # noqa
    ts_c_s: rfl.ParameterizedGenericTypeSpec = gts(C[str])  # noqa
    ts_d = gts(D)  # noqa
    ts_d_i: rfl.ParameterizedGenericTypeSpec = gts(D[int])  # noqa
    ts_d_s: rfl.ParameterizedGenericTypeSpec = gts(D[str])  # noqa
    ts_e = gts(E)  # noqa
    ts_f = gts(F)  # noqa
    ts_f_is: rfl.ParameterizedGenericTypeSpec = gts(F[int, str])  # noqa
    ts_f_si: rfl.ParameterizedGenericTypeSpec = gts(F[str, int])  # noqa

    assert ts_c_i.vars[T] == gts(int)
    assert ts_c_s.vars[T] == gts(str)

    assert ts_f_is.bases == [gts(D[int]), gts(E[str])]
    assert ts_f_si.bases == [gts(D[str]), gts(E[int])]
