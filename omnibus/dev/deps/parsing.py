"""
TODO:
 - comments, hot comments
 - rendering, identical output
 - link peps in g4
"""
import typing as ta

from ... import antlr
from ... import check
from ... import dataclasses as dc
from ... import dispatch
from ..._vendor import antlr4
from ._antlr.Pep508Lexer import Pep508Lexer  # type: ignore
from ._antlr.Pep508Parser import Pep508Parser  # type: ignore
from ._antlr.Pep508Visitor import Pep508Visitor  # type: ignore


T = ta.TypeVar('T')


def _get_enum_value(value: ta.Any, cls: ta.Type[T]) -> T:
    return check.single([v for v in cls.__members__.values() if v.value == value])


class Node(dc.Enum):
    pass


class Version(Node):
    op: str
    val: str


class NameDep(Node):
    name: str
    extras: ta.Sequence[str]
    vers: ta.Sequence[Version]
    marker: ta.Optional['Marker'] = None


class Marker(Node, abstract=True):
    pass


class MarkerAnd(Marker):
    left: Marker
    right: Marker


class MarkerOr(Marker):
    left: Marker
    right: Marker


class MarkerExpr(Marker):
    left: str
    op: str
    right: str


class Renderer(dispatch.Class):
    __call__ = dispatch.property()

    def __call__(self, node: Node) -> str:  # noqa
        raise TypeError(node)

    def __call__(self, node: MarkerAnd) -> str:  # noqa
        raise NotImplementedError

    def __call__(self, node: MarkerExpr) -> str:  # noqa
        raise NotImplementedError

    def __call__(self, node: MarkerOr) -> str:  # noqa
        raise NotImplementedError

    def __call__(self, node: NameDep) -> str:  # noqa
        return ''.join([
            node.name,
            ('[' + ','.join(e for e in node.extras) + ']') if node.extras else '',
            ','.join(self(v) for v in node.vers),
            ('; ' + self(node.marker)) if node.marker is not None else '',
        ])

    def __call__(self, node: Version) -> str:  # noqa
        return node.op + node.val


def render(node: Node) -> str:
    return Renderer()(node)


class _ParseVisitor(Pep508Visitor):

    def aggregateResult(self, aggregate, nextResult):
        return check.one_of(aggregate, nextResult, not_none=True, default=None)

    def visitExtrasList(self, ctx: Pep508Parser.ExtrasListContext):
        return [self.visit(e) for e in ctx.identifier()]

    def visitIdentifier(self, ctx: Pep508Parser.IdentifierContext):
        return ctx.getText()

    def visitMarkerAnd(self, ctx: Pep508Parser.MarkerAndContext):
        if len(ctx.markerExpr()) >= 1:
            return MarkerAnd(*[self.visit(m) for m in ctx.markerExpr()])
        else:
            return self.visit(check.single(ctx.markerExpr()))

    def visitMarkerExpr(self, ctx: Pep508Parser.MarkerExprContext):
        if ctx.markerOp() is not None:
            left, right = [m.getText() for m in ctx.markerVar()]
            op = ctx.markerOp().getText()
            return MarkerExpr(
                left=left,
                op=op,
                right=right,
            )
        else:
            return self.visit(ctx.marker())

    def visitMarkerOr(self, ctx: Pep508Parser.MarkerOrContext):
        if len(ctx.markerAnd()) >= 1:
            return MarkerOr(*[self.visit(m) for m in ctx.markerAnd()])
        else:
            return self.visit(check.single(ctx.markerAnd()))

    def visitNameReq(self, ctx: Pep508Parser.NameReqContext):
        name = self.visit(ctx.name())
        extras = self.visit(ctx.extras()) if ctx.extras() else []
        vers = self.visit(ctx.versionspec()) if ctx.versionspec() else []
        return NameDep(
            name=name,
            extras=extras,
            vers=vers,
        )

    def visitVersionMany(self, ctx: Pep508Parser.VersionManyContext):
        return [self.visit(v) for v in ctx.versionOne()]

    def visitVersionOne(self, ctx: Pep508Parser.VersionOneContext):
        op = ctx.versionCmp().getText()
        val = ctx.version().getText()
        return Version(
            op=op,
            val=val,
        )


def _parse(buf: str) -> Pep508Parser:
    lexer = Pep508Lexer(antlr4.InputStream(buf))
    lexer.removeErrorListeners()
    lexer.addErrorListener(antlr.SilentRaisingErrorListener())

    stream = antlr4.CommonTokenStream(lexer)
    stream.fill()

    parser = Pep508Parser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(antlr.SilentRaisingErrorListener())

    return parser


def parse(buf: str) -> ta.Any:
    parser = _parse(buf)
    visitor = _ParseVisitor()
    root = parser.spec()
    return visitor.visit(root)
