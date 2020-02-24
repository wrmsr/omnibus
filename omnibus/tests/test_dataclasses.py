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


def test_validate():
    @dc.dataclass(frozen=True)
    class C:
        x: int = dc.field(validate=lambda x: x > 0)
        y: int

        dc.valiadte(lambda x, y: x > y)

        @dc.validate
        @staticmethod
        def _validate(x, y):
            if not (x > y):
                raise ValueError


def test_coerce():
    @dc.dataclass(frozen=True)
    class C:
        s: str = dc.field(coerce=str)


def test_derive():
    @dc.dataclass(frozen=True)
    class C:
        x: int
        y: int
        s: str = dc.field(derive=lambda x, y: str(x + y))
