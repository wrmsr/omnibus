import pytest


@pytest.mark.xfail()
def test_link():
    from ...cy import caches

    assert isinstance(repr(caches.CacheLink()), str)
