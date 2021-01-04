from .. import ordered as ordered_


def test_ordered_set():
    os = ordered_.OrderedSet([1, 2])
    assert list(os) == [1, 2]
    os.add(1)
    assert list(os) == [1, 2]
    os.add(3)
    assert list(os) == [1, 2, 3]
    os.remove(2)
    assert list(os) == [1, 3]


def test_ordered_frozen_set():
    OSF = ordered_.OrderedFrozenSet
    s0 = OSF(range(3))
    assert list(s0) == [0, 1, 2]
