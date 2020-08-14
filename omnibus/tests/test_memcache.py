import pytest

from .. import docker


@pytest.mark.xfail()
def test_memcache():
    if docker.is_in_docker():
        (host, port) = 'omnibus-memcached', 11211

    else:
        with docker.client_context() as client:
            eps = docker.get_container_tcp_endpoints(
                client,
                [('docker_omnibus-memcached_1', 11211)])

        [(host, port)] = eps.values()

    from pymemcache.client.base import Client
    client = Client((host, port))
    client.set('some_key', 'some_value')
    print(client.get('some_key'))
