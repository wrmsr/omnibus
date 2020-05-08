from .. import cpu as cpu_


def test_cpu():
    assert cpu_.arch() is not None
