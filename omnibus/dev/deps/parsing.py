import typing as ta

from ... import antlr
from ... import check
from ... import dataclasses as dc
from ..._vendor import antlr4
from ._antlr.Pep508Lexer import Pep508Lexer  # type: ignore
from ._antlr.Pep508Parser import Pep508Parser  # type: ignore
from ._antlr.Pep508Visitor import Pep508Visitor  # type: ignore


T = ta.TypeVar('T')


def _get_enum_value(value: ta.Any, cls: ta.Type[T]) -> T:
    return check.single([v for v in cls.__members__.values() if v.value == value])


class Version(dc.Pure):
    op: str
    val: str


class NameDep(dc.Pure):
    name: str
    extras: ta.Sequence[str]
    vers: ta.Sequence[Version]


class _ParseVisitor(Pep508Visitor):

    def aggregateResult(self, aggregate, nextResult):
        return check.one_of(aggregate, nextResult, not_none=True, default=None)

    def visitExtrasList(self, ctx: Pep508Parser.ExtrasListContext):
        return [self.visit(e) for e in ctx.identifier()]

    def visitIdentifier(self, ctx: Pep508Parser.IdentifierContext):
        return ctx.getText()

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
