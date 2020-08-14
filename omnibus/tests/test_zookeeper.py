import pytest

from .. import docker


@pytest.mark.xfail()
def test_zookeeper():
    if docker.is_in_docker():
        (host, port) = 'omnibus-zookeeper', 2181

    else:
        with docker.client_context() as client:
            eps = docker.get_container_tcp_endpoints(
                client,
                [('docker_omnibus-zookeeper_1', 2181)])

        [(host, port)] = eps.values()

    from kazoo.client import KazooClient

    zk = KazooClient(hosts=f'{host}:{port}')
    zk.start()
    try:
        zk.ensure_path('/my/favorite')
        if zk.exists("/my/favorite"):
            zk.delete('/my/favorite/node')
        zk.create('/my/favorite/node', b'a value')
        data, stat = zk.get('/my/favorite')
        print('Version: %s, data: %s' % (stat.version, data.decode('utf-8')))
        children = zk.get_children('/my/favorite')
        print('There are %s children with names %s' % (len(children), children))
    finally:
        zk.stop()
