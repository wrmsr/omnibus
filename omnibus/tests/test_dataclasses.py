import collections
import pickle

from .. import dataclasses as dc


def test_reorder():
    @dc.dataclass()
    class C:
        x: int
        y: int = 5

    @dc.dataclass(reorder=True)
    class D(C):
        z: int

    assert [f.name for f in dc.fields(D)] == ['x', 'z', 'y']


def test_defaultdict():
    @dc.dc_.dataclass()
    class C:
        d: dict

    c = C(collections.defaultdict(lambda: 3, {}))
    d = dc.asdict(c)
    assert isinstance(d['d'], collections.defaultdict)
    assert d['d']['a'] == 3


@dc.dataclass(reorder=True)
class A(dc.SimplePickle):
    x: int
    y: int
    z: int = 0


@dc.dataclass(reorder=True)
class B(A):
    a: int


def test_pickle():
    o0 = B(1, 2, 3, 4)
    o1 = pickle.loads(pickle.dumps(o0))
    assert o1 == o0
