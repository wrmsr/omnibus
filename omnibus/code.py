import dis
import gc
import opcode
import sys
import textwrap
import types
import typing as ta

from . import lang


Code = types.CodeType
Function = types.FunctionType
Frame = types.FrameType


CODE_ARGS = [
    'argcount',
    'kwonlyargcount',
    'nlocals',
    'stacksize',
    'flags',
    'code',
    'consts',
    'names',
    'varnames',
    'filename',
    'name',
    'firstlineno',
    'lnotab',
    'freevars',
    'cellvars',
]

if sys.version_info[1] > 7:
    CODE_ARGS.insert(1, 'posonlyargcount')


CO_FLAG_VALUES = {v: k for k, v in dis.COMPILER_FLAG_NAMES.items()}

CO_OPTIMIZED: int = CO_FLAG_VALUES['OPTIMIZED']
CO_NEWLOCALS: int = CO_FLAG_VALUES['NEWLOCALS']
CO_VARARGS: int = CO_FLAG_VALUES['VARARGS']
CO_VARKEYWORDS: int = CO_FLAG_VALUES['VARKEYWORDS']
CO_NESTED: int = CO_FLAG_VALUES['NESTED']
CO_GENERATOR: int = CO_FLAG_VALUES['GENERATOR']
CO_NOFREE: int = CO_FLAG_VALUES['NOFREE']
CO_COROUTINE: int = CO_FLAG_VALUES['COROUTINE']
CO_ITERABLE_COROUTINE: int = CO_FLAG_VALUES['ITERABLE_COROUTINE']
CO_ASYNC_GENERATOR: int = CO_FLAG_VALUES['ASYNC_GENERATOR']


FUNCTION_ARGS = [
    'code',
    'globals',
    'name',
    'defaults',
    'closure',
]

FUNC_NONE = 0
FUNC_DEFAULTS = 1
FUNC_KWDEFAULTS = 2
FUNC_ANNOTATIONS = 4
FUNC_CLOSURE = 8


class CallTypes:

    def __iter__(self):
        for k, v in type(self).__dict__.items():
            if callable(v) and not k.startswith('_'):
                yield v

    def _visit(self, *args, **kwargs):
        pass

    def nullary(self):
        return self._visit()

    def arg(self, arg):
        return self._visit(arg)

    def default(self, default=None):
        return self._visit(default)

    def varargs(self, *varargs):
        return self._visit(*varargs)

    def kwonly(self, *, kwonly=None):
        return self._visit(kwonly=kwonly)

    if sys.version_info[1] > 7:
        exec(textwrap.dedent("""
            def posonly(self, /, posonly):
                return self._visit(posonly)
        """), globals(), locals())

    def kwargs(self, **kwargs):
        return self._visit(**kwargs)

    def all(self, arg, *varargs, default=None, **kwargs):
        return self._visit(arg, *varargs, default=default, **kwargs)

    def all2(self, arg0, arg1, *varargs, default0=None, default1=None, **kwargs):
        return self._visit(arg0, arg1, *varargs, default0=default0, default1=default1, **kwargs)


CALL_TYPES = CallTypes()


class _Op(lang.Final):

    def __getattr__(self, opname: str) -> int:
        return opcode.opmap[opname]


op = _Op()


def make_cell(value):
    def fn():
        nonlocal value
    return fn.__closure__[0]


def get_code_flag_names(flags: int) -> ta.List[str]:
    return [k for k, v in CO_FLAG_VALUES.items() if flags & v]


def recode_func(func: Function, code_bytes: ta.Union[bytes, bytearray]) -> ta.Iterable[ta.Any]:
    codeargs = [getattr(func.__code__, f'co_{k}') for k in CODE_ARGS]
    codeargs[CODE_ARGS.index('code')] = bytes(code_bytes)
    code = Code(*codeargs)

    funcargs = [getattr(func, f'__{k}__') for k in FUNCTION_ARGS]
    funcargs[FUNCTION_ARGS.index('code')] = code
    return funcargs


def instruction_bytes(instrs: ta.Iterable[dis.Instruction]) -> bytes:
    return bytes(b if b is not None else 0 for instr in instrs for b in [instr.opcode, instr.arg])


class AmbiguousFrameException(Exception):
    pass


def get_frame_function(frame: Frame) -> Function:
    """
    AmbiguousFrameException should always be handled gracefully - in the presence of multiple threads (and even
    recursive invocations within a single thread) the originally invoking function may have already had its code
    patched. Callers of this code should be robust enough for this to only result in wasted work that will likely be
    redone and corrected in subsequent invocations.
    """

    refs = gc.get_referrers(frame.f_code)
    funcs = [
        r for r in refs if (
            isinstance(r, Function) and
            r.__code__ is frame.f_code
        )
    ]
    if len(funcs) != 1:
        raise AmbiguousFrameException
    return funcs[0]
