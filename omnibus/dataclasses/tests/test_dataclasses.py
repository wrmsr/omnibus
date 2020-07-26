import collections
import dataclasses as dc
import pickle  # noqa
import typing as ta

import pytest

from .. import api as api_
from .. import pickling as pickling_  # noqa
from .. import process as process_
from .. import reflect as reflect_
from .. import types as types_
from .. import validation as validation_
from .. import virtual as virtual_
from ... import check
from ... import lang
from ... import properties
from ..process import dicts as dicts_
from ..process import init as init_
from ..process import persistent as persistent_
from ..process import storage as storage_
from ..process import tuples as tuples_


T = ta.TypeVar('T')


def test_reorder():
    @api_.dataclass()
    class C:
        x: int
        y: int = 5

    @api_.dataclass(reorder=True)
    class D(C):
        z: int

    assert [f.name for f in api_.fields(D)] == ['x', 'z', 'y']


def test_defaultdict():
    @api_.dataclass()
    class C:
        d: dict

    c = C(collections.defaultdict(lambda: 3, {}))
    d = api_.asdict(c)
    assert isinstance(d['d'], collections.defaultdict)
    assert d['d']['a'] == 3


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


def test_check():
    @api_.dataclass()
    class C:
        x: int = api_.field(check=lambda x: x > 2)

    C(3)
    with pytest.raises(Exception):
        C(2)


def test_validate():
    @api_.dataclass(frozen=True)
    class C:
        x: int = api_.field(validate=lambda x: x > 0)
        y: int

        api_.validate(lambda x, y: x > y)

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

        api_.validate(lambda x, y: check.arg(x > y))

    @api_.dataclass()
    class B(A):
        z: int

        api_.check_(lambda x, z: x > z)

    spec = reflect_.get_cls_spec(B)  # noqa

    A(2, 1)
    B(2, 1, 0)
    with pytest.raises(types_.CheckException):
        B(2, 1, 3)


def test_defdecls():
    @dc.dataclass()
    class Point:
        x: int
        y: int

        api_.check_(lambda x: x > 1)

    cdd = reflect_.get_cls_spec(Point)  # noqa


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


def test_property():
    @dc.dataclass()
    class C:
        x: int = 0

        @property
        def y(self) -> int:
            return self.x + 1

        z: ta.ClassVar[properties.SetOnceProperty[int]] = properties.set_once()

    c = C(1)
    assert c.y == 2
    c.z = 3
    assert c.z == 3
    with pytest.raises(Exception):
        c.z = 4


def test_exc():
    @dc.dataclass()
    class E1(Exception):
        x: int
        y: int

    e = E1(1, 2)
    assert e.args == (e.x, e.y) == (1, 2)

    # FIXME
    # e = E1(y=3, x=4)
    # assert e.args == (e.x, e.y) == (4, 3)


def test_frozen():
    @api_.dataclass(frozen=True)
    class C:
        x: int

    c = C(1)
    assert c.x == 1
    with pytest.raises(Exception):
        c.x = 2


def test_redaction():
    @api_.dataclass(frozen=True)
    class Db:
        username: str
        password: lang.Redacted[str]

    db = Db('u', lang.redact('p'))
    print(db)

    # FIXME:
    # db = Db('u', 'p')
    # assert isinstance(db.password, lang.Redacted)
    # print(db)


def test_dfac():
    @api_.dataclass(frozen=True)
    class C:
        dct: dict = dc.field(default_factory=dict)

    assert isinstance(C().dct, dict)


def test_iv():
    @dc.dataclass(frozen=True)
    class C:
        x: int
        iv: dc.InitVar[int]

        def __post_init__(self, iv):
            l.append(iv)

    l = []
    c = C(1, 2)
    assert c.x == 1
    assert l == [2]
    with pytest.raises(Exception):
        c.y

    @api_.dataclass(frozen=True)
    class C:
        x: int
        iv: dc.InitVar[int]

        def __post_init__(self, iv):
            l.append(iv)

    l = []
    c = C(1, 2)
    assert c.x == 1
    assert l == [2]
    with pytest.raises(Exception):
        c.y


def test_descriptor():
    # TODO: *must* have descrpitorless get/set if possible

    class Desc:

        def __init__(self, field: dc.Field, *, attr_field: bool = False) -> None:
            super().__init__()

            self._field = field
            self._attr_field = attr_field

        def __get__(self, instance, owner=None):
            pass

        def __set__(self, instance, value):
            pass

        def __delete__(self, instance):
            pass


