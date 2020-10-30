import array

import pytest

from .. import vmath as vmath_  # type: ignore
from ..... import arrays


@pytest.mark.xfail()
def test_add():
    t = arrays.INT_GLYPHS_BY_SIZE[4]
    l = 10
    a = array.array(t, list(range(l)))
    b = array.array(t, list(range(l, l * 2)))
    c = array.array(t, [0] * l)
    vmath_.add_int32(a, b, c, l)
    assert list(c) == [l + r for l, r in zip(a, b)]
