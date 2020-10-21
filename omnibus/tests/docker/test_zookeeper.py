import pytest

from ...docker.dev.pytest import DockerManager
from ...inject.dev import pytest as ptinj


@pytest.mark.xfail()
def test_zookeeper(harness: ptinj.Harness):
    [(host, port)] = harness[DockerManager].get_container_tcp_endpoints([('zookeeper', 2181)]).values()

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
