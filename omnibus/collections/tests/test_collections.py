from .. import collections as collections_


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
