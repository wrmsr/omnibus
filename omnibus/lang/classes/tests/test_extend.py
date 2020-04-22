import pytest

from .. import extend as extend_


def test_extension():
    class A:
        pass

    class _(extend_.Extension[A]):  # noqa
        def f(self):
            return 1

    assert A().f() == 1

    with pytest.raises(NameError):
        class _(extend_.Extension[A]):  # noqa
            def f(self):
                pass

    class C:
        def f(self):
            return 1

    assert C().f() == 1

    class D(C):
        pass

    assert D().f() == 1

    class _(extend_.Extension[D]):  # noqa
        def f(self):
            return super(D, self).f() + 1

    assert D().f() == 2


def test_mixin():
    class M0(extend_.Mixin):
        extend_.Mixin.capture()

        def f(self):
            return 1

    class C:
        M0()

    assert C().f() == 1

    class M1(extend_.Mixin):
        extend_.Mixin.capture()

        def f(self):
            return str(super().f())

    class D(C):
        M1()

    assert D().f() == '1'
