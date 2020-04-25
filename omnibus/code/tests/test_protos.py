import sys

from .. import protos


def test_protos():
    assert isinstance(sys._getframe(1), protos.Frame)
    assert isinstance(sys._getframe(1).f_code, protos.Code)
    assert not isinstance('banana', protos.Frame)
    assert not isinstance('banana', protos.Code)
