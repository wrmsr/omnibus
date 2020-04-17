from .. import compression as compression_


def test_gzip():
    c = compression_.gzip()
    assert c.decode(c.encode(b'123')) == b'123'


def test_bz2():
    c = compression_.bz2()
    assert c.decode(c.encode(b'123')) == b'123'


def test_lzma():
    c = compression_.lzma()
    assert c.decode(c.encode(b'123')) == b'123'
