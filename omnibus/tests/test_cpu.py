import pytest

from .. import cpu as cpu_


@pytest.mark.ext
def test_cpu():
    assert cpu_.arch() is not None
