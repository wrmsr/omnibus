"""
https://bitbucket.org/windel/ppci/src/default/ppci/graph/relooper.py

https://docs.python.org/3.7/library/dis.html#python-bytecode-instructions
https://docs.python.org/3.8/library/dis.html#python-bytecode-instructions
"""
import sys
import textwrap

from .. import recon as recon_
from .. import values as values_


def reverse_expr(x):
    caller = sys._getframe(1)
    print(caller)

    # import astpretty
    # astpretty.pprint(ana.ast)
    # print()

    # import dis
    # dis.dis(caller.f_code)

    # print('\n'.join(f'{idx}: {repr(instr)}' for idx, instr in enumerate(ana.instrs)))
    # print()

    xv = recon_.reconstruct_frame_call_arg(caller)

    print(xv)
    print(values_.render(xv))
    print()

    return x


def g(x):
    # f(0, 1)

    def barf(y):
        return y ** 10

    class C: pass
    C.f = barf

    C.f(0)

    if x:
        C.f(5 + 6 * x > 9 and x % 2 == 0)

    C.r = 8

    reverse_expr(1 + x * 2 == 3 + C.r)

    if sys.version_info[1] > 7:
        exec(textwrap.dedent("""
            reverse_expr(1 + x * (y := 2) == 420 + C.r)
        """), globals(), locals())

    v = 0
    for foo in range(3):
        v += foo

    v = 0
    i = 0
    while i < 3:
        v += i
        i += 1

    lg = [i + 1 for i in range(x) if i % 2 == 0]  # noqa

    # yield 2


def test_fexprs():
    print()

    x = 1
    # f(x + 2 | x % 2 == 0 & x > 5)
    # f(x and 2 and x % 2 == 0 or x > 5)

    g(1)

    class G:
        x = 1
        reverse_expr(x + 2)

    a = 0
    if a:
        x = 3
    else:
        x = 4
    b = 1
    if b:
        x += 1
    else:
        x += 2
    for _ in range(1):
        if b:
            # f(f(x + 4) + 5 and 6)
            reverse_expr(reverse_expr(x + 4) + 5)

    # x = 5
    # f(x > 1 and x % 3 == 2)
