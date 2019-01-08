from .. import revision


def test_revision():
    assert revision.get_revision() is None
