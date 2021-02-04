"""
TODO:
 - (py, later my) ast -> lpy ast - minimal, simple
 - usecases
  - snakepid / cadence / hank-lang
   - asyncs?
  - numba
  - jax
  - * auto-cython * - run on lang helpers, etc, handle more and more
  - what i would have used lisp for / that tiny-vm thing
"""
import ast
import inspect
import textwrap

from .. import rendering as ren
from ... import dataclasses as dc
from ... import lang
from ... import pyasts
from ..pyasts import translate


def f0(x, y):
    return x + y + 2


def f1(x, y):
    z = x / 2
    return abs(y - z) + 2


class Pt(dc.Data):
    x: int
    y: int


def f2(pt):
    return pt.x + pt.y


def f3(pt):
    pt.x = pt.x + 2
    pt.y = pt.x + 2
    return pt


def f4(pt, y):
    if pt.y == pt.x:
        print(pt)
    if pt.x > y:
        return pt.y
    else:
        return pt.x


def f5(a, b=2, *args, c, d=3, e, **kwargs):
    pass


def test_simp():
    for f in [
        f0,
        f1,
        f2,
        f3,
        f4,
        f5,
        lang.descriptors._MethodDescriptor._py__check_get,  # noqa
        lang.descriptors._MethodDescriptor._py___get__,  # noqa
        lang.descriptors._MethodDescriptor._py___call__,  # noqa
        lang.descriptors.MethodDescriptor._py__get,  # noqa
    ]:
        print(f)
        ar = ast.parse(textwrap.dedent(inspect.getsource(f)), 'exec')
        try:
            nr = translate(ar)
            print(nr)

            rd = ren.render(nr)
            print(rd.strip())

            ar2 = ast.parse(rd, 'exec')
            print(ar2)

            rar = pyasts.reduce_py_ast(ar)
            rar2 = pyasts.reduce_py_ast(ar2)
            assert rar == rar2

        except Exception as e:  # noqa
            print(repr(e))
            raise

        print()
