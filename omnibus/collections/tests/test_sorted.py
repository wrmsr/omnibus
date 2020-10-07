import random

from .. import sorted as sorted_
from ...dev.pytest import skip_if_cant_import


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


@skip_if_cant_import('sortedcontainers')
def test_sortedcontainers():
    _test_sorteddict(sorted_.SortedContainersDict.new())


def test_sorted_list_dict():
    assert dict(sorted_.SkipListDict()) == {}
    assert dict(sorted_.SkipListDict({3: 4, 1: 2})) == {1: 2, 3: 4}
