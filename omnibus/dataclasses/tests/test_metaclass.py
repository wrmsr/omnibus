import abc
import dataclasses as dc
import pickle  # noqa
import typing as ta

import pytest

from .. import api as api_
from .. import metaclass as metaclass_
from .. import pickling as pickling_  # noqa


T = ta.TypeVar('T')


def test_meta():
    class Point(metaclass_.Data):
        x: int
        y: int

    pt = Point(1, 2)
    assert pt.x == 1
    pt.z = 2
    assert pt.z == 2

    class Abs(metaclass_.Data, abstract=True):
        x: int

    with pytest.raises(TypeError):
        Abs(1)

    class NAbs(Abs):
        pass

    assert NAbs(2).x == 2

    class AbsV(metaclass_.Data, abstract=True):
        @abc.abstractproperty
        def value(self) -> int:
            raise NotImplementedError

        @abc.abstractmethod
        def f(self):
            raise NotImplementedError

    class ImplV(AbsV):
        value: int

        def f(self):
            return 2

    assert ImplV(3).value == 3

    class ImplVNoF(AbsV):
        value: int

    with pytest.raises(TypeError):
        ImplVNoF(4)

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

    with pytest.raises(TypeError):
        class AbsImpl2(Abs, final=True):
            pass

    class Gen(metaclass_.Data, ta.Generic[T]):
        val: T

    assert Gen(1).val == 1


def test_post_init():
    class Point(metaclass_.Data):
        x: int
        y: int

        api_.post_init(lambda pt: l.append(pt))

    l = []
    Point(1, 2)
    Point(3, 4)
    assert len(l) == 2


def test_generic():
    class Box(metaclass_.Data, ta.Generic[T]):
        value: T

    assert isinstance(Box(1), Box)
    # assert issubclass(Box[int], Box)

    class SubBox(Box):
        pass

    assert SubBox(1).value == 1

    class SubIntBox(Box[int]):
        pass

    assert SubIntBox(1).value == 1


def test_frozen():
    class Pt(metaclass_.Frozen):
        x: int
        y: int

    pt = Pt(1, 2)
    assert pt.x == 1
    assert pt.y == 2

    with pytest.raises(Exception):
        pt.x = 3

    class Pt2(Pt):
        z: int

    pt2 = Pt2(1, 2, 3)
    assert pt2.x == 1
    assert pt2.y == 2
    assert pt2.z == 3


def test_pure():
    class Pt(metaclass_.Pure):
        x: int
        y: int

    pt = Pt(1, 2)
    assert pt.x == 1
    assert pt.y == 2

    with pytest.raises(Exception):
        pt.x = 3

    with pytest.raises(Exception):
        class Pt2(Pt):
            pass


def test_enum():
    class E(metaclass_.Enum, sealed=True):
        x: int

    class E0(E):
        y: int

    class E1(E):
        z: int

    with pytest.raises(Exception):
        E(1)

    e0 = E0(0, 1)
    e1 = E1(1, 2)

    assert e0.x == 0
    assert e0.y == 1
    assert e1.x == 1
    assert e1.z == 2

    with pytest.raises(Exception):
        E2 = type('E2', (E,), {'__module__': 'barf'})  # noqa

    with pytest.raises(Exception):
        class E11(E1):
            pass

    class AE(metaclass_.Enum, sealed=True):
        x: int

        @abc.abstractmethod
        def f(self):
            raise NotImplementedError

    class AE0(AE):
        y: int

        def f(self):
            return '0'

    class AE1(AE):
        z: int

        def f(self):
            return '1'

    with pytest.raises(Exception):
        class AE2(AE):   # noqa
            z: int

    with pytest.raises(Exception):
        AE(1)

    ae0 = AE0(0, 1)
    ae1 = AE1(1, 2)

    assert ae0.x == 0
    assert ae0.y == 1
    assert ae0.f() == '0'
    assert ae1.x == 1
    assert ae1.z == 2
    assert ae1.f() == '1'
