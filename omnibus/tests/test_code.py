import sys

from .. import code as code_


def test_recode_func():
    def g():
        frame = sys._getframe(1)
        func = code_.get_frame_function(frame)
        code = func.__code__
        newcodeargs = [getattr(code, f'co_{a}') for a in code_.CODE_ARGS]
        newcodeargs[code_.CODE_ARGS.index('consts')] = (None, 2)
        newcode = type(code)(*newcodeargs)
        func.__code__ = newcode

    class C:
        def f(self):
            g()
            return 1

    assert C().f() == 1
    assert C().f() == 2


def test_get_frame_function():
    def f():
        return code_.get_frame_function(sys._getframe(1))

    def g():
        return f()

    v = g()
    assert v is g


def test_posonly():
    if sys.version_info[1] > 7:
        assert callable(code_.CallTypes.posonly)
