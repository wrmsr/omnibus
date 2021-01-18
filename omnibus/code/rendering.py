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


compact_part = CompactPart()


def render_part(part: Part, buf: io.StringIO) -> None:
    if isinstance(part, str):
        buf.write(part)
    elif isinstance(part, collections.abc.Sequence):
        for i, c in enumerate(part):
            if i:
                buf.write(' ')
            render_part(c, buf)
    elif isinstance(part, Paren):
        buf.write('(')
        render_part(part.part, buf)
        buf.write(')')
    elif isinstance(part, List):
        for i, c in enumerate(part.parts):
            if i:
                buf.write(part.delimiter + ' ')
            render_part(c, buf)
        if part.trailer:
            buf.write(part.delimiter)
    elif isinstance(part, Concat):
        for c in part.parts:
            render_part(c, buf)
    elif isinstance(part, Node):
        pass
    else:
        raise TypeError(part)
