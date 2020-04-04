from ...cy import caches


def test_link():
    assert isinstance(repr(caches.LruCacheLink()), str)
