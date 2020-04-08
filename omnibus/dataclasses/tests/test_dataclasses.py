import abc
import collections
import dataclasses as dc
import pickle  # noqa
import typing as ta

import pyrsistent
import pytest

from .. import api as api_
from .. import defdecls as defdecls_
from .. import metaclass as metaclass_
from .. import pickling as pickling_  # noqa
from .. import specs as specs_
from .. import types as types_
from .. import validation as validation_
from .. import virtual as virtual_
from ... import check


T = ta.TypeVar('T')


# def test_reorder():
#     @build_.dataclass()
#     class C:
#         x: int
#         y: int = 5
#
#     @build_.dataclass(reorder=True)
#     class D(C):
#         z: int
#
#     assert [f.name for f in api_.fields(D)] == ['x', 'z', 'y']


def test_defaultdict():
    @api_.dataclass()
    class C:
        d: dict

    c = C(collections.defaultdict(lambda: 3, {}))
    d = api_.asdict(c)
    assert isinstance(d['d'], collections.defaultdict)
    assert d['d']['a'] == 3


def test_meta():
    class Point(metaclass_.Data):
        x: int
        y: int

    pt = Point(1, 2)
    assert pt.x == 1
    pt.z = 2
    assert pt.z == 2

    class Iface(metaclass_.Data, abstract=True, sealed=True, pickle=True):
        x: int

    with pytest.raises(TypeError):
        Iface(1)

    class Impl(Iface, final=True):
        y: int

    pt = Impl(1, 2)
    assert pt.x == 1
    pt.y = 2
    assert pt.y == 2
    pt.z = 3
    assert pt.z == 3

    class FrozenIface(metaclass_.Data, abstract=True, sealed=True, pickle=True, frozen=True):
        x: int

    class FrozenImpl(FrozenIface, final=True, frozen=True):
        y: int

    pt = FrozenImpl(1, 2)
    assert pt.x == 1
    with pytest.raises(dc.FrozenInstanceError):
        pt.y = 2

    with pytest.raises(TypeError):
        class Iface(Impl):
            pass

    with pytest.raises(TypeError):
        class Impl2(Impl):
            pass

    class Abs(metaclass_.Data, abstract=True):
        x: int

        @abc.abstractproperty
        def y(self) -> int:
            raise NotImplementedError

    with pytest.raises(TypeError):
        Abs(1)

    class AbsImpl(Iface, final=True):
        y: int

    pt = AbsImpl(1, 2)
    assert pt.x == 1
    pt.z = 2
    assert pt.z == 2

    class AbsImpl2(Abs, final=True):
        pass

    with pytest.raises(TypeError):
        AbsImpl2(1)

    class Gen(metaclass_.Data, ta.Generic[T]):
        val: T

    assert Gen(1).val == 1


# @build_.dataclass(reorder=True)
# class A(pickling_.SimplePickle):
#     x: int
#     y: int
#     z: int = 0
#
#
# @build_.dataclass(reorder=True)
# class B(A):
#     a: int
#
#
# def test_pickle():
#     o0 = B(1, 2, 3, 4)
#     o1 = pickle.loads(pickle.dumps(o0))
#     assert o1 == o0


def test_implicit_abc():
    @api_.dataclass(frozen=True)
    class C0:
        x: int

    @dc.dataclass(frozen=True)
    class C1:
        x: int

    for C in [C0, C1]:
        assert issubclass(C, virtual_.VirtualClass)
        assert isinstance(C(1), virtual_.VirtualClass)

        assert not issubclass(int, virtual_.VirtualClass)
        assert not isinstance(1, virtual_.VirtualClass)


def test_validate():
    @api_.dataclass(frozen=True)
    class C:
        x: int = api_.field(validate=lambda x: x > 0)
        y: int

        defdecls_.validate(lambda x, y: x > y)

        # @dataclasses_.validate
        # @staticmethod
        # def _validate(x, y):
        #     if not (x > y):
        #         raise ValueError

    # assert C.__dataclass_validators__


