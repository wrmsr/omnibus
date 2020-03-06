import typing as ta

import pytest

from .. import dispatch as dsp


K = ta.TypeVar('K')
V = ta.TypeVar('V')
T0 = ta.TypeVar('T0')
T1 = ta.TypeVar('T1')


def test_erasing_dispatch():
    disp = dsp.ErasingDictDispatcher()
    disp[ta.Dict[K, V]] = 'dict'
    impl, manifest = disp[ta.Dict[int, str]]
    assert isinstance(manifest, dsp.Manifest)


def test_dispatch():
    disp = dsp.DefaultDispatcher()
    disp[ta.Dict[K, V]] = 'dict'
    impl, manifest = disp[ta.Dict[int, str]]
    assert isinstance(manifest, dsp.Manifest)


@pytest.mark.parametrize('nolock', [False, True])
def test_function(nolock):
    @dsp.function(nolock=nolock)
    def f(val):
        return 'default'

    assert f(()) == 'default'
    assert f(1) == 'default'
    assert f('1') == 'default'
    assert f(b'1') == 'default'

    @f.register(int)  # noqa
    def _(val):
        return 'int'

    assert f(()) == 'default'
    assert f(1) == 'int'
    assert f('1') == 'default'
    assert f(b'1') == 'default'

    @f.register(str, bytes)  # noqa
    def _(val):
        return 'str/bytes'

    assert f(()) == 'default'
    assert f(1) == 'int'
    assert f('1') == 'str/bytes'
    assert f(b'1') == 'str/bytes'
