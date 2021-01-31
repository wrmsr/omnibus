import typing as ta

from .. import check
from .. import defs
from .. import lang
from .. import properties
from .types import Instr
from .types import Ip
from .values import Value


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

    def __init__(self, instr: Instr, stack: Stack, prev: ta.Optional['Stream'] = None) -> None:
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
    def seq(self) -> ta.Sequence['Stream']:
        l: ta.List[Stream] = []
        cur = self
        while cur is not None:
            l.append(cur)
            cur = cur._prev
        return l

    @property
    def stack_seq(self) -> ta.Sequence[Stack]:
        return list(self._stack)

    @property
    def prev(self) -> ta.Optional['Stream']:
        return self._prev

    next: ta.Sequence['Stream'] = properties.set_once()
