import collections.abc
import pickle

from .. import frozen as frozen_


def test_frozendict():
    frozen_.FrozenDict(x=1, y=2).set(x=10, z=20)
    pickle.loads(pickle.dumps(frozen_.FrozenDict(x=1, y=2).set(x=10, z=20)))


def test_frozen_list():
    lst = frozen_.FrozenList([1, 2, 3])
    assert isinstance(lst, collections.abc.Sequence)
    assert lst + [4, 5] == [1, 2, 3, 4, 5]
