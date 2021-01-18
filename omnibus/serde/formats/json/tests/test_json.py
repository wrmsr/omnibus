import os.path

from .. import json as json_
from .. import parsing as parsing_
from .....dev.pytest import skip_if_cant_import


def test_parse():
    with open(os.path.join(os.path.dirname(__file__), 'examples/example2.json'), 'r') as f:
        buf = f.read()
    ret = parsing_.parse(buf)
    print(ret)


def test_codec():
    assert json_.codec().decode(json_.codec().encode({'a': 2})) == {'a': 2}


def _test_provider(p: json_.Provider) -> None:
    p.json.dumps(1, **p.pretty_kwargs)
    p.json.dumps(1, **p.compact_kwargs)


@skip_if_cant_import('ujson')
def test_lib_ujson():
    _test_provider(json_.UjsonProvider())


@skip_if_cant_import('orjson')
def test_lib_orjson():
    _test_provider(json_.OrjsonProvider())
