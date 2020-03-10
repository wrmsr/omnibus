from .. import registries

import pytest


def test_registries():
    reg0 = registries.DictRegistry()
    reg0[0] = 'zero'
    reg0[1] = 'one'
    assert reg0[0] == 'zero'
    assert reg0[1] == 'one'
    with pytest.raises(registries.NotRegisteredException):
        reg0[2]

    reg1 = registries.DictRegistry()
    reg1[1] = 'onex'
    reg1[2] = 'two'
    assert reg1[1] == 'onex'
    assert reg1[2] == 'two'
    with pytest.raises(registries.NotRegisteredException):
        reg1[3]

    foreg0 = registries.CompositeRegistry([reg0, reg1], registries.CompositeRegistry.FIRST_ONE)
    with pytest.raises(TypeError):
        foreg0[3] = 'three'
    assert foreg0[0] == 'zero'
    assert foreg0[1] == 'one'
    assert foreg0[2] == 'two'
    with pytest.raises(registries.NotRegisteredException):
        foreg0[3]

    foreg1 = registries.CompositeRegistry([reg1, reg0], registries.CompositeRegistry.FIRST_ONE)
    assert foreg1[0] == 'zero'
    assert foreg1[1] == 'onex'
    assert foreg1[2] == 'two'
    with pytest.raises(registries.NotRegisteredException):
        foreg1[3]

    with pytest.raises(registries.AmbiguouslyRegisteredException):
        registries.CompositeRegistry([reg0, reg1], registries.CompositeRegistry.ONLY_ONE)

    oreg0 = registries.DictRegistry()
    oreg0[0] = 'zero'
    oreg0[1] = 'one'
    oreg1 = registries.DictRegistry()
    oreg1[2] = 'two'
    oreg1[3] = 'three'
    ooreg = registries.CompositeRegistry([oreg0, oreg1], registries.CompositeRegistry.ONLY_ONE)
    assert ooreg[0] == 'zero'
    assert ooreg[1] == 'one'
    assert ooreg[2] == 'two'
    assert ooreg[3] == 'three'
    with pytest.raises(registries.NotRegisteredException):
        ooreg[4]

    dreg = registries.DictRegistry({'a': 'A', 'b': 'B'}, frozen=True)
    assert dreg['a'] == 'A'
    assert dreg['b'] == 'B'
    with pytest.raises(registries.NotRegisteredException):
        dreg['c']
    with pytest.raises(registries.FrozenRegistrationException):
        dreg['c'] = 'C'


def test_multi_registries():
    reg0 = registries.MultiDictRegistry()
    reg0[0] = {'zero'}
    reg0[1] = {'one'}
    assert reg0[0] == {'zero'}
    assert reg0[1] == {'one'}
    with pytest.raises(registries.NotRegisteredException):
        reg0[2]

    reg1 = registries.MultiDictRegistry()
    reg1[1] = {'onex'}
    reg1[2] = {'two'}
    assert reg1[1] == {'onex'}
    assert reg1[2] == {'two'}
    with pytest.raises(registries.NotRegisteredException):
        reg1[3]

    foreg0 = registries.CompositeMultiRegistry([reg0, reg1], registries.CompositeRegistry.FIRST_ONE)
    with pytest.raises(TypeError):
        foreg0[3] = {'three'}
    assert foreg0[0] == {'zero'}
    assert foreg0[1] == {'one'}
    assert foreg0[2] == {'two'}
    with pytest.raises(registries.NotRegisteredException):
        foreg0[3]

    foreg1 = registries.CompositeMultiRegistry([reg1, reg0], registries.CompositeRegistry.FIRST_ONE)
    assert foreg1[0] == {'zero'}
    assert foreg1[1] == {'onex'}
    assert foreg1[2] == {'two'}
    with pytest.raises(registries.NotRegisteredException):
        foreg1[3]

    foreg2 = registries.CompositeMultiRegistry([reg1, reg0], registries.CompositeMultiRegistry.MERGE)
    assert foreg2[0] == {'zero'}
    assert foreg2[1] == {'one', 'onex'}
    assert foreg2[2] == {'two'}
    with pytest.raises(registries.NotRegisteredException):
        foreg2[3]
