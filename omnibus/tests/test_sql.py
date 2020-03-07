import pytest
import sqlalchemy as sa
import sqlalchemy.pool

from .. import docker
from .. import lang
from .. import sql


def test_pymysql():
    assert sql.pymysql_render_statement(sa.select([1])) == 'SELECT 1'


@pytest.mark.xfail()
def test_docker_mysql():
    with docker.client_context() as client:
        eps = docker.get_container_tcp_endpoints(
            client,
            [('docker_omnibus-mysql-master_1', 3306)])

    [(host, port)] = eps.values()

    engine: sa.engine.Engine
    with lang.disposing(sa.create_engine(f'mysql+mysqlconnector://omnibus:omnibus@{host}:{port}')) as engine:
        with engine.connect() as conn:
            print(conn.scalar(sa.select([sa.func.version()])))


@pytest.mark.xfail()
def test_docker_postgres():
    with docker.client_context() as client:
        eps = docker.get_container_tcp_endpoints(
            client,
            [('docker_omnibus-postgres-master_1', 5432)])

    [(host, port)] = eps.values()

    engine: sa.engine.Engine
    with lang.disposing(sa.create_engine(f'postgresql+psycopg2://omnibus:omnibus@{host}:{port}')) as engine:
        with engine.connect() as conn:
            print(conn.scalar(sa.select([sa.func.version()])))


def test_sqlite():
    engine: sa.engine.Engine
    with lang.disposing(
            sa.create_engine(
                f'sqlite://',
                connect_args={'check_same_thread': False},
                poolclass=sa.pool.StaticPool,
            )
    ) as engine:
        with engine.connect() as conn:
            print(conn.scalar(sa.select([sa.func.sqlite_version()])))
