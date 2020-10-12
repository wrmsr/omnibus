import pytest

from ..docker.dev.pytest import DockerManager
from ..inject.dev import pytest as ptinj


@pytest.mark.xfail()
def test_redis(harness: ptinj.Harness):
    [(host, port)] = harness[DockerManager].get_container_tcp_endpoints([('redis', 6379)]).values()

    import redis
    r = redis.Redis(host=host, port=port, db=0)
    r.set('foo', 'bar')
    print(r.get('foo'))
