import contextlib
import random
import time

from .. import popen


def test_wait():
    for _ in range(4):
        with contextlib.closing(popen.PopenSpawn(['cat'])) as p:
            for i in range(10):
                p.write(b'hi %d\r\n' % (i,))
            time.sleep(random.random())
            l = []
            for i in range(25):
                l.append(p.read_nb(4))
            assert l == [
                b'hi 0',
                b'\r\nhi',
                b' 1\r\n',
                b'hi 2',
                b'\r\nhi',
                b' 3\r\n',
                b'hi 4',
                b'\r\nhi',
                b' 5\r\n',
                b'hi 6',
                b'\r\nhi',
                b' 7\r\n',
                b'hi 8',
                b'\r\nhi',
                b' 9\r\n',
                b'',
                b'',
                b'',
                b'',
                b'',
                b'',
                b'',
                b'',
                b'',
                b'',
            ]
            p.write_eof()


def test_close():
    with contextlib.closing(popen.PopenSpawn(['cat'])) as p:  # noqa
        for i in range(10):
            p.write(b'hi %d\r\n' % (i,))
