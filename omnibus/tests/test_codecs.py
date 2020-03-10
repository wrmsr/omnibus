from .. import codecs as co


def test_nop():
    assert co.nop().encode(1) == 1


def test_lines():
    c = co.lines()
    assert c.decode(c.encode(['a', 'b'])) == ['a', 'b']


def test_pickle():
    c = co.pickle()
    d0 = {'a': 'b'}
    buf = c.encode(d0)
    d1 = c.decode(buf)
    assert d0 == d1


def test_gzip():
    c = co.gzip()
    assert c.decode(c.encode(b'123')) == b'123'


def test_registries():
    assert issubclass(co.EXTENSION_REGISTRY['gz'], co.Codec)
