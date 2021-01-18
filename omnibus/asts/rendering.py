import io
import typing as ta

from . import nodes as no
from .. import check
from .. import dispatch
from ..code import rendering as r


def needs_paren(node: no.Node) -> bool:
    return False


class Renderer(dispatch.Class):
    render = dispatch.property()

    def __call__(self, node: ta.Optional[no.Node]) -> r.Part:
        if node is None:
            return []
        return [r.Node(node), self.render(node)]

    def render(self, node: no.Node) -> r.Part:  # noqa
        raise TypeError(node)

    def paren(self, node: no.Node) -> r.Part:  # noqa
        return r.Paren(self(node)) if needs_paren(node) else self(node)

    def render(self, node: no.Assign) -> r.Part:  # noqa
        return [r.List([self.render(t) for t in node.targets]), '=', self.render(node.value)]

    def render(self, node: no.BinExpr) -> r.Part:  # noqa
        return [self.paren(node.left), node.op.value, self.paren(node.right)]

    def render(self, node: no.Call) -> r.Part:  # noqa
        return r.Concat([
            self.render(node.func),
            '(',
            r.List([self.render(a) for a in [*node.args, *node.kwargs]]),
            ')',
        ])

    def render(self, node: no.Constant) -> r.Part:  # noqa
        return repr(node.value)

    def render(self, node: no.ExprStmt) -> r.Part:  # noqa
        return self.render(node.expr)

    def render(self, node: no.Lambda) -> r.Part:  # noqa
        return ['lambda', r.Concat([self.render(node.args), ':']), self.render(node.body)]

    def render(self, node: no.List) -> r.Part:  # noqa
        return r.Concat(['[', r.List([self.render(e) for e in node.items]), ']'])

    def render(self, node: no.Name) -> r.Part:  # noqa
        return node.name

    def render(self, node: no.Set) -> r.Part:  # noqa
        return r.Concat(['{', r.List([self.render(e) for e in node.items]), '}'])

    def render(self, node: no.SetComp) -> r.Part:  # noqa
        raise NotImplementedError

    def render(self, node: no.Starred) -> r.Part:  # noqa
        raise NotImplementedError

    def render(self, node: no.Subscript) -> r.Part:  # noqa
        return r.Concat(self.render(node.value), '[', self.render(node.slice), ']')

    def render(self, node: no.Tuple) -> r.Part:  # noqa
        return r.Concat(['(', r.List([self.render(e) for e in node.items], trailer=len(node.items) == 1), ')'])

    def render(self, node: no.UnaryExpr) -> r.Part:  # noqa
        return r.Concat([node.op.value, self.paren(node.value)])

    def render(self, node: no.Yield) -> r.Part:  # noqa
        return ['yield', self.render(node.value)]

    def render(self, node: no.YieldFrom) -> r.Part:  # noqa
        return ['yield', 'from', self.render(node.value)]


def render(node: no.Node) -> str:
    check.isinstance(node, no.Node)
    part = Renderer()(node)
    part = r.remove_nodes(part)
    part = r.compact_part(part)
    buf = io.StringIO()
    r.render_part(part, buf)
    return buf.getvalue()
