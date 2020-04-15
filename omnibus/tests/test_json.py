from .. import json


def test_codec():
    assert json.codec().decode(json.codec().encode({'a': 2})) == {'a': 2}
