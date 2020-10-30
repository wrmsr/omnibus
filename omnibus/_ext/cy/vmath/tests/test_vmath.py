import pytest

from .. import vmath as vmath_  # type: ignore


@pytest.mark.xfail()
def test_add():
    assert vmath_.add(1, 2) == 3
