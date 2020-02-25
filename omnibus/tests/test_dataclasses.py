import collections
import pickle

import pytest

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


def test_meta():
    class Point(dc.Dataclass):
        x: int
        y: int

    pt = Point(1, 2)
    assert pt.x == 1
    pt.z = 2
    assert pt.z == 2

    class Iface(dc.Dataclass, abstract=True, sealed=True, pickle=True):
        x: int

    with pytest.raises(TypeError):
        Iface(1)

    class Impl(Iface, final=True):
        y: int

    pt = Impl(1, 2)
    assert pt.x == 1
    pt.z = 2
    assert pt.z == 2

    with pytest.raises(TypeError):
        class Iface(Impl):
            pass

    with pytest.raises(TypeError):
        class Impl2(Impl):
            pass


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


def test_implicit_abc():
    @dc.dataclass(frozen=True)
    class C:
        x: int

    assert issubclass(C, dc.VirtualClass)
    assert isinstance(C(1), dc.VirtualClass)

    assert not issubclass(int, dc.VirtualClass)
    assert not isinstance(1, dc.VirtualClass)


def test_validate():
    @dc.dataclass(frozen=True)
    class C:
        x: int = dc.field(validate=lambda x: x > 0)
        y: int

        dc.validate(lambda x, y: x > y)

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
