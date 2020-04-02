import collections.abc
import concurrent.futures
import contextlib
import time
import typing as ta

import pytest

from .. import asyncs as asyncs_
from .. import classes as classes_
from .. import contextmanagers as cms_
from .. import enums as enums_
from .. import lang as lang_
from .. import math as math_
from .. import maybes as maybes_
from .. import strings as strings_
from ... import toolz


def test_cls_dct():
    class C:
        assert lang_.is_possibly_cls_dct(locals())

    assert not lang_.is_possibly_cls_dct(locals())


def test_public():
    __all__ = []

    @lang_.public
    def f():
        pass

    assert 'f' in __all__

    @lang_.public_as('f2')
    def g():
        pass

    assert 'f2' in __all__


def test_protocol():
    class P(classes_.Protocol):
        @classes_.abstract
        def f(self):
            raise NotImplementedError()

    class A:
        def f(self):
            pass

    class B:
        def g(self):
            pass

    assert issubclass(A, P)
    assert not issubclass(B, P)
    assert isinstance(A(), P)
    assert not isinstance(B(), P)

    @P
    class C:
        def f(self):
            pass

    with pytest.raises(classes_.ProtocolException):
        @P
        class D:
            pass


def test_interface():
    class I0(classes_.Interface):
        def f(self):
            pass

    with pytest.raises(TypeError):
        I0()

    class C0(I0):
        pass

    with pytest.raises(TypeError):
        C0()

    class C1(I0):
        def f(self):
            pass

    C1().f()

    class I1(classes_.Interface, I0):
        def g(self):
            pass

    with pytest.raises(TypeError):
        I1()

    class C2(I1):
        pass

    with pytest.raises(TypeError):
        C2()

    class C3(I1):
        def f(self):
            pass

    with pytest.raises(TypeError):
        C3()

    class C4(I1):
        def f(self):
            pass

        def g(self):
            pass

    C4().f()

    class C5(C1, I1):
        def g(self):
            pass

    C5().g()


def test_final():
    class A:
        pass

    A()

    class B(A, classes_.Final):
        pass

    B()

    with pytest.raises(classes_.FinalException):
        class C(B):
            pass

    T = ta.TypeVar('T')

    class D(ta.Generic[T], classes_.Final):
        pass

    D()
    D[int]

    with pytest.raises(classes_.FinalException):
        class E(D[int]):
            pass


def test_sealed():
    class A(classes_.Sealed):
        __module__ = 'a'

    class B(A):
        __module__ = 'a'

    with pytest.raises(classes_.SealedException):
        class C(A):
            __module__ = 'c'

    class D(B):
        __module__ = 'd'


def test_extension():
    class A:
        pass

    class _(classes_.Extension[A]):  # noqa
        def f(self):
            return 1

    assert A().f() == 1

    with pytest.raises(NameError):
        class _(classes_.Extension[A]):  # noqa
            def f(self):
                pass

    class C:
        def f(self):
            return 1

    assert C().f() == 1

    class D(C):
        pass

    assert D().f() == 1

    class _(classes_.Extension[D]):  # noqa
        def f(self):
            return super(D, self).f() + 1

    assert D().f() == 2


def test_override():
    class A:
        def f(self):
            pass

    class B(A):
        @classes_.override
        def f(self):
            pass

    assert B().f() is None

    with pytest.raises(Exception):
        class C(A):
            @classes_.override
            def g(self):
                pass

    with pytest.raises(Exception):
        class D:
            @classes_.override
            def g(self):
                pass


def test_camelize():
    assert strings_.camelize('some_class') == 'SomeClass'


def test_decamelize():
    assert strings_.decamelize('Abc') == 'abc'
    assert strings_.decamelize('AbcDef') == 'abc_def'
    assert strings_.decamelize('AbcDefG') == 'abc_def_g'
    assert strings_.decamelize('AbcDefGH') == 'abc_def_g_h'
    assert strings_.decamelize('') == ''


