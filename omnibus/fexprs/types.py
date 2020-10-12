import abc
import dataclasses as dc
import dis
import opcode
import sys
import typing as ta

from .. import check
from .. import defs
from .. import lang
from .. import properties


T = ta.TypeVar('T')
Ip = int


_VERSION_FLOAT = float('.'.join(map(str, sys.version_info[:2])))


def _add(st: ta.MutableSet[T], val: T) -> T:
    st.add(val)
    return val


class Value(lang.Abstract):

    defs.repr()

    stream: 'Stream' = properties.set_once()


class Unknown(Value, lang.Final):
    pass


class Const(Value, lang.Final):

    def __init__(self, value: ta.Any) -> None:
        super().__init__()

        self._value = value

    defs.repr('value')

    @property
    def value(self) -> ta.Any:
        return self._value


class NamedValue(Value, lang.Abstract):

    def __init__(self, name: str) -> None:
        super().__init__()

        self._name = check.not_empty(name)

    defs.repr('name')

    @property
    def name(self) -> str:
        return self._name


class Global(NamedValue, lang.Final):
    pass


class Local(NamedValue, lang.Final):
    pass


class Name(NamedValue, lang.Final):
    pass


class InstanceValue(Value, lang.Abstract):

    def __init__(self, object: Value, name: str) -> None:
        super().__init__()

        self._object = object
        self._name = check.not_empty(name)

    defs.repr('object', 'name')

    @property
    def object(self) -> Value:
        return self._object

    @property
    def name(self) -> str:
        return self._name


class Attr(InstanceValue, lang.Final):
    pass


class MethodInstance(InstanceValue, lang.Final):
    pass


class MethodCallable(InstanceValue, lang.Final):
    pass


Instr = dis.Instruction


class Stack(lang.Final):

    NIL: ta.Optional['Stack'] = None

    def __init__(self, value: Value, prev: 'Stack') -> None:
        super().__init__()

        check.arg((value is None) == (prev is None) == (Stack.NIL is None))
        self._value = check.isinstance(value, Value) if value is not None else None
        self._prev = check.isinstance(prev, Stack) if prev is not None else None
        self._len = self._prev._len + 1 if self._prev is not None else 0

    @staticmethod
    def of(values: ta.Iterable[Value]) -> 'Stack':
        cur = Stack.NIL
        for val in values:
            cur = Stack(val, cur)
        return cur

    @property
    def value(self) -> Value:
        if self._value is None:
            raise TypeError
        return self._value

    @property
    def prev(self) -> ta.Optional['Stack']:
        return self._prev

    def __iter__(self) -> ta.Iterator[Value]:
        cur = self
        while cur is not Stack.NIL:
            yield cur._value
            cur = cur._prev

    def __len__(self) -> int:
        return self._len

    def __getitem__(self, idx: ta.Union[int, slice]) -> ta.Union[Value, 'Stack']:
        if isinstance(idx, int):
            if idx < 0:
                if -idx >= self._len:
                    raise IndexError(idx)
                idx = self._len + idx
            cur = self
            while idx > 0:
                cur = cur._prev
                if cur is Stack.NIL:
                    raise IndexError(idx)
                idx -= 1
            return cur._value

        elif isinstance(idx, slice):
            if idx.step is not None and idx.step != 1:
                raise TypeError(idx)
            cur = self
            if idx.start is not None:
                if idx.start < 0:
                    raise TypeError(idx)
                for _ in range(idx.start):
                    if cur is Stack.NIL:
                        return cur
                    cur = cur._prev
            if idx.stop is not None:
                if idx.stop < 0:
                    raise TypeError(idx)
                ret = []
                for _ in range(idx.start or 0, idx.stop):
                    if cur is Stack.NIL:
                        break
                    ret.append(cur._value)
                    cur = cur._prev
                cur = Stack.of(reversed(ret))
            return cur

        else:
            raise TypeError(idx)

    def __add__(self, other: ta.Iterable[Value]) -> 'Stack':
        cur = self
        for val in other:
            cur = Stack(val, cur)
        return cur

    def __repr__(self) -> str:
        return f'{{{{{", ".join(repr(e) for e in self)}}}}}'


Stack.NIL = Stack(None, None)  # type: ignore


class Stream(lang.Final):

    def __init__(self, instr: Instr, stack: Stack, prev: 'Stream' = None) -> None:
        super().__init__()

        self._instr = check.isinstance(instr, Instr)
        self._stack = check.isinstance(stack, Stack)
        self._prev = check.isinstance(prev, Stream) if prev is not None else None
        check.state(all(isinstance(v, Value) for v in self._stack))
        check.state(instr.offset & 1 == 0)
        self._ip = instr.offset // 2

    defs.repr('ip', 'instr', 'stack')

    @property
    def instr(self) -> Instr:
        return self._instr

    @property
    def ip(self) -> Ip:
        return self._ip

    @property
    def stack(self) -> Stack:
        return self._stack

    @property
    def prev(self) -> ta.Optional['Stream']:
        return self._prev

    next: ta.Sequence['Stream'] = properties.set_once()


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
