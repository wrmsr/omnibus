import pytest
import sqlalchemy as sa

from ...inject.dev import pytest as ptinj
from ..dev.pytest.manager import SparkManager


@pytest.mark.no_ci
@pytest.mark.spark
def test_sql(harness: ptinj.Harness):
    # conn = hive.Connection(host='localhost', port=10000)
    # cur = conn.cursor()
    # print(list(cur.execute('select 1')))

    engine = sa.create_engine(harness[SparkManager].thrift_url)
    with engine.connect() as conn:
        print(list(conn.execute(sa.select([1]))))
