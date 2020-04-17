import pytest

from .. import unmodifiable as unmodifiable_


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
