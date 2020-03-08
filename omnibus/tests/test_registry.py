from .. import registries

import pytest


def test_registries():
    reg = registries.DictRegistry()
    reg[0] = 'zero'
    reg[1] = 'one'
    assert reg[0] == 'zero'
    assert reg[1] == 'one'
    with pytest.raises(registries.NotRegisteredException):
        reg[2]