def test_coerce():
    @api_.dataclass(frozen=True)
    class C:
        s: str = api_.field(coerce=str)


def test_derive():
    @api_.dataclass(frozen=True)
    class C:
        x: int
        y: int
        s: str = api_.field(derive=lambda x, y: str(x + y))


def test_pyrsistent():
    v = pyrsistent.pvector(range(6))
    v = v.set(3, 'a')
    assert list(v) == [0, 1, 2, 'a', 4, 5]
    v = v.mset(2, 'b', 4, 'c')
    assert list(v) == [0, 1, 'b', 'a', 'c', 5]
    e = v.evolver()
    e[0] = 'd'
    e[-1] = 'f'
    v = e.persistent()
    assert list(v) == ['d', 1, 'b', 'a', 'c', 'f']


def test_default_validation():
    @api_.dataclass()
    class Point:
        x: int
        xs: ta.Iterable[int]
        ys_by_x: ta.Mapping[int, float]
        s: str
        d: dict
        oi: ta.Optional[int]

    xfld = api_.fields_dict(Point)['x']
    xfv = validation_.build_default_field_validation(xfld)
    xfv(420)
    with pytest.raises(Exception):
        xfv(420.)

    xsfld = api_.fields_dict(Point)['xs']
    xsfv = validation_.build_default_field_validation(xsfld)
    xsfv([420])
    xsfv({420})
    xsfv(frozenset([420]))
    for v in [420, [420.]]:
        with pytest.raises(Exception):
            xsfv(v)

    ysbyxfld = api_.fields_dict(Point)['ys_by_x']
    ysbyxfv = validation_.build_default_field_validation(ysbyxfld)
    ysbyxfv({})
    ysbyxfv({420: 421.})
    for v in [{420: 420}, {420.: 420.}]:
        with pytest.raises(Exception):
            ysbyxfv(v)

    sfld = api_.fields_dict(Point)['s']
    sfv = validation_.build_default_field_validation(sfld)
    sfv('420')
    with pytest.raises(Exception):
        sfv(420)

    dfld = api_.fields_dict(Point)['d']
    dfv = validation_.build_default_field_validation(dfld)
    dfv({})
    dfv({1: 2})
    with pytest.raises(Exception):
        sfv(())

    oifld = api_.fields_dict(Point)['oi']
    oifv = validation_.build_default_field_validation(oifld)
    oifv(None)
    oifv(420)
    with pytest.raises(Exception):
        oifv(420.)


def test_spec():
    @api_.dataclass()
    class A:
        x: int
        y: int

        defdecls_.validate(lambda x, y: check.arg(x > y))

    @api_.dataclass()
    class B(A):
        z: int

        defdecls_.check_(lambda x, z: x > z)

    spec = specs_.get_spec(B)  # noqa

    A(2, 1)
    B(2, 1, 0)
    with pytest.raises(types_.CheckException):
        B(2, 1, 3)


def test_post_init():
    class Point(metaclass_.Data):
        x: int
        y: int

        defdecls_.post_init(lambda pt: l.append(pt))

    l = []
    Point(1, 2)
    Point(3, 4)
    assert len(l) == 2


def test_defdecls():
    @dc.dataclass()
    class Point:
        x: int
        y: int

        defdecls_.CheckerDefdcel.install(lambda x: x > 1)

    cdd = defdecls_.get_cls_defdecls(Point)  # noqa


def test_field_attrs():
    @api_.dataclass()
    class A:
        y: int
        x: int = 0

    @api_.dataclass(field_attrs=True)
    class B:
        y: int
        x: int = 0

    assert not hasattr(A, 'y')
    assert A.x == 0
    assert A(0).y == 0
    assert A(0).x == 0
    assert A(0, 1).y == 0
    assert A(0, 1).x == 1

    assert isinstance(B.y, dc.Field)
    assert B.y.name == 'y'
    assert isinstance(B.x, dc.Field)
    assert B.x.name == 'x'
    assert B(0).y == 0
    assert B(0).x == 0
    assert B(0, 1).y == 0
    assert B(0, 1).x == 1
