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
