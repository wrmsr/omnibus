import abc
import dataclasses as dc
import dis
import opcode
import sys
import typing as ta

from .. import check
from .. import defs
from .. import lang
from .streams import Stack
from .streams import Stream
from .types import Instr
from .values import Unknown
from .values import Value


T = ta.TypeVar('T')


_VERSION_FLOAT = float('.'.join(map(str, sys.version_info[:2])))


def _add(st: ta.MutableSet[T], val: T) -> T:
    st.add(val)
    return val


class Effect(lang.Abstract):

    @abc.abstractmethod
    def __call__(self, stream: Stream) -> ta.Tuple[Stack, ta.Iterable[Value]]:
        raise NotImplementedError


class NopEffect(Effect, lang.Final):

    def __call__(self, stream: Stream) -> ta.Tuple[Stack, ta.Iterable[Value]]:
        return stream.stack, []


@dc.dataclass(frozen=True)
class SimpleEffect(Effect, lang.Final):
    offset: ta.Union[ta.Callable[[Instr], int], int] = None
    replace: int = 0

    def __call__(self, stream: Stream) -> ta.Tuple[Stack, ta.Iterable[Value]]:
        # if stream.instr.opname in ('WITH_CLEANUP_START', 'BEGIN_FINALLY'):
        #     breakpoint()
        if callable(self.offset):
            offset = self.offset(stream.instr)
        elif isinstance(self.offset, int):
            offset = self.offset
        elif self.offset is None:
            offset = opcode.stack_effect(stream.instr.opcode, stream.instr.arg)
        else:
            raise TypeError(self.offset)

        out_stack = stream.stack
        out_values = set()

        if offset > 0:
            out_stack = out_stack + [_add(out_values, Unknown())] * offset
        elif offset < 0:
            check.state(len(out_stack) >= offset)
            out_stack = out_stack[-offset:]

        if self.replace:
            check.state(len(out_stack) >= self.replace > 0)
            out_stack = out_stack[self.replace:] + [_add(out_values, Unknown())] * self.replace

        return out_stack, out_values


@dc.dataclass(frozen=True)
class PushEffect(Effect, lang.Final):
    fn: ta.Callable[[Stream], ta.Iterable[Value]]
    replace: int = 0

    def __call__(self, stream: Stream) -> ta.Tuple[Stack, ta.Iterable[Value]]:
        stack = stream.stack
        if self.replace:
            check.state(self.replace > 0)
            stack = stack[self.replace:]
        out_values = list(self.fn(stream))
        return stack + out_values, set(out_values)


@dc.dataclass(frozen=True)
class RotEffect(Effect, lang.Final):
    num: int

    def __call__(self, stream: Stream) -> ta.Tuple[Stack, ta.Iterable[Value]]:
        return stream.stack[self.num:] + [stream.stack[1]] + stream.stack[1:self.num], []


@dc.dataclass(frozen=True)
class DupEffect(Effect, lang.Final):
    num: int

    def __call__(self, stream: Stream) -> ta.Tuple[Stack, ta.Iterable[Value]]:
        return stream.stack + stream.stack[:self.num], []


class Dst(lang.Abstract):

    def __call__(self, stream: Stream) -> ta.Optional[int]:
        raise NotImplementedError

    def __repr__(self) -> str:
        return type(self).__name__


class NextDst(Dst, lang.Final):

    def __call__(self, stream: Stream) -> ta.Optional[int]:
        return stream.ip + 1


class RetDst(Dst, lang.Final):

    def __call__(self, stream: Stream) -> ta.Optional[int]:
        return None


class RelJmpDst(Dst, lang.Final):

    def __call__(self, stream: Stream) -> ta.Optional[int]:
        return (stream.instr.offset + 2 + stream.instr.arg) // 2


class AbsJmpDst(Dst, lang.Final):

    def __call__(self, stream: Stream) -> ta.Optional[int]:
        return stream.instr.arg // 2


@dc.dataclass(frozen=True)
class Step(lang.Final):
    dst: Dst = NextDst()
    effect: Effect = SimpleEffect()

    def __call__(self, stream: Stream, instrs: ta.List[Instr]) -> ta.Optional[Stream]:
        out_stack, out_values = self.effect(stream)
        out_ip = self.dst(stream)
        if out_ip is not None:
            out_instr = instrs[out_ip]
            out_stream = Stream(out_instr, out_stack, stream)
            for val in out_values:
                val.stream = stream
            return out_stream
        else:
            check.state(not out_stack)
            check.state(not out_values)
            return None


class Op:

    def __init__(
            self,
            name: str,
            steps: ta.Iterable[Step] = None,
            *,
            versions: ta.Iterable[float] = None,
    ) -> None:
        super().__init__()

        self._name = name
        self._versions = frozenset(check.isinstance(v, float) for v in versions) if versions is not None else None
        self._explicit = False

        if self._versions is not None and _VERSION_FLOAT not in self._versions:
            self._enabled = False

        else:
            self._enabled = True
            self._opcode = opcode.opmap[name]

            steps_: ta.List[Step]
            if steps is not None:
                steps_ = check.not_empty([check.isinstance(s, Step) for s in steps])
            else:
                steps_ = [Step()]
                if self._opcode in dis.hasjrel:
                    steps_.append(Step(RelJmpDst()))
                elif self._opcode in dis.hasjabs:
                    steps_.append(Step(AbsJmpDst()))
            self._steps = steps_

    defs.repr('name')

    @property
    def name(self) -> str:
        return self._name

    @property
    def versions(self) -> ta.Optional[ta.FrozenSet[float]]:
        return self._versions

    @property
    def opcode(self) -> int:
        check.state(self._enabled)
        return self._opcode

    @property
    def steps(self) -> ta.List[Step]:
        check.state(self._enabled)
        return self._steps

    @property
    def explicit(self) -> bool:
        return self._explicit
