import collections.abc
import concurrent.futures
import contextlib
import time
import typing as ta

import pytest

from .. import lang
from .. import toolz


def test_public():
    __all__ = []

    @lang.public
    def f():
        pass

    assert 'f' in __all__

    @lang.public_as('f2')
    def g():
        pass

    assert 'f2' in __all__


def test_protocol():
    class P(lang.Protocol):
        @lang.abstract
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

    with pytest.raises(lang.ProtocolException):
        @P
        class D:
            pass


def test_interface():
    class I0(lang.Interface):
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

    class I1(lang.Interface, I0):
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

    class B(A, lang.Final):
        pass

    B()

    with pytest.raises(lang.FinalException):
        class C(B):
            pass

    T = ta.TypeVar('T')

    class D(ta.Generic[T], lang.Final):
        pass

    D()
    D[int]

    with pytest.raises(lang.FinalException):
        class E(D[int]):
            pass


def test_sealed():
    class A(lang.Sealed):
        __module__ = 'a'

    class B(A):
        __module__ = 'a'

    with pytest.raises(lang.SealedException):
        class C(A):
            __module__ = 'c'

    class D(B):
        __module__ = 'd'


def test_extension():
    class A:
        pass

    class _(lang.Extension[A]):  # noqa
        def f(self):
            return 1

    assert A().f() == 1

    with pytest.raises(NameError):
        class _(lang.Extension[A]):  # noqa
            def f(self):
                pass

    class C:
        def f(self):
            return 1

    assert C().f() == 1

    class D(C):
        pass

    assert D().f() == 1

    class _(lang.Extension[D]):  # noqa
        def f(self):
            return super(D, self).f() + 1

    assert D().f() == 2


def test_override():
    class A:
        def f(self):
            pass

    class B(A):
        @lang.override
        def f(self):
            pass

    assert B().f() is None

    with pytest.raises(Exception):
        class C(A):
            @lang.override
            def g(self):
                pass

    with pytest.raises(Exception):
        class D:
            @lang.override
            def g(self):
                pass


def test_camelize():
    assert lang.camelize('some_class') == 'SomeClass'


def test_decamelize():
    assert lang.decamelize('Abc') == 'abc'
    assert lang.decamelize('AbcDef') == 'abc_def'
    assert lang.decamelize('AbcDefG') == 'abc_def_g'
    assert lang.decamelize('AbcDefGH') == 'abc_def_g_h'
    assert lang.decamelize('') == ''


def test_bits():
    assert lang.get_bit(3, 0b0100) == 0
    assert lang.get_bit(2, 0b0100) == 1
    assert lang.get_bits(1, 2, 0b0100) == 0b10
    assert lang.get_bits(1, 3, 0b0100) == 0b10
    assert lang.get_bits(0, 3, 0b0100) == 0b100
    assert lang.get_bits(1, 1, 0b0100) == 0
    assert lang.set_bit(2, 1, 0b01010) == 0b01110
    assert lang.set_bit(3, 0, 0b01010) == 0b00010
    assert lang.set_bits(1, 2, 0b11, 0b01010) == 0b01110
    assert lang.set_bits(1, 2, 0b10, 0b01010) == 0b01100


def test_manage_maybe_iterator():
    i = 0

    @contextlib.contextmanager
    def manager():
        nonlocal i
        i += 1
        yield

    assert lang.manage_maybe_iterator(manager, lambda: None) is None
    assert i == 1

    assert lang.manage_maybe_iterator(manager, lambda: []) == []
    assert i == 2

    it = lang.manage_maybe_iterator(manager, lambda: iter([]))
    assert isinstance(it, collections.abc.Iterator)
    assert i == 3
    assert list(it) == []
    assert i == 4

    it = lang.manage_maybe_iterator(manager, lambda: iter(range(3)))
    assert isinstance(it, collections.abc.Iterator)
    assert i == 5
    assert list(it) == [0, 1, 2]
    assert i == 6


def test_autoenum():
    class E(lang.AutoEnum):
        A = ...
        B = ...
        C = ...

    assert E.B.name == 'B'
    assert E.B.value == 2

    class F(lang.AutoEnum):
        class A:
            thing = 1

        @lang.singleton()
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
    class M0(lang.Mixin):
        lang.Mixin.capture()

        def f(self):
            return 1

    class C:
        M0()

    assert C().f() == 1

    class M1(lang.Mixin):
        lang.Mixin.capture()

        def f(self):
            return str(super().f())

    class D(C):
        M1()

    assert D().f() == '1'


def test_abstract():
    class C(lang.Abstract):
        pass

    class D(C):
        pass

    class E(D, lang.Abstract):
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
    class M(lang.Marker):
        pass

    with pytest.raises(lang.FinalException):
        class N(M):
            pass
    with pytest.raises(TypeError):
        M()


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
    C = lang.new_type('C', (object,), {'f': lambda self: 420})
    assert C().f() == 420


def test_access_forbidden():
    class C:
        f = lang.AccessForbiddenDescriptor()

    try:
        C.f
    except lang.AttrAccessForbiddenException as e:
        assert e.name == 'f'


def test_await_futures():
    def fn() -> float:
        time.sleep(.2)
        return time.time()

    tp: concurrent.futures.Executor
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as tp:
        futures = [tp.submit(fn) for _ in range(10)]
        assert not lang.await_futures(futures, tick_fn=iter([True, False]).__next__)
        assert lang.await_futures(futures)

    def pairs(l):
        return [set(p) for p in toolz.partition_all(2, l)]

    idxs = [t[0] for t in sorted(list(enumerate(futures)), key=lambda t: t[1].result())]
    assert pairs(idxs) == pairs(range(10))
