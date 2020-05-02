import os.path

from .. import parsing as parsing_
from .. import json as json_


def test_parsee():
    with open(os.path.join(os.path.dirname(__file__), 'examples/example2.json'), 'r') as f:
        buf = f.read()
    ret = parsing_.parse(buf)
    print(ret)


def test_codec():
    assert json_.codec().decode(json_.codec().encode({'a': 2})) == {'a': 2}
