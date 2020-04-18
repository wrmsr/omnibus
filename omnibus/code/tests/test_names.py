import datetime

from .. import names as names_


def test_namegen():
    ng = names_.name_generator()
    assert ng() == '_0'
    assert ng() == '_1'
    assert ng('self') == '_self0'

    nsb = cg.NamespaceBuilder()
    now = datetime.datetime.now()
    assert nsb.add(0) == '_0'
    assert nsb.add(now) == '_1'
    assert dict(nsb) == {'_0': 0, '_1': now}
