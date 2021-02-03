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

    def render(self, node: no.Arg) -> r.Part:  # noqa
        if node.default is not None:
            default = ['=', self.render(node.default)]
        else:
            default = []

        if node.annotation is not None:
            return [r.Concat([node.name, ':']), self.render(node.annotation), *default]
        else:
            return r.Concat([node.name, *default])

    def render(self, node: no.Args) -> r.Part:  # noqa
        l = []  # noqa
        l.extend(self.render(a) for a in node.args)
        if node.vararg:
            l.append(r.Concat(['*', self.render(node.vararg)]))
        elif node.kw_only_args:
            l.append('*')
        if node.kw_only_args:
            l.extend(self.render(a) for a in node.kw_only_args)
        if node.kwarg is not None:
            l.append(r.Concat(['**', self.render(node.kwarg)]))
        return r.List(l)

    def render(self, node: no.BinExpr) -> r.Part:  # noqa
        return [self.paren(node.left), node.op.value, self.paren(node.right)]

    def render(self, node: no.Call) -> r.Part:  # noqa
        return r.Concat([
            self.render(node.func),
            '(',
            r.List([self.render(a) for a in [*node.args, *node.keywords]]),
            ')',
        ])

    def render(self, node: no.Const) -> r.Part:  # noqa
        return repr(node.value)

    def render(self, node: no.ExprStmt) -> r.Part:  # noqa
        return self.render(node.expr)

    def render(self, node: no.FunctionDef) -> r.Part:  # noqa
        args = [
            node.name,
            '(',
            self.render(node.args),
            ')',
        ]

        if node.returns is not None:
            proto = [
                r.Concat(args),
                '->',
                r.Concat([self.render(node.returns), ':']),
            ]
        else:
            proto = r.Concat([*args, ':'])

        return [
            'def',
            proto,
            self.render(check.single(node.body)),  # FIXME: ...
        ]

    def render(self, node: no.Return) -> r.Part:  # noqa
        return ['return', *([self.render(node.value)] if node.value is not None else [])]

    def render(self, node: no.UnaryExpr) -> r.Part:  # noqa
        return r.Concat([node.op.value, self.paren(node.value)])


def render(node: no.Node) -> str:
    check.isinstance(node, no.Node)
    part = Renderer()(node)
    part = r.remove_nodes(part)
    part = r.compact_part(part)
    return r.render_part(part).getvalue()
