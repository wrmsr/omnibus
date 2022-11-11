"""
https://bitbucket.org/windel/ppci/src/default/ppci/graph/relooper.py

https://docs.python.org/3.7/library/dis.html#python-bytecode-instructions
https://docs.python.org/3.8/library/dis.html#python-bytecode-instructions
"""
import contextlib
import sys
import textwrap

import pytest  # noqa

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


@pytest.mark.xfail
def test_try():
    """
              0 LOAD_CONST               1 (0)
              2 LOAD_CONST               0 (None)
              4 IMPORT_NAME              0 (dis)
              6 STORE_FAST               0 (dis)

109           8 LOAD_FAST                0 (dis)
             10 LOAD_METHOD              0 (dis)
             12 LOAD_GLOBAL              1 (test_try)
             14 CALL_METHOD              1
             16 POP_TOP

111          18 LOAD_CONST               2 (2)
             20 STORE_FAST               1 (x)

112          22 SETUP_FINALLY           72 (to 96)
             24 SETUP_FINALLY           24 (to 50)

113          26 LOAD_GLOBAL              3 (reverse_expr)
             28 LOAD_GLOBAL              3 (reverse_expr)
             30 LOAD_FAST                1 (x)
             32 LOAD_CONST               4 (4)
             34 BINARY_ADD
             36 CALL_FUNCTION            1
             38 LOAD_CONST               5 (5)
             40 BINARY_ADD
             42 CALL_FUNCTION            1
             44 POP_TOP
             46 POP_BLOCK
             48 JUMP_FORWARD            42 (to 92)

114     >>   50 DUP_TOP
             52 LOAD_GLOBAL              4 (Exception)
             54 COMPARE_OP              10 (exception match)
             56 POP_JUMP_IF_FALSE       90
             58 POP_TOP
             60 STORE_FAST               2 (e)
             62 POP_TOP
             64 SETUP_FINALLY           12 (to 78)

115          66 LOAD_GLOBAL              2 (print)
             68 LOAD_FAST                2 (e)
             70 CALL_FUNCTION            1
             72 POP_TOP
             74 POP_BLOCK
             76 BEGIN_FINALLY
        >>   78 LOAD_CONST               0 (None)
             80 STORE_FAST               2 (e)
             82 DELETE_FAST              2 (e)
             84 END_FINALLY
             86 POP_EXCEPT
             88 JUMP_FORWARD             2 (to 92)
        >>   90 END_FINALLY
        >>   92 POP_BLOCK
             94 BEGIN_FINALLY

117     >>   96 LOAD_GLOBAL              2 (print)
             98 LOAD_CONST               3 ('finally')
            100 CALL_FUNCTION            1
            102 POP_TOP
            104 END_FINALLY
            106 LOAD_CONST               0 (None)
            108 RETURN_VALUE
    """
    # import dis
    # dis.dis(test_try)

    x = 2
    try:
        reverse_expr(reverse_expr(x + 4) + 5)
    except Exception as e:
        print(e)
        raise
    finally:
        print('finally')


@contextlib.contextmanager
def _cm():
    yield 1


@pytest.mark.xfail
def test_with():
    """
              0 LOAD_CONST               1 (0)
              2 LOAD_CONST               0 (None)
              4 IMPORT_NAME              0 (dis)
              6 STORE_FAST               0 (dis)

133           8 LOAD_FAST                0 (dis)
             10 LOAD_METHOD              0 (dis)
             12 LOAD_GLOBAL              1 (test_with)
             14 CALL_METHOD              1
             16 POP_TOP

135          18 LOAD_GLOBAL              2 (_cm)
             20 CALL_FUNCTION            0
             22 SETUP_WITH              26 (to 50)
             24 STORE_FAST               1 (x)

136          26 LOAD_GLOBAL              3 (reverse_expr)
             28 LOAD_GLOBAL              3 (reverse_expr)
             30 LOAD_FAST                1 (x)
             32 LOAD_CONST               2 (4)
             34 BINARY_ADD
             36 CALL_FUNCTION            1
             38 LOAD_CONST               3 (5)
             40 BINARY_ADD
             42 CALL_FUNCTION            1
             44 POP_TOP
             46 POP_BLOCK
             48 BEGIN_FINALLY
        >>   50 WITH_CLEANUP_START
             52 WITH_CLEANUP_FINISH
             54 END_FINALLY
             56 LOAD_CONST               0 (None)
             58 RETURN_VALUE
    """
    # import dis
    # dis.dis(test_with)

    with _cm() as x:
        reverse_expr(reverse_expr(x + 4) + 5)
