import opcode
import sys
import typing as ta

from .ops import AbsJmpDst
from .ops import DupEffect
from .ops import NextDst
from .ops import NopEffect
from .ops import Op
from .ops import PushEffect
from .ops import RelJmpDst
from .ops import RetDst
from .ops import RotEffect
from .ops import SimpleEffect
from .ops import Step
from .values import Attr
from .values import Const
from .values import Global
from .values import Local
from .values import MethodCallable
from .values import MethodInstance
from .values import Name


OPS = [

    Op('NOP', [Step(NextDst(), NopEffect())]),

    Op('ROT_TWO', [Step(NextDst(), RotEffect(2))]),
    Op('ROT_THREE', [Step(NextDst(), RotEffect(3))]),
    Op('ROT_FOUR', [Step(NextDst(), RotEffect(4))], versions=[3.8]),
    Op('DUP_TOP', [Step(NextDst(), DupEffect(1))]),
    Op('DUP_TOP_TWO', [Step(NextDst(), DupEffect(2))]),

    Op('UNARY_POSITIVE', [Step(NextDst(), SimpleEffect(replace=1))]),
    Op('UNARY_NEGATIVE', [Step(NextDst(), SimpleEffect(replace=1))]),
    Op('UNARY_NOT', [Step(NextDst(), SimpleEffect(replace=1))]),
    Op('UNARY_INVERT', [Step(NextDst(), SimpleEffect(replace=1))]),
    # GET_ITER
    # GET_YIELD_FROM_ITER

    Op('BINARY_POWER', [Step(NextDst(), SimpleEffect(replace=1))]),
    Op('BINARY_MULTIPLY', [Step(NextDst(), SimpleEffect(replace=1))]),
    Op('BINARY_MATRIX_MULTIPLY', [Step(NextDst(), SimpleEffect(replace=1))]),
    Op('BINARY_FLOOR_DIVIDE', [Step(NextDst(), SimpleEffect(replace=1))]),
    Op('BINARY_TRUE_DIVIDE', [Step(NextDst(), SimpleEffect(replace=1))]),
    Op('BINARY_MODULO', [Step(NextDst(), SimpleEffect(replace=1))]),
    Op('BINARY_ADD', [Step(NextDst(), SimpleEffect(replace=1))]),
    Op('BINARY_SUBTRACT', [Step(NextDst(), SimpleEffect(replace=1))]),
    Op('BINARY_SUBSCR', [Step(NextDst(), SimpleEffect(replace=1))]),
    Op('BINARY_LSHIFT', [Step(NextDst(), SimpleEffect(replace=1))]),
    Op('BINARY_RSHIFT', [Step(NextDst(), SimpleEffect(replace=1))]),
    Op('BINARY_AND', [Step(NextDst(), SimpleEffect(replace=1))]),
    Op('BINARY_XOR', [Step(NextDst(), SimpleEffect(replace=1))]),
    Op('BINARY_OR', [Step(NextDst(), SimpleEffect(replace=1))]),

    Op('INPLACE_POWER', [Step(NextDst(), SimpleEffect(replace=1))]),
    Op('INPLACE_MULTIPLY', [Step(NextDst(), SimpleEffect(replace=1))]),
    Op('INPLACE_MATRIX_MULTIPLY', [Step(NextDst(), SimpleEffect(replace=1))]),
    Op('INPLACE_FLOOR_DIVIDE', [Step(NextDst(), SimpleEffect(replace=1))]),
    Op('INPLACE_TRUE_DIVIDE', [Step(NextDst(), SimpleEffect(replace=1))]),
    Op('INPLACE_MODULO', [Step(NextDst(), SimpleEffect(replace=1))]),
    Op('INPLACE_ADD', [Step(NextDst(), SimpleEffect(replace=1))]),
    Op('INPLACE_SUBTRACT', [Step(NextDst(), SimpleEffect(replace=1))]),
    Op('INPLACE_LSHIFT', [Step(NextDst(), SimpleEffect(replace=1))]),
    Op('INPLACE_RSHIFT', [Step(NextDst(), SimpleEffect(replace=1))]),
    Op('INPLACE_AND', [Step(NextDst(), SimpleEffect(replace=1))]),
    Op('INPLACE_XOR', [Step(NextDst(), SimpleEffect(replace=1))]),
    Op('INPLACE_OR', [Step(NextDst(), SimpleEffect(replace=1))]),
    Op('STORE_SUBSCR', [Step(NextDst(), SimpleEffect(replace=1))]),
    Op('DELETE_SUBSCR', [Step(NextDst(), SimpleEffect(replace=1))]),

    # GET_AWAITABLE
    # GET_AITER
    # GET_ANEXT
    # !END_ASYNC_FOR
    # BEFORE_ASYNC_WITH
    # SETUP_ASYNC_WITH

    # PRINT_EXPR
    # ^BREAK_LOOP
    # ^CONTINUE_LOOP(target)
    # SET_ADD(i)
    # LIST_APPEND(i)
    # MAP_ADD(i)

    Op('RETURN_VALUE', [Step(RetDst())]),
    # YIELD_VALUE
    # YIELD_FROM
    # SETUP_ANNOTATIONS
    # IMPORT_STAR
    # POP_BLOCK
    # POP_EXCEPT
    # !POP_FINALLY(preserve_tos)
    # !BEGIN_FINALLY
    # END_FINALLY
    # LOAD_BUILD_CLASS
    # SETUP_WITH(delta)
    # WITH_CLEANUP_START
    # WITH_CLEANUP_FINISH

    # STORE_NAME(namei)
    # DELETE_NAME(namei)
    # UNPACK_SEQUENCE(count)
    # UNPACK_EX(counts)
    # STORE_ATTR(namei)
    # DELETE_ATTR(namei)
    # STORE_GLOBAL(namei)
    # DELETE_GLOBAL(namei)
    Op('LOAD_CONST', [Step(NextDst(), PushEffect(lambda stream: [Const(stream.instr.argval)]))]),
    Op('LOAD_NAME', [Step(NextDst(), PushEffect(lambda stream: [Name(stream.instr.argval)]))]),

    # BUILD_TUPLE(count)
    # BUILD_LIST(count)
    # BUILD_SET(count)
    # BUILD_MAP(count)
    # BUILD_CONST_KEY_MAP(count)
    # BUILD_STRING(count)
    # BUILD_TUPLE_UNPACK(count)
    # BUILD_TUPLE_UNPACK_WITH_CALL(count)
    # BUILD_LIST_UNPACK(count)
    # BUILD_SET_UNPACK(count)
    # BUILD_MAP_UNPACK(count)
    # BUILD_MAP_UNPACK_WITH_CALL(count)
    Op('LOAD_ATTR', [Step(NextDst(), PushEffect(lambda stream: [Attr(stream.stack[0], stream.instr.argval)], 1))]),
    Op('COMPARE_OP', [Step(NextDst(), SimpleEffect(replace=1))]),

    # IMPORT_NAME(namei)
    # IMPORT_FROM(namei)

    Op('JUMP_FORWARD', [Step(RelJmpDst())]),
    Op('POP_JUMP_IF_TRUE', [Step(NextDst()), Step(AbsJmpDst())]),
    Op('POP_JUMP_IF_FALSE', [Step(NextDst()), Step(AbsJmpDst())]),
    Op('JUMP_IF_TRUE_OR_POP', [Step(NextDst(), SimpleEffect(-1)), Step(AbsJmpDst())]),
    Op('JUMP_IF_FALSE_OR_POP', [Step(NextDst(), SimpleEffect(-1)), Step(AbsJmpDst())]),
    Op('JUMP_ABSOLUTE', [Step(AbsJmpDst())]),
    Op('FOR_ITER', [Step(), Step(RelJmpDst(), SimpleEffect(-1))]),
    Op('LOAD_GLOBAL', [Step(NextDst(), PushEffect(lambda stream: [Global(stream.instr.argval)]))]),
    Op('SETUP_LOOP', [Step()], versions=[3.7]),
    # ^SETUP_EXCEPT(delta)
    # SETUP_FINALLY(delta)
    # !CALL_FINALLY(delta)

    Op('LOAD_FAST', [Step(NextDst(), PushEffect(lambda stream: [Local(stream.instr.argval)]))]),
    # STORE_FAST(var_num)
    # DELETE_FAST(var_num)
    # LOAD_CLOSURE(i)
    # LOAD_DEREF(i)
    # LOAD_CLASSDEREF(i)
    # STORE_DEREF(i)
    # DELETE_DEREF(i)
    # RAISE_VARARGS(argc)
    Op('CALL_FUNCTION', [Step(NextDst(), SimpleEffect(replace=1))]),
    # CALL_FUNCTION_KW(argc)
    # CALL_FUNCTION_EX(flags)
    # MAKE_FUNCTION(flags)
    # BUILD_SLICE(argc)
    # EXTENDED_ARG(ext)
    # FORMAT_VALUE(flags)
    # HAVE_ARGUMENT

]

OPS.extend([

    Op('LOAD_METHOD', [Step(NextDst(), PushEffect(lambda stream: [MethodInstance(stream.stack[0], stream.instr.argval), MethodCallable(stream.stack[0], stream.instr.argval)], 1))]),  # noqa
    Op('CALL_METHOD', [Step(NextDst(), SimpleEffect(replace=1))]),

] if sys.implementation.name != 'pypy' else [])


OPS_BY_NAME: ta.Dict[str, Op] = {op.name: op for op in OPS if op.name in opcode.opmap}
OPS_BY_NAME.update({name: Op(name) for name in opcode.opmap if name not in OPS_BY_NAME})
