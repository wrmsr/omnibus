import collections.abc
import pickle

import pytest

from .. import frozen as frozen_


def test_frozendict():
    frozen_.FrozenDict(x=1, y=2).set(x=10, z=20)
    pickle.loads(pickle.dumps(frozen_.FrozenDict(x=1, y=2).set(x=10, z=20)))

    assert dict(frozen_.frozendict((x, x + 1) for x in range(3))) == {0: 1, 1: 2, 2: 3}
    dct = {frozen_.frozendict({0: 1}): 2, frozen_.frozendict({3: 4}): 5}
    assert dct[frozen_.frozendict({0: 1})] == 2
    assert dct[frozen_.frozendict({3: 4})] == 5
    with pytest.raises(KeyError):
        dct[frozen_.frozendict({0: 2})]  # noqa


def test_frozen_list():
    lst = frozen_.FrozenList([1, 2, 3])
    assert isinstance(lst, collections.abc.Sequence)
    assert lst + [4, 5] == [1, 2, 3, 4, 5]
    assert lst[0] == 1
    assert lst[0:2] == [1, 2]

    dct = {frozen_.frozenlist([0, 1]): 2, frozen_.frozenlist([3, 4]): 5}
    assert dct[frozen_.frozenlist([0, 1])] == 2
    assert dct[frozen_.frozenlist([3, 4])] == 5
    with pytest.raises(KeyError):
        dct[frozen_.frozenlist([0, 2])]  # noqa
