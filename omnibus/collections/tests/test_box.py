from .. import box as bx


def test_box():
    class StrBox(bx.Box[str]):
        pass

    assert StrBox('abc').value == 'abc'
