"""
https://github.com/craSH/socat/blob/c20699fced66696e243d785fdfcd2a94cf11e4cc/EXAMPLES
"""
import contextlib
import io
import os
import pty
import random
import subprocess
import sys
import time
import tty  # noqa

import pytest

from .. import popen


def test_wait():
    for _ in range(4):
        with contextlib.closing(popen.PopenSpawn(['cat'])) as p:
            for i in range(10):
                p.write(b'hi %d\r\n' % (i,))
            time.sleep(.5 + random.random())
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


@pytest.mark.skip()
def test_python():
    with contextlib.closing(popen.PopenSpawn([sys.executable])) as p:
        time.sleep(.5 + random.random())
        buf = b''
        while True:
            p.write(b'1\r\n')
            buf += p.read_nb(32)
            print(buf)
            time.sleep(.5 + random.random())


def test_telnet():
    sp = subprocess.Popen(   # noqa
        "socat tcp-l:7777,reuseaddr,fork system:'cat',nofork",
        shell=True,
    )
    try:
        with contextlib.closing(popen.PopenSpawn(['/usr/local/bin/telnet', 'localhost', '7777'])) as p:
            time.sleep(.5 + random.random())
            buf = b''
            for i in range(5):
                p.write(b'%d\r\n' % (i,))
                buf += p.read_nb(32)
                print(buf)
                time.sleep(.5 + random.random())
    finally:
        sp.kill()
        sp.wait(10.)


@pytest.mark.skip()
def test_pty():
    buf = io.BytesIO()

    def master_read(fd):
        data = os.read(fd, 1024)
        buf.write(data)
        return data

    def stdin_read(fd):
        return os.read(fd, 1024)

    pty.spawn(sys.executable, master_read, stdin_read)
