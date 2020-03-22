import ast
import ctypes as ct
import dis
import inspect
import platform
import types
import typing as ta

from omnibus import check
from omnibus import properties

from .frames import PyFrameObject
from .ops import OPS_BY_NAME
from .types import Instr
from .types import Ip
from .types import Stack
from .types import Stream


class Analysis:

    def __init__(self, frame: types.FrameType) -> None:
        super().__init__()

        self._frame = check.isinstance(frame, types.FrameType)

    @property
    def frame(self) -> types.FrameType:
        return self._frame

    @properties.cached
    def py_frame(self) -> PyFrameObject:
        if platform.python_implementation() != 'CPython':
            raise RuntimeError
        return ct.cast(id(self._frame), ct.POINTER(PyFrameObject)).contents

    @properties.cached
    def source(self) -> str:
        return inspect.getsource(self._frame)

    @properties.cached
    def ast(self) -> ast.AST:
        return ast.parse(self.source)

    @property
    def code(self) -> types.CodeType:
        return self._frame.f_code

    @properties.cached
    def instrs(self) -> ta.Sequence[Instr]:
        return list(dis.get_instructions(self.code))

    @properties.cached
    def ips_by_instr(self) -> ta.Mapping[Ip, Instr]:
        return {instr: ip for ip, instr in enumerate(self.instrs)}

    @properties.cached
    def streams_by_src_by_dst(self) -> ta.Mapping[Ip, ta.Mapping[Ip, Stream]]:
        streams: ta.List[Stream] = [Stream(self.instrs[0], Stack.NIL)]
        streams_by_src_by_dst: ta.Dict[Ip, ta.Dict[Ip, Stream]] = {}

        while streams:
            stream = streams.pop()

            while True:
                instr = self.instrs[stream.ip]
                op = OPS_BY_NAME[instr.opname]

                streams_by_src = streams_by_src_by_dst.setdefault(stream.ip, {})
                src_ip = stream.prev.ip if stream.prev is not None else None
                if src_ip in streams_by_src:
                    break
                streams_by_src[src_ip] = stream

                out_stream, *branch_streams = stream.next = tuple(s(stream, self.instrs) for s in op.steps)
                for branch_stream in branch_streams:
                    streams.append(branch_stream)

                if out_stream is None:
                    break

                stream = out_stream

        return streams_by_src_by_dst
