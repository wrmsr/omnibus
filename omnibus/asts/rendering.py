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
        return r.Wrap(self(node)) if needs_paren(node) else self(node)

    def render(self, node: no.Alias) -> r.Part:  # noqa
        return [node.name, ['as', node.as_] if node.as_ is not None else []]

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
        elif node.kwonly_args:
            l.append('*')
        if node.kwonly_args:
            l.extend(self.render(a) for a in node.kwonly_args)
        if node.kwarg is not None:
            l.append(r.Concat(['**', self.render(node.kwarg)]))
        return r.List(l)

    def render(self, node: no.Assign) -> r.Part:  # noqa
        return [r.List([self.render(t) for t in node.targets]), '=', self.render(node.value)]

    def render(self, node: no.BinExpr) -> r.Part:  # noqa
        return [self.paren(node.left), node.op.glyph, self.paren(node.right)]

    def render(self, node: no.Body) -> r.Part:  # noqa
        return r.Block([self.render(s) for s in node.stmts])

    def render(self, node: no.Call) -> r.Part:  # noqa
        return r.Concat([
            self.render(node.func),
            '(',
            r.List([self.render(a) for a in [*node.args, *node.keywords]]),
            ')',
        ])

    def render(self, node: no.Constant) -> r.Part:  # noqa
        return repr(node.value)

    def render(self, node: no.ExprStmt) -> r.Part:  # noqa
        return self.render(node.expr)

    def render(self, node: no.FunctionDef) -> r.Part:  # noqa
        args = [node.name, '(', self.render(node.args), ')']
        if node.returns is not None:
            proto = [r.Concat(args), '->', r.Concat([self.render(node.returns), ':'])]
        else:
            proto = r.Concat([*args, ':'])

        return [
            'def',
            proto,
            r.Block([self.render(b) for b in node.body]),
        ]

    def render(self, node: no.Import) -> r.Part:  # noqa
        return ['import', r.List([self.render(n) for n in node.names])]

    def render(self, node: no.ImportFrom) -> r.Part:  # noqa
        return ['from', node.module, 'import', r.List([self.render(n) for n in node.names])]

    def render(self, node: no.Lambda) -> r.Part:  # noqa
        return ['lambda', r.Concat([self.render(node.args), ':']), self.render(node.body)]

    def render(self, node: no.List) -> r.Part:  # noqa
        return r.Concat(['[', r.List([self.render(e) for e in node.items]), ']'])

    def render(self, node: no.Module) -> r.Part:  # noqa
        return [self.render(d) for d in node.stmts]

    def render(self, node: no.Name) -> r.Part:  # noqa
        return node.id

    def render(self, node: no.Return) -> r.Part:  # noqa
        return ['return', [self.render(node.value)] if node.value is not None else []]

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
        return r.Concat([node.op.glyph, self.paren(node.value)])

    def render(self, node: no.Yield) -> r.Part:  # noqa
        return ['yield', self.render(node.value)]

    def render(self, node: no.YieldFrom) -> r.Part:  # noqa
        return ['yield', 'from', self.render(node.value)]


def render(node: no.Node) -> str:
    check.isinstance(node, no.Node)
    part = Renderer()(node)
    part = r.remove_nodes(part)
    part = r.compact_part(part)
    return r.render_part(part).getvalue()
