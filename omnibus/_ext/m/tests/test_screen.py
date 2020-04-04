import pytest


@pytest.mark.xfail()
def test_screen():
    from .. import screen

    assert isinstance(screen.backing_scale_factor(), float)
