import abc
import collections
import dataclasses as dc
import pickle
import typing as ta

import pyrsistent
import pytest

from .. import api as api_
from .. import build as build_
from .. import metaclass as metaclass_
from .. import pickling as pickling_
from .. import specs as specs_
from .. import validation as validation_
from .. import virtual as virtual_
from ... import check
from ... import lang


T = ta.TypeVar('T')


def test_reorder():
    @build_.dataclass()
    class C:
        x: int
        y: int = 5

    @build_.dataclass(reorder=True)
    class D(C):
        z: int

    assert [f.name for f in api_.fields(D)] == ['x', 'z', 'y']


def test_defaultdict():
    @build_.dataclass()
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


@build_.dataclass(reorder=True)
class A(pickling_.SimplePickle):
    x: int
    y: int
    z: int = 0


@build_.dataclass(reorder=True)
class B(A):
    a: int


def test_pickle():
    o0 = B(1, 2, 3, 4)
    o1 = pickle.loads(pickle.dumps(o0))
    assert o1 == o0


def test_implicit_abc():
    @build_.dataclass(frozen=True)
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


@lang.cls_dct_fn()
def field_validate(cls_dct, field_validator):
    check.callable(field_validator)
    cls_dct.setdefault('__dataclass_field_validators__', []).append(field_validator)


@lang.cls_dct_fn()
def validate(cls_dct, validator):
    check.callable(validator)
    cls_dct.setdefault('__dataclass_validators__', []).append(validator)


def test_validate():
    @build_.dataclass(frozen=True)
    class C:
        x: int = api_.field(validate=lambda x: x > 0)
        y: int

        validate(lambda x, y: x > y)

        # @dataclasses_.validate
        # @staticmethod
        # def _validate(x, y):
        #     if not (x > y):
        #         raise ValueError

    assert C.__dataclass_validators__


def test_coerce():
    @build_.dataclass(frozen=True)
    class C:
        s: str = api_.field(coerce=str)


def test_derive():
    @build_.dataclass(frozen=True)
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
    @build_.dataclass()
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
    @build_.dataclass()
    class A:
        x: int
        y: int

        field_validate(lambda x, y: x > y)
        validate(lambda pt: pt.x > pt.y)

    @build_.dataclass()
    class B(A):
        z: int

        field_validate(lambda x, z: x > z)
        validate(lambda pt: pt.x > pt.z)

    spec = specs_.get_spec(B)
    print(spec.validators)
    print(spec.fields_validators)
    print(spec)
