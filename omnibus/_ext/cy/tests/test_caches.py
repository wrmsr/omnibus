def test_link():
    from .. import caches

    assert isinstance(repr(caches.CacheLink()), str)
