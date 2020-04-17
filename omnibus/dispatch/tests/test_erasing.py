import typing as ta

from .. import erasing as erasing_
from .. import types as types_


K = ta.TypeVar('K')
V = ta.TypeVar('V')


def test_erasing_dispatch():
    disp = erasing_.ErasingDispatcher()
    disp[ta.Dict[K, V]] = 'dict'
    impl, manifest = disp[ta.Dict[int, str]]
    assert isinstance(manifest, types_.Manifest)
    assert manifest.spec.erased_cls is dict
    assert manifest.spec.args[0].cls is int
    assert manifest.spec.args[1].cls is str
