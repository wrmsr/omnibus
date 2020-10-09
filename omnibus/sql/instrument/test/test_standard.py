import contextlib
import typing as ta
import urllib.parse

import sqlalchemy as sa

from .. import standard as std
from .... import lang
from ....inject.dev.pytest import harness as har
from ...tests.manager import DbManager
from ...util import transaction_context


def parse_tags(stmt: str) -> ta.Dict[str, str]:
    return {
        k: v
        for tag in stmt.partition('  --  ')[2].strip().split(' ')
        for k, _, v in [tag.strip().partition('=')]
    }


def test_query_tagging(harness: har.Harness, monkeypatch):
    import mysql.connector.connection
    import mysql.connector.cursor_cext

    cursorcls = mysql.connector.cursor_cext.CMySQLCursor
    cursorcls_execute_original = cursorcls.execute
    last_stmt = None

    def cursorcls_execute_patch(self, operation, params=None, multi=False):
        nonlocal last_stmt
        last_stmt = operation
        return cursorcls_execute_original(self, operation, params=params, multi=multi)

    monkeypatch.setattr(cursorcls, 'execute', cursorcls_execute_patch)

    url = harness[DbManager].mysql_url
    purl = urllib.parse.urlparse(url)
    url = urllib.parse.urlunparse(purl._replace(scheme='o_mysql+mysqlconnector'))

    with contextlib.ExitStack() as es:
        engine: sa.engine.Engine = es.enter_context(lang.disposing(sa.create_engine(
            url, instrumentations=[std.StandardInstrumentation()])))

        conn: sa.engine.Connection = es.enter_context(engine.connect())

        input_stmt = "select 'test_0'"
        assert conn.scalar(input_stmt) == 'test_0'
        assert last_stmt.startswith(input_stmt + '  --  ')
        tags = parse_tags(last_stmt)
        assert 'caller' in tags
        assert 'txn_seq' not in tags

        with transaction_context(conn):
            conn.scalar("select 'test_1'")
            tags = parse_tags(last_stmt)
            assert 'caller' in tags
            assert tags['txn_seq'] == '1'

            conn.scalar("select 'test_2'")
            tags = parse_tags(last_stmt)
            assert 'caller' in tags
            assert tags['txn_seq'] == '2'

        conn.scalar("select 'test_3'")
        tags = parse_tags(last_stmt)
        assert 'caller' in tags
        assert 'txn_seq' not in tags
