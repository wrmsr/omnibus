import pytest

from .. import functions as functions_


@pytest.mark.parametrize('nolock', [False, True])
def test_function(nolock):
    @functions_.function(**({'lock': None} if nolock else {}))
    def f(val):
        return 'default'

    assert f(()) == 'default'
    assert f(1) == 'default'
    assert f('1') == 'default'
    assert f(b'1') == 'default'

    @f.registering(int)  # noqa
    def _(val):
        return 'int'

    assert f(()) == 'default'
    assert f(1) == 'int'
    assert f('1') == 'default'
    assert f(b'1') == 'default'

    @f.registering(str, bytes)  # noqa
    def _(val):
        return 'str/bytes'

    assert f(()) == 'default'
    assert f(1) == 'int'
    assert f('1') == 'str/bytes'
    assert f(b'1') == 'str/bytes'

    @f.register
    def _(val: set):
        return 'set'

    assert f(set()) == 'set'

    class A:
        pass

    class B(A):
        pass

    @f.register
    def _(v: A):
        return 'A'

    assert f(A()) == 'A'
    assert f(B()) == 'A'

    @f.register
    def _(v: B):
        return 'B'

    assert f(A()) == 'A'
    assert f(B()) == 'B'
