import ast
import contextlib
import glob
import os.path
import time
import typing as ta

import pytest

from .. import nodes
from .. import parsing


@pytest.mark.xfail()
def test_internal():
    from ...antlr import accel  # noqa
    with contextlib.ExitStack() as es:  # noqa
        # es.enter_context(accel.patch_simulator_context())
        # es.enter_context(accel.patch_hash_context())

        def run(buf):
            parsed = parsing.parse(buf)
            print(parsed)

        print()
        dp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../caches'))
        for fp in sorted(glob.glob(f'{dp}/**/*.py', recursive=True)):
            with open(fp, 'r') as f:
                buf = f.read()
            buf = buf.strip()
            if not buf:
                continue

            start = time.time()
            run(buf)
            end = time.time()
            print('%-80s: %0.2f' % (fp, end - start,))


@pytest.mark.xfail()
def test_internal_raw():
    from ...antlr import accel  # noqa
    with contextlib.ExitStack() as es:  # noqa
        # es.enter_context(accel.patch_simulator_context())
        # es.enter_context(accel.patch_hash_context())

        def run(buf):
            parser = parsing._parse(buf)
            root = parser.singleInput()
            print(root)

        print()
        dp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../caches'))
        for fp in sorted(glob.glob(f'{dp}/**/*.py', recursive=True)):
            with open(fp, 'r') as f:
                buf = f.read()
            buf = buf.strip()
            if not buf:
                continue

            start = time.time()
            for _ in range(3):
                run(buf)
            end = time.time()
            print('%-80s: %0.2f' % (fp, end - start,))


def test_exprs():
    for src in [
        '[1]\n',

        '1 + 2\n',
        '1+2-3+4-5\n',
        '1+++++2\n',
        'x = 2\n',
        '1|2|3\n',
        '1^2^3\n',
        '1&2&3\n',
        '1<<2>>3\n',
        'f(1)\n',
        '[1]\n',
    ]:
        print(src.strip())
        root = parsing.parse(src)
        print(root)

        # from ...antlr import dot
        # from ..._vendor import antlr4
        # dot.open_dot_ctx(root.meta[antlr4.ParserRuleContext])
        # input()

        from .. import rendering
        print(rendering.render(root))

        print()


class PyAstNode(ta.NamedTuple):
    type: str
    fields: ta.Sequence[ta.Tuple[str, ta.Any]]


def _strip_py_ast(obj):
    if obj is None:
        return None
    elif isinstance(obj, ast.AST):
        return PyAstNode(
            type(obj).__name__,
            [(a, _strip_py_ast(getattr(obj, a))) for a in type(obj)._fields],
        )
    elif isinstance(obj, list):
        return tuple(_strip_py_ast(e) for e in obj)
    elif isinstance(obj, (int, str)):
        return obj
    else:
        raise TypeError(obj)


def test_stmts():
    for src in [
        '1 + 2\n',

        'x = 1\n',
        'x = 1\ny = 2\n',

        'def f(x): return x + 1\n',
        'def f(x=0): return x + 1\n',
        'def f(x:int): return x + 1\n',
        'def f(x:int=0): return x + 1\n',
        'def f(x=0, *, y=1, z=2): return x + 1\n',
        'def f(x=0, y=1, z=2): return x + 1\n',
        'def f(x=0, y=1, z=2) -> int: return x + 1\n',
    ]:
        print(src.strip())

        pa0 = _strip_py_ast(ast.parse(src))
        print(pa0)

        root = parsing.parse(src, 'file')
        print(root)

        from .. import rendering
        buf = rendering.render(root)
        print(buf.strip())

        pa1 = _strip_py_ast(ast.parse(buf))
        print(pa1)

        assert pa0 == pa1

        print()


def test_nodes():
    print(nodes.Assign([nodes.Name('a')], nodes.Name('b'), type_comment='c'))


@pytest.mark.xfail()
def test_future():
    print(parsing._parse("(x := 1)\n").singleInput())
    print(parsing._parse("def f(x, /, y): pass\n").singleInput())


if __name__ == '__main__':
    test_internal_raw()
