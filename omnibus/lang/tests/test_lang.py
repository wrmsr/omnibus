import pickle

import pytest

from .. import lang as lang_


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


def test_new_type():
    C = lang_.new_type('C', (object,), {'f': lambda self: 420})
    assert C().f() == 420


def test_const():
    c = lang_.constant(4)
    assert c() == 4
    assert pickle.loads(pickle.dumps(c))() == 4


def test_empty_mmap():
    ed = lang_.EmptyMap()
    assert len(ed) == 0
    with pytest.raises(KeyError):
        ed['x']
    buf = pickle.dumps(ed)
    ed2 = pickle.loads(buf)
    assert ed2 is ed


def test_cmp():
    assert lang_.cmp('a', 'b') == -1
    assert lang_.cmp('b', 'b') == 0
    assert lang_.cmp('c', 'b') == 1


def test_recurse():
    assert lang_.recurse(lambda rec, i: i + (rec(i - 1) if i else 0), 5) == 5 + 4 + 3 + 2 + 1


def test_simple_proxy():
    class WrappedInt(lang_.SimpleProxy):
        __wrapped_attrs__ = {'__add__'}

    assert WrappedInt(4) + 2 == 6

    class IncInt(lang_.SimpleProxy):

        def __add__(self, other):
            return self.__wrapped__.__add__(other + 1)

    assert IncInt(4) + 2 == 7


def test_cached_nullary():
    c = 0

    @lang_.cached_nullary
    def f():
        nonlocal c
        c += 1
        return 'f'

    assert f() == 'f'
    assert c == 1
    assert f() == 'f'
    assert c == 1
    f.reset()
    assert f() == 'f'
    assert c == 2
    assert f() == 'f'
    assert c == 2

    class C:
        cv = 'C'

        def __init__(self, iv):
            super().__init__()
            self.iv = iv

        @lang_.cached_nullary
        @staticmethod
        def s():
            nonlocal c
            c += 1
            return 'C.s'

        @lang_.cached_nullary
        @classmethod
        def c(cls):
            nonlocal c
            c += 1
            return f'C.c({cls.cv})'

        @lang_.cached_nullary
        def i(self):
            nonlocal c
            c += 1
            return f'C.i({self.iv})'

    class D(C):
        cv = 'D'

    c = 0
    ci = C('c')
    di = D('d')

    assert C.s() == 'C.s'
    assert c == 1
    assert C.s() == 'C.s'
    assert c == 1
    assert D.s() == 'C.s'
    assert c == 1
    assert ci.s() == 'C.s'
    assert c == 1
    assert di.s() == 'C.s'
    assert c == 1

    c = 0

    assert C.c() == 'C.c(C)'
    assert c == 1
    assert C.c() == 'C.c(C)'
    assert c == 1
    assert ci.c() == 'C.c(C)'
    assert c == 1
    assert D.c() == 'C.c(D)'
    assert c == 2
    assert di.c() == 'C.c(D)'
    assert c == 2

    c = 0
    ci2 = C('c2')

    assert ci.i() == 'C.i(c)'
    assert c == 1
    assert ci.i() == 'C.i(c)'
    assert c == 1
    assert di.i() == 'C.i(d)'
    assert c == 2
    assert ci2.i() == 'C.i(c2)'
    assert c == 3
    assert ci2.i() == 'C.i(c2)'
    assert c == 3


def test_peek():
    it = range(4)
    v, it = lang_.peek(it)
    assert v == 0
    assert list(it) == [0, 1, 2, 3]
