import typing as ta

import pytest
import sqlalchemy as sa
import sqlalchemy.sql.elements

from .. import caching as caching_
from .. import mysql as mysql_
from ... import dataclasses as dc
from ... import lang
from ...docker.dev.pytest import DockerManager
from ...inject.dev import pytest as ptinj
from .fixtures import sqlite_engine  # noqa


def test_pymysql():
    assert mysql_.pymysql_render_statement(sa.select([1])) == 'SELECT 1'


def test_docker_mysql(harness: ptinj.Harness):
    [(host, port)] = harness[DockerManager].get_container_tcp_endpoints([('mysql-master', 3306)]).values()

    engine: sa.engine.Engine
    with lang.disposing(sa.create_engine(f'mysql+mysqlconnector://omnibus:omnibus@{host}:{port}')) as engine:
        with engine.connect() as conn:
            print(list(conn.execute("show session status like 'Com_begin'")))
            print(conn.scalar(sa.select([sa.func.version()])))


@pytest.mark.no_ci
def test_docker_postgres(harness: ptinj.Harness):
    [(host, port)] = harness[DockerManager].get_container_tcp_endpoints([('postgres-master', 5432)]).values()

    engine: sa.engine.Engine
    with lang.disposing(sa.create_engine(f'postgresql+psycopg2://omnibus:omnibus@{host}:{port}')) as engine:
        with engine.connect() as conn:
            print(conn.scalar(sa.select([sa.func.version()])))


def test_sqlite(sqlite_engine: sa.engine.Engine):  # noqa
    with sqlite_engine.connect() as conn:
        print(conn.scalar(sa.select([sa.func.sqlite_version()])))


def test_caching(sqlite_engine):  # noqa
    @dc.dataclass(frozen=True)
    class Point:
        x: int
        y: int

    class PointParameterizer(caching_.Parameterizer[ta.Tuple, Point]):

        def key(self, value: Point) -> ta.Tuple:
            return (value.x, value.y)

        def parameterize(self, key: ta.Tuple) -> caching_.ParameterizedValue[Point]:
            x = sa.bindparam('x')
            y = sa.bindparam('y')

            return caching_.ParameterizedValue(
                Point(x, y),
                [x, y],
                [
                    lambda pt: {x: pt.x},
                    lambda pt: {y: pt.y},
                ]
            )

    def construct(
            point: Point,
            conn: sa.engine.Connection,
    ) -> ta.Tuple[sa.sql.Selectable, ta.Dict[sa.sql.elements.BindParameter, ta.Any]]:
        return sa.select([point.x + point.y]), {}

    qcc = caching_.QueryCompilationCache(PointParameterizer(), construct)

    with sqlite_engine.connect() as conn:
        for _ in range(3):
            assert list(qcc.execute(Point(1, 2), conn)) == [(3,)]
