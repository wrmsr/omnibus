import sqlalchemy as sa

from .. import sql


def test_pymysql():
    assert sql.pymysql_render_statement(sa.select([1])) == 'SELECT 1'
