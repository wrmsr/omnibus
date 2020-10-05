import sqlalchemy as sa

from .. import tpch
from .fixtures import sqlite_engine  # noqa


def test_tpch(sqlite_engine):  # noqa
    conn: sa.engine.Connection
    with sqlite_engine.connect() as conn:
        tpch.Base.metadata.create_all(conn)

        conn.execute("insert into part (name) values ('testpart')")
        print(list(conn.execute('select * from part')))