def test_bits():
    assert math_.get_bit(3, 0b0100) == 0
    assert math_.get_bit(2, 0b0100) == 1
    assert math_.get_bits(1, 2, 0b0100) == 0b10
    assert math_.get_bits(1, 3, 0b0100) == 0b10
    assert math_.get_bits(0, 3, 0b0100) == 0b100
    assert math_.get_bits(1, 1, 0b0100) == 0
    assert math_.set_bit(2, 1, 0b01010) == 0b01110
    assert math_.set_bit(3, 0, 0b01010) == 0b00010
    assert math_.set_bits(1, 2, 0b11, 0b01010) == 0b01110
    assert math_.set_bits(1, 2, 0b10, 0b01010) == 0b01100


def test_manage_maybe_iterator():
    i = 0

    @contextlib.contextmanager
    def manager():
        nonlocal i
        i += 1
        yield

    assert cms_.manage_maybe_iterator(manager, lambda: None) is None
    assert i == 1

    assert cms_.manage_maybe_iterator(manager, lambda: []) == []
    assert i == 2

    it = cms_.manage_maybe_iterator(manager, lambda: iter([]))
    assert isinstance(it, collections.abc.Iterator)
    assert i == 3
    assert list(it) == []
    assert i == 4

    it = cms_.manage_maybe_iterator(manager, lambda: iter(range(3)))
    assert isinstance(it, collections.abc.Iterator)
    assert i == 5
    assert list(it) == [0, 1, 2]
    assert i == 6


def test_autoenum():
    class E(enums_.AutoEnum):
        A = ...
        B = ...
        C = ...

    assert E.B.name == 'B'
    assert E.B.value == 2

    class F(enums_.AutoEnum):
        class A:
            thing = 1

        @classes_.singleton()
        class B:
            def __init__(self):
                self.thing = 2

            def f(self):
                return 3

    assert F.A.name == 'A'
    assert F.B.name == 'B'
    assert F.A.value.thing == 1
    assert F.B.value.thing == 2
    assert F.B.value.f() == 3


def test_mixin():
    class M0(classes_.Mixin):
        classes_.Mixin.capture()

        def f(self):
            return 1

    class C:
        M0()

    assert C().f() == 1

    class M1(classes_.Mixin):
        classes_.Mixin.capture()

        def f(self):
            return str(super().f())

    class D(C):
        M1()

    assert D().f() == '1'


def test_abstract():
    class C(classes_.Abstract):
        pass

    class D(C):
        pass

    class E(D, classes_.Abstract):
        pass

    class F(E):
        pass

    with pytest.raises(TypeError):
        C()
    D()
    with pytest.raises(TypeError):
        E()
    F()


def test_marker():
    class M(classes_.Marker):
        pass

    with pytest.raises(classes_.FinalException):
        class N(M):
            pass
    with pytest.raises(TypeError):
        M()

    assert repr(M) == '<M>'


def test_init_subclass():
    l = []

    class A:
        def __init_subclass__(cls):
            l.append((A, cls))
            super(A, cls).__init_subclass__()
    assert l == []

    class B(A):
        def __init_subclass__(cls):
            l.append((B, cls))
            super(B, cls).__init_subclass__()
    assert l == [(A, B)]
    l.clear()

    class C(B):
        def __init_subclass__(cls):
            l.append((C, cls))
            super(C, cls).__init_subclass__()
    assert l == [(B, C), (A, C)]


def test_new_type():
    C = lang_.new_type('C', (object,), {'f': lambda self: 420})
    assert C().f() == 420


def test_access_forbidden():
    class C:
        f = classes_.AccessForbiddenDescriptor()

    try:
        C.f
    except classes_.AttrAccessForbiddenException as e:
        assert e.name == 'f'


