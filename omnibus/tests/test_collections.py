import pickle
import random

import pytest

from . import helpers
from .. import collections as col


def test_frozendict():
    col.FrozenDict(x=1, y=2).set(x=10, z=20)
    pickle.loads(pickle.dumps(col.FrozenDict(x=1, y=2).set(x=10, z=20)))


def test_skiplist():
    lst = col.SkipList()

    nums = list(range(100))
    random.shuffle(nums, random=random.Random(42).random)
    for i in nums:
        lst.add(i)

    assert lst.find(42) == 42
    assert lst.find(100) is None
    assert list(lst.iter()) == list(range(100))
    assert list(lst.riter()) == list(reversed(range(100)))

    lst.remove(42)

    assert lst.find(41) == 41
    assert lst.find(42) is None
    assert lst.find(43) == 43
    no42 = list(sorted(set(range(100)) - {42}))
    assert list(lst.iter()) == list(no42)
    assert list(lst.riter()) == list(reversed(no42))


def _test_sorteddict(dct: col.SortedMutableMapping):
    dct[4] = 'd'
    dct[2] = 'b'
    dct[5] = 'e'

    assert dct[2] == 'b'
    assert list(dct) == [2, 4, 5]
    assert list(dct.items()) == [(2, 'b'), (4, 'd'), (5, 'e')]
    assert list(dct.ritems()) == [(5, 'e'), (4, 'd'), (2, 'b')]

    assert list(dct.itemsfrom(3.9)) == [(4, 'd'), (5, 'e')]
    assert list(dct.itemsfrom(4)) == [(4, 'd'), (5, 'e')]
    assert list(dct.itemsfrom(4.1)) == [(5, 'e')]

    assert list(dct.ritemsfrom(4.1)) == [(4, 'd'), (2, 'b')]
    assert list(dct.ritemsfrom(4)) == [(4, 'd'), (2, 'b')]
    assert list(dct.ritemsfrom(3.9)) == [(2, 'b')]


def test_skiplistdict():
    _test_sorteddict(col.SkipListDict())


@helpers.skip_if_cant_import('bintrees')
def test_bintrees():
    _test_sorteddict(col.BintreesDict.new())


@helpers.skip_if_cant_import('sortedcontainers')
def test_sortedcontainers():
    _test_sorteddict(col.SortedContainersDict.new())


def test_identity_hashable_set():
    hash(col.IdentityHashableSet({1, 2, 3}))


class Incomparable:

    def __eq__(self, other):
        raise TypeError


def test_identity_key_dict():
    x, y = Incomparable(), Incomparable()
    with pytest.raises(TypeError):
        {x: 0, y: 1}
    dct = col.IdentityKeyDict()
    with pytest.raises(KeyError):
        dct[x]
    dct[x] = 4
    dct[y] = 5
    assert dct[x] == 4
    assert dct[y] == 5
    dct[x] = 6
    assert dct[x] == 6
    assert dct[y] == 5
    assert list(dct)[0] is x
    assert list(dct)[1] is y
    del dct[y]
    with pytest.raises(KeyError):
        dct[y]
    assert dct[x] == 6


def test_identity_key_set():
    x, y = Incomparable(), Incomparable()
    with pytest.raises(TypeError):
        {x, y}
    st = col.IdentitySet()
    assert len(st) == 0
    st.add(x)
    assert len(st) == 1
    assert x in st
    assert y not in st
    st.add(y)
    assert len(st) == 2
    assert x in st
    assert y in st
    st.remove(x)
    assert x not in st
    assert y in st


def test_ordered_frozen_set():
    OSF = col.OrderedFrozenSet
    s0 = OSF(range(3))
    assert list(s0) == [0, 1, 2]
