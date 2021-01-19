import types

from .analysis import Analysis
from .streams import Stream
from .values import Attr
from .values import BinaryOp
from .values import Call
from .values import Const
from .values import NamedValue
from .values import Unknown
from .values import Value


BINARY_OP_TAGS_BY_OPNAME = {
    'BINARY_ADD': '+',
    'BINARY_MULTIPLY': '*',
}


def reconstruct_value(value: Value) -> Value:
    if isinstance(value, (Const, NamedValue)):
        return value

    elif isinstance(value, Unknown):
        return reconstruct_stream_value(value.stream)

    elif isinstance(value, Attr):
        return Attr(reconstruct_value(value.object), value.name)

    else:
        raise TypeError(value)


def reconstruct_stream_value(stream: Stream) -> Value:
    if stream.instr.opname == 'COMPARE_OP':
        return BinaryOp(
            reconstruct_value(stream.stack[1]),
            stream.instr.argrepr,
            reconstruct_value(stream.stack[0]),
        )

    elif stream.instr.opname in BINARY_OP_TAGS_BY_OPNAME:
        return BinaryOp(
            reconstruct_value(stream.stack[1]),
            BINARY_OP_TAGS_BY_OPNAME[stream.instr.opname],
            reconstruct_value(stream.stack[0]),
        )

    elif stream.instr.opname == 'CALL_FUNCTION':
        vs = [reconstruct_value(v) for v in reversed(stream.stack[:stream.instr.argval + 1])]  # noqa
        return Call(vs[0], vs[1:])

    else:
        raise ValueError(stream.instr)


def reconstruct_frame_call_arg(frame: types.FrameType) -> Value:
    ana = Analysis(frame)

    caller_stream: Stream
    [caller_stream] = ana.streams_by_src_by_dst[frame.f_lasti // 2].values()  # noqa

    if caller_stream.instr.opname != 'CALL_FUNCTION':
        raise ValueError(f'{frame}: {caller_stream.instr.opname}')

    return reconstruct_stream_value(caller_stream.prev)
