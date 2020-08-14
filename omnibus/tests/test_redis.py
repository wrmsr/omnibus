import pytest

from .. import docker


@pytest.mark.xfail()
def test_redis():
    if docker.is_in_docker():
        (host, port) = 'omnibus-redis', 6379

    else:
        with docker.client_context() as client:
            eps = docker.get_container_tcp_endpoints(
                client,
                [('docker_omnibus-redis_1', 6379)])

        [(host, port)] = eps.values()

    import redis
    r = redis.Redis(host=host, port=port, db=0)
    r.set('foo', 'bar')
    print(r.get('foo'))
