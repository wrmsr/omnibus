import pytest
import sqlalchemy as sa

from .. import docker
from .. import sql


def test_pymysql():
    assert sql.pymysql_render_statement(sa.select([1])) == 'SELECT 1'


@pytest.mark.xfail()
def test_docker_mysql():
    with docker.client_context() as client:
        eps = docker.get_container_tcp_endpoints(
            client,
            [('docker_omnibus-mysql-master_1', 3306)])

    print(eps)
