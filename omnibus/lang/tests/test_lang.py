import pickle

import pytest

from .. import lang as lang_


def test_new_type():
    C = lang_.new_type('C', (object,), {'f': lambda self: 420})
    assert C().f() == 420


def test_empty_map():
    ed = lang_.EmptyMap()
    assert len(ed) == 0
    with pytest.raises(KeyError):
        ed['x']
    buf = pickle.dumps(ed)
    ed2 = pickle.loads(buf)
    assert ed2 is ed


def test_simple_proxy():
    class WrappedInt(lang_.SimpleProxy):
        __wrapped_attrs__ = {'__add__'}

    assert WrappedInt(4) + 2 == 6

    class IncInt(lang_.SimpleProxy):

        def __add__(self, other):
            return self.__wrapped__.__add__(other + 1)

    assert IncInt(4) + 2 == 7


def test_peek():
    it = range(4)
    v, it = lang_.peek(it)
    assert v == 0
    assert list(it) == [0, 1, 2, 3]


def test_no_bool():
    @lang_.no_bool
    def f():
        return 1

    assert f() == 1
    assert bool(f())
    with pytest.raises(TypeError):
        bool(f)

    class C(lang_.NoBool):
        pass

    assert C
    with pytest.raises(TypeError):
        bool(C())
