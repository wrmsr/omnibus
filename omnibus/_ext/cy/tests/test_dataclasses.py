from .. import dataclasses as dc_


def test_descriptor():
    class D(dc_.Descriptor):
        pass

    class C:
        x = D('_x')

    c = C()
    c._x = 5
    assert c.x == 5
