import typing as ta

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
