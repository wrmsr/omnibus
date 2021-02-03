import collections.abc
import io
import typing as ta

from .. import dataclasses as dc
from .. import dispatch


T = ta.TypeVar('T')
NodeT = ta.TypeVar('NodeT')


Part = ta.Union[str, ta.Sequence['Part'], 'DataPart']


class DataPart(dc.Enum):
    pass


class Paren(DataPart):
    part: Part


class List(DataPart):
    parts: ta.Sequence[ta.Optional[Part]]
    delimiter: str = ','
    trailer: bool = False


class Concat(DataPart):
    parts: ta.Sequence[Part]


class Block(DataPart):
    parts: ta.Sequence[Part]


class Section(DataPart):
    parts: ta.Sequence[Part]


class Node(DataPart, ta.Generic[NodeT], final=False):
    node: NodeT


class PartTransform(dispatch.Class):
    __call__ = dispatch.property()

    def __call__(self, part: str) -> Part:  # noqa
        return part

    def __call__(self, part: collections.abc.Sequence) -> Part:  # noqa
        return [self(c) for c in part]

    def __call__(self, part: Paren) -> Part:  # noqa
        return Paren(self(part.part))

    def __call__(self, part: List) -> Part:  # noqa
        return List([self(c) for c in part.parts], part.delimiter, part.trailer)

    def __call__(self, part: Concat) -> Part:  # noqa
        return Concat([self(c) for c in part.parts])

    def __call__(self, part: Block) -> Part:  # noqa
        return Block([self(c) for c in part.parts])

    def __call__(self, part: Section) -> Part:  # noqa
        return Section([self(c) for c in part.parts])

    def __call__(self, part: Node) -> Part:  # noqa
        return part


class RemoveNodes(PartTransform):

    def __call__(self, part: Node) -> Part:  # noqa
        return []


remove_nodes = RemoveNodes()


def _drop_empties(it: ta.Iterable[T]) -> ta.List[T]:
    return [
        e for e in it if not (
                isinstance(e, collections.abc.Sequence) and
                not e and
                not isinstance(e, str)
        )
    ]


class CompactPart(PartTransform):

    def __call__(self, part: collections.abc.Sequence) -> Part:  # noqa
        return _drop_empties(self(c) for c in part)

    def __call__(self, part: List) -> Part:  # noqa
        parts = _drop_empties(self(c) for c in part.parts)
        return List(parts, part.delimiter, part.trailer) if parts else []

    def __call__(self, part: Concat) -> Part:  # noqa
        parts = _drop_empties(self(c) for c in part.parts)
        return Concat(parts) if parts else []

    def __call__(self, part: Block) -> Part:  # noqa
        parts = _drop_empties(self(c) for c in part.parts)
        return Block(parts) if parts else []

    def __call__(self, part: Section) -> Part:  # noqa
        parts = _drop_empties(self(c) for c in part.parts)
        return Section(parts) if parts else []


compact_part = CompactPart()


class PartRenderer(dispatch.Class):
    def __init__(self, buf: io.StringIO, *, indent: str = '    ') -> None:
        super().__init__()

        self._buf = buf

        self._indents = 0
        self._indent = indent

    __call__ = dispatch.property()

    def __call__(self, part: str) -> None:  # noqa
        self._buf.write(part)

    def __call__(self, part: collections.abc.Sequence) -> None:  # noqa
        for i, c in enumerate(part):
            if i:
                self._buf.write(' ')
            self(c)

    def __call__(self, part: DataPart) -> None:  # noqa
        raise TypeError(part)

    def __call__(self, part: Paren) -> None:  # noqa
        self._buf.write('(')
        self(part.part)
        self._buf.write(')')

    def __call__(self, part: List) -> None:  # noqa
        for i, c in enumerate(part.parts):
            if i:
                self._buf.write(part.delimiter + ' ')
            self(c)
        if part.trailer:
            self._buf.write(part.delimiter)

    def __call__(self, part: Concat) -> None:  # noqa
        for c in part.parts:
            self(c)

    def __call__(self, part: Block) -> None:  # noqa
        for c in part.parts:
            self._buf.write(self._indent * self._indents)
            self(c)
            self._buf.write('\n')

    def __call__(self, part: Section) -> None:  # noqa
        self._indents += 1
        try:
            for c in part.parts:
                self(c)
        finally:
            self._indents -= 1


def render_part(part: Part, buf: ta.Optional[io.StringIO] = None) -> io.StringIO:
    if buf is None:
        buf = io.StringIO()
    PartRenderer(buf)(part)
    return buf
