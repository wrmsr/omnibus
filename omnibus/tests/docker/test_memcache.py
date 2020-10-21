import pytest

from ...docker.dev.pytest import DockerManager
from ...inject.dev import pytest as ptinj


@pytest.mark.xfail()
def test_memcache(harness: ptinj.Harness):
    [(host, port)] = harness[DockerManager].get_container_tcp_endpoints([('memcached', 11211)]).values()

    from pymemcache.client.base import Client
    client = Client((host, port))
    client.set('some_key', 'some_value')
    print(client.get('some_key'))