def test_await_futures():
    def fn() -> float:
        time.sleep(.2)
        return time.time()

    tp: concurrent.futures.Executor
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as tp:
        futures = [tp.submit(fn) for _ in range(10)]
        assert not asyncs_.await_futures(futures, tick_fn=iter([True, False]).__next__)
        assert asyncs_.await_futures(futures)

    def pairs(l):
        return [set(p) for p in toolz.partition_all(2, l)]

    idxs = [t[0] for t in sorted(list(enumerate(futures)), key=lambda t: t[1].result())]
    assert pairs(idxs) == pairs(range(10))


def test_syncable_iterable():
    async def f():
        return 1

    @asyncs_.syncable_iterable
    async def g():
        yield await f()

    assert list(g()) == [1]


def test_exit_stacked():
    class A(cms_.ExitStacked):
        pass

    with A() as a:
        assert isinstance(a, A)
        assert isinstance(a._exit_stack, contextlib.ExitStack)

    class B(cms_.ExitStacked):

        def __enter__(self):
            return 'hi'

    with B() as b:
        assert b == 'hi'


def test_is_abstract():
    class A(classes_.Abstract):
        pass

    assert classes_.is_abstract(A)

    class B(A):
        pass

    assert not classes_.is_abstract(B)

    class C(classes_.Abstract):

        def __init_subclass__(cls, **kwargs):
            super().__init_subclass__(**kwargs)
            if cls.__name__ == 'D':
                assert classes_.is_abstract(cls)
            else:
                assert not classes_.is_abstract(cls)

    class D(C, classes_.Abstract):
        pass

    class E(D):
        pass


def test_context_wrapped():
    class CM:
        count = 0

        def __enter__(self):
            self.count += 1

        def __exit__(self, et, e, tb):
            pass

    cm = CM()

    @cms_.context_wrapped(cm)
    def f(x):
        return x + 1

    assert f(4) == 5
    assert cm.count == 1
    assert f(5) == 6
    assert cm.count == 2

    class C:
        def __init__(self):
            self.cm = CM()

        @cms_.context_wrapped('cm')
        def f(self, x):
            return x + 2

    for _ in range(2):
        c = C()
        assert c.f(6) == 8
        assert c.cm.count == 1

    gcm = CM()

    @cms_.context_wrapped(lambda x: gcm)
    def g(x):
        return x + 3

    assert g(10) == 13
    assert gcm.count == 1

    class D:
        @cms_.context_wrapped(lambda self, x: gcm)
        def g(self, x):
            return x + 3

    d = D()
    assert d.g(10) == 13
    assert gcm.count == 2


def test_maybe():
    assert maybes_.Maybe(1)
    assert not maybes_.Maybe.empty()
    assert maybes_.Maybe.empty() is maybes_.Maybe.empty()
    assert maybes_.Maybe('foo').value.endswith('o')
    assert next(iter(maybes_.Maybe('x'))).capitalize() == 'X'
    assert maybes_.Maybe(None)

    assert maybes_.Maybe(0) == maybes_.Maybe(0)
    assert not (maybes_.Maybe(0) != maybes_.Maybe(0))
    assert maybes_.Maybe(0) != maybes_.Maybe(1)

    assert maybes_.Maybe(0) != (0,)
    assert not (maybes_.Maybe(0) == (0,))

    assert maybes_.Maybe(0) < maybes_.Maybe(1)
    assert maybes_.Maybe(1) > maybes_.Maybe(0)

    assert maybes_.Maybe(3).map(lambda v: v + 1) == maybes_.Maybe(4)
    assert maybes_.Maybe.empty().map(lambda v: v + 1) is maybes_.Maybe.empty()


def test_delimited_escaping():
    de = strings_.DelimitedEscaping('.', '"', '\\')
    assert de.quote('abc') == 'abc'
    assert de.quote('a.bc') == '"a\\.bc"'

    parts = ['abc', 'de.f', 'g', 'f']
    delimited = de.delimit_many(parts)
    assert delimited == 'abc."de\\.f".g.f'

    undelimited = de.undelimit(delimited)
    assert undelimited == parts
