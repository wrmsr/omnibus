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
    assert p.dumps(1, **p.pretty_kwargs) == '1'
    assert p.dumps(1, **p.compact_kwargs) == '1'
    assert p.dumpb(1) == b'1'
    assert p.loads('1') == 1
    assert p.loads(b'1') == 1
    assert p.loads(bytearray(b'1')) == 1


def test_lib_builtin():
    _test_provider(json_.BuiltinProvider())


@skip_if_cant_import('ujson')
def test_lib_ujson():
    _test_provider(json_.UjsonProvider())


@skip_if_cant_import('orjson')
def test_lib_orjson():
    _test_provider(json_.OrjsonProvider())
