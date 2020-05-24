import os.path

import pytest


@pytest.mark.xfail()
def test_csv():
    from .. import csvloader

    with open(os.path.join(os.path.dirname(__file__), 'csvs', 'sales100.csv'), 'r') as f:
        buf = f.read()

    rows = csvloader.loads(buf.strip())
    assert len(rows) == 101
