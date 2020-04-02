import collections.abc
import pickle
import random

import pytest

from .. import collections as collections_
from .. import frozen as frozen_
from .. import identity as identity_
from .. import ordered as ordered_
from .. import sorted as sorted_
from .. import unmodifiable as unmodifiable_
from .. import wrapped as wrapped_
from ...tests import helpers


def test_frozendict():
    frozen_.FrozenDict(x=1, y=2).set(x=10, z=20)
    pickle.loads(pickle.dumps(frozen_.FrozenDict(x=1, y=2).set(x=10, z=20)))


def test_skiplist():
    lst = sorted_.SkipList()

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


def _test_sorteddict(dct: sorted_.SortedMutableMapping):
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
    _test_sorteddict(sorted_.SkipListDict())


@helpers.skip_if_cant_import('sortedcontainers')
def test_sortedcontainers():
    _test_sorteddict(sorted_.SortedContainersDict.new())


def test_identity_hashable_set():
    hash(identity_.IdentityHashableSet({1, 2, 3}))


class Incomparable:

    def __eq__(self, other):
        raise TypeError


def test_identity_key_dict():
    x, y = Incomparable(), Incomparable()
    with pytest.raises(TypeError):
        {x: 0, y: 1}
    dct = identity_.IdentityKeyDict()
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
    st = identity_.IdentitySet()
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
    OSF = ordered_.OrderedFrozenSet
    s0 = OSF(range(3))
    assert list(s0) == [0, 1, 2]


def test_frozen_list():
    lst = frozen_.FrozenList([1, 2, 3])
    assert isinstance(lst, collections.abc.Sequence)
    assert lst + [4, 5] == [1, 2, 3, 4, 5]


def test_unmodifiable():
    l = unmodifiable_.UnmodifiableSequence([1, 2, 3])
    s = unmodifiable_.UnmodifiableSet({1, 2, 3})
    d = unmodifiable_.UnmodifiableMapping({1: 2, 3: 4})

    assert l == [1, 2, 3]
    assert s == {1, 2, 3}
    assert d == {1: 2, 3: 4}

    with pytest.raises(Exception):
        l[0] = 1
    with pytest.raises(Exception):
        s.add(4)
    with pytest.raises(Exception):
        d[5] = 6


def test_wrapped():
    l = []
    w = wrapped_.WrappedSequence(lambda x: x + 10, lambda x: x - 10, l)

    assert not w
    w.append(5)
    assert l == [15]
    assert w == [5]


def test_unify():
    l = [
        {1, 2},
        {1, 3},
        {4, 5},
        {5, 6},
        {7, 8},
    ]

    r = collections_.unify(l)

    x = [
        {1, 2, 3},
        {4, 5, 6},
        {7, 8},
    ]

    def munge(lst):
        return frozenset(map(frozenset, lst))

    assert munge(r) == munge(x)