def test_derive2():
    @api_.dataclass()
    class C:
        s: str
        sp: str = api_.field(derive=lambda s: s + '!')
        spp: str

        api_.derive('spp', lambda sp: sp + '!!')

    assert C('a', 'b', 'c').spp == 'c'
    # FIXME:
    # assert C('c').spp == 'c!!'


def test_cache_hash():
    l = []

    class I:
        def __init__(self, h):
            self.h = h

        def __hash__(self):
            nonlocal l
            l.append(self)
            return self.h

    @api_.dataclass(frozen=True)
    class A:
        i: I

    a = A(I(420))
    assert hash(a) == hash(a)
    assert l == [a.i, a.i]

    l.clear()

    @api_.dataclass(frozen=True, cache_hash=True)
    class B:
        i: I

    b = B(I(420))
    assert hash(b) == hash(b)
    assert l == [b.i]


class TestDicts:

    @property
    def aspects(self):
        da = []
        for a in process_.DEFAULT_ASPECTS:
            if issubclass(a, storage_.Storage):
                a = dicts_.DictStorage
            da.append(a)
        return da

    def test_dicts0(self):
        @api_.dataclass(aspects=self.aspects)
        class C:
            x: int
            y: int

        c = C(1, 2)
        assert c.x == 1
        assert c.y == 2
        c.y = 3
        assert c.y == 3

    def test_dicts1(self):
        @api_.dataclass(aspects=self.aspects, frozen=True)
        class C:
            x: int
            y: int

        c = C(1, 2)
        assert c.x == 1
        assert c.y == 2
        with pytest.raises(dc.FrozenInstanceError):
            c.y = 3

    def test_dicts2(self):
        @api_.dataclass(aspects=self.aspects, frozen=True, field_attrs=True)
        class C:
            x: int
            y: int

        c = C(1, 2)
        assert c.x == 1
        assert c.y == 2
        with pytest.raises(dc.FrozenInstanceError):
            c.y = 3
        assert isinstance(C.x, dc.Field)


@pytest.mark.skip('fixme')
class TestPersistent:

    @property
    def aspects(self):
        da = []
        for a in process_.DEFAULT_ASPECTS:
            if issubclass(a, storage_.Storage):
                a = persistent_.PersistentStorage
            da.append(a)
        return da

    def test_persistent(self):
        @api_.dataclass(frozen=True, aspects=self.aspects)
        class C:
            x: int
            y: int

        c = C(1, 2)
        assert c.x == 1
        assert c.y == 2


class TestTuples:

    @property
    def aspects(self):
        return process_.replace_aspects(process_.DEFAULT_ASPECTS, {
            init_.Init: tuples_.TupleInit,
            storage_.Storage: tuples_.TupleStorage,
        })

    def test_tuples(self):
        @api_.dataclass(frozen=True, aspects=self.aspects)
        class C(tuple):
            x: int
            y: int

        c = C(1, 2)
        assert c.x == 1
        assert c.y == 2


def test_kwonly():
    @api_.dataclass(frozen=True)
    class C:
        a: int
        b: int = api_.field(kwonly=True)

    with pytest.raises(Exception):
        C(0, 1)  # noqa

    c = C(0, b=1)
    assert c.a == 0
    assert c.b == 1


def test_kwonly2():
    @api_.dataclass(frozen=True)
    class C:
        a: int
        b: int = api_.field(default=1000, kwonly=True)
        c: int = 420

    c = C(0, 100)
    assert c.a == 0
    assert c.b == 1000
    assert c.c == 100

    with pytest.raises(Exception):
        C(0, 1, 2)  # noqa

    c = C(0, 110, b=1)
    assert c.a == 0
    assert c.b == 1
    assert c.c == 110


def test_allow_setattr():
    @api_.dataclass(frozen=True, allow_setattr=True)
    class C:
        a: int

    c = C(2)
    assert c.a == 2
    with pytest.raises(dc.FrozenInstanceError):
        c.a = 3
    with pytest.raises(dc.FrozenInstanceError):
        del c.a
    assert c.a == 2

    with pytest.raises(AttributeError):
        c.b  # noqa
    c.b = 3
    assert c.b == 3
    assert c.a == 2
    c.b = 4
    assert c.b == 4
    del c.b
    with pytest.raises(AttributeError):
        c.b  # noqa
