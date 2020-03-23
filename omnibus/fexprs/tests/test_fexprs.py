"""
https://docs.python.org/3.7/library/dis.html#python-bytecode-instructions
https://docs.python.org/3.8/library/dis.html#python-bytecode-instructions
"""
import sys
import textwrap

from .. import analysis as analysis_
from ..import types as types_


BINARY_OP_TAGS_BY_OPNAME = {
    'BINARY_ADD': '+',
    'BINARY_MULTIPLY': '*',
}


def f(x):
    caller = sys._getframe(1)
    ana = analysis_.Analysis(caller)

    # import astpretty
    # astpretty.pprint(ana.ast)
    # print()

    # import dis
    # dis.dis(caller.f_code)

    # print('\n'.join(f'{idx}: {repr(instr)}' for idx, instr in enumerate(ana.instrs)))
    # print()

    caller_stream: types_.Stream
    [caller_stream] = ana.streams_by_src_by_dst[caller.f_lasti // 2].values()
    print(caller_stream)
    print()

    def rec_value(value: types_.Value):
        if isinstance(value, types_.Const):
            return value.value
        elif isinstance(value, types_.Local):
            return ['LOCAL', value.name]
        elif isinstance(value, types_.Global):
            return ['GLOBAL', value.name]
        elif isinstance(value, types_.Name):
            return ['NAME', value.name]
        elif isinstance(value, types_.Unknown):
            return rec_stream(value.stream)
        elif isinstance(value, types_.Attr):
            return ['ATTR', rec_value(value.object), value.name]
        else:
            raise TypeError(value)

    def rec_stream(stream: types_.Stream):
        if stream.instr.opname == 'COMPARE_OP':
            return [stream.instr.argrepr, rec_value(stream.stack[1]), rec_value(stream.stack[0])]
        elif stream.instr.opname in BINARY_OP_TAGS_BY_OPNAME:
            return [BINARY_OP_TAGS_BY_OPNAME[stream.instr.opname], rec_value(stream.stack[1]), rec_value(stream.stack[0])]  # noqa
        elif stream.instr.opname == 'CALL_FUNCTION':
            return ['CALL_FUNCTION'] + [rec_value(v) for v in reversed(stream.stack[:stream.instr.argval + 1])]
        else:
            raise TypeError

    assert caller_stream.instr.opname == 'CALL_FUNCTION'
    print(rec_stream(caller_stream.prev))
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

    f(1 + x * 2 == 3 + C.r)

    if sys.version_info[1] > 7:
        exec(textwrap.dedent("""
            f(1 + x * (y := 2) == 420 + C.r)
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
    x = 1
    # f(x + 2 | x % 2 == 0 & x > 5)
    # f(x and 2 and x % 2 == 0 or x > 5)

    g(1)

    class G:
        x = 1
        f(x + 2)

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
            f(f(x + 4) + 5)

    # x = 5
    # f(x > 1 and x % 3 == 2)
