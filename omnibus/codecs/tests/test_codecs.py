from .. import compression as compression_
from .. import misc as misc_
from .. import objects as objects_
from .. import registries as registries_
from .. import simple as simple_
from .. import types as types_


def test_nop():
    assert simple_.nop().encode(1) == 1


def test_lines():
    c = misc_.lines()
    assert c.decode(c.encode(['a', 'b'])) == ['a', 'b']


def test_pickle():
    c = objects_.pickle()
    d0 = {'a': 'b'}
    buf = c.encode(d0)
    d1 = c.decode(buf)
    assert d0 == d1


def test_yaml():
    c = objects_.yaml()
    dct = {1: 2}
    assert isinstance(c.encode(dct), str)
    assert c.decode(c.encode(dct)) == dct


def test_cbor():
    c = objects_.cbor()
    dct = {1: 2}
    assert isinstance(c.encode(dct), bytes)
    assert c.decode(c.encode(dct)) == dct


def test_gzip():
    c = compression_.gzip()
    assert c.decode(c.encode(b'123')) == b'123'


def test_bz2():
    c = compression_.bz2()
    assert c.decode(c.encode(b'123')) == b'123'


def test_lzma():
    c = compression_.lzma()
    assert c.decode(c.encode(b'123')) == b'123'


def test_registries():
    assert issubclass(registries_.EXTENSION_REGISTRY['gz'], types_.Codec)

    gz_lines_codec = registries_.for_extension('lines.gz')
    assert isinstance(gz_lines_codec, types_.Codec)
