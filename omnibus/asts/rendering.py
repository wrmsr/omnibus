import collections.abc
import io
import typing as ta

from . import nodes as no
from .. import check
from .. import dataclasses as dc
from .. import dispatch


T = ta.TypeVar('T')
NoneType = type(None)


Part = ta.Union[str, ta.Sequence['Part'], 'DataPart']


class DataPart(dc.Enum):
    pass


class Paren(DataPart):
    part: Part


class List(DataPart):
    parts: ta.Sequence[ta.Optional[Part]]
    delimiter: str = ','


class Concat(DataPart):
    parts: ta.Sequence[Part]


class Node(DataPart):
    node: no.Node


def needs_paren(node: no.Node) -> bool:
    return False


class Renderer(dispatch.Class):
    render = dispatch.property()

    def __call__(self, node: ta.Optional[no.Node]) -> Part:
        if node is None:
            return []
        return [Node(node), self.render(node)]

    def render(self, node: no.Node) -> Part:  # noqa
        raise TypeError(node)

    def paren(self, node: no.Node) -> Part:  # noqa
        return Paren(self(node)) if needs_paren(node) else self(node)

    def render(self, node: no.BinExpr) -> Part:  # noqa
        return [
            self.paren(node.left),
            node.op.value,
            self.paren(node.right),
        ]

    def render(self, node: no.Constant) -> Part:  # noqa
        return repr(node.value)


class PartTransform(dispatch.Class):
    __call__ = dispatch.property()

    def __call__(self, part: str) -> Part:  # noqa
        return part

    def __call__(self, part: collections.abc.Sequence) -> Part:  # noqa
        return [self(c) for c in part]

    def __call__(self, part: Paren) -> Part:  # noqa
        return Paren(self(part.part))

    def __call__(self, part: List) -> Part:  # noqa
        return List([self(c) for c in part.parts], part.delimiter)

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
        return List(parts, part.delimiter) if parts else []

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
    elif isinstance(part, Concat):
        for c in part.parts:
            render_part(c, buf)
    elif isinstance(part, Node):
        pass
    else:
        raise TypeError(part)


def render(node: no.Node) -> str:
    check.isinstance(node, no.Node)
    part = Renderer()(node)
    part = remove_nodes(part)
    part = compact_part(part)
    buf = io.StringIO()
    render_part(part, buf)
    return buf.getvalue()
