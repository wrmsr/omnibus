import pytest

from .. import os as oos
from .. import procfs


@pytest.mark.skipif(not oos.LINUX, reason='requires linux')
def test_procfs():
    print(procfs.get_process_stats())
    print(procfs.get_process_chain())
    print(procfs.get_process_start_time())
    print(procfs.get_process_rss())
    print(list(procfs.get_process_maps()))
    print(procfs.get_process_range_pagemaps(0, 1000))
    print(list(procfs.get_process_pagemaps()))
