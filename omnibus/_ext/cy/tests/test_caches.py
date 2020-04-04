import pytest

from ...cy import caches


@pytest.mark.xfail()
def test_link():
    assert isinstance(repr(caches.LruCacheLink()), str)
