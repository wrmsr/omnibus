from .. import ordered as ordered_


def test_ordered_frozen_set():
    OSF = ordered_.OrderedFrozenSet
    s0 = OSF(range(3))
    assert list(s0) == [0, 1, 2]
