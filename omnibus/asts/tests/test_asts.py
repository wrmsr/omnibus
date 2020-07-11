import contextlib
import glob
import os.path
import time

import pytest

from .. import nodes
from .. import parsing


@pytest.mark.xfail()
def test_internal():
    from ...antlr import accel
    with contextlib.ExitStack() as es:
        es.enter_context(accel.patch_simulator_context())
        es.enter_context(accel.patch_hash_context())

        def run(buf):
            parsed = parsing.parse(buf)
            print(parsed)

        print()
        dp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../caches'))
        for fp in sorted(glob.glob(f'{dp}/**/*.py', recursive=True)):
            with open(fp, 'r') as f:
                buf = f.read()

            start = time.time()
            run(buf)
            end = time.time()
            print('%-80s: %0.2f' % (fp, end - start,))


def test_exprs():
    for src in [
        '1 + 2\n',
        '1+2-3+4-5\n',
        '1+++++2\n',
        'x = 2\n',
        '1|2|3\n',
        '1^2^3\n',
        '1&2&3\n',
        '1<<2>>3\n',
        'f(1)\n',
    ]:
        print(src)
        print(parsing.parse(src))


def test_nodes():
    print(nodes.Assign('a', 'b', type_comment='c'))


@pytest.mark.xfail()
def test_future():
    print(parsing._parse("(x := 1)\n").singleInput())
    print(parsing._parse("def f(x, /, y): pass\n").singleInput())
