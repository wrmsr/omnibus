import typing as ta

from . import nodes as no
from .. import antlr
from .. import check
from .. import dataclasses as dc
from .._vendor import antlr4
from ._antlr import CLexer  # type: ignore
from ._antlr import CParser  # type: ignore
from ._antlr import CVisitor  # type: ignore


T = ta.TypeVar('T')


class _Temp(dc.Enum, reorder=True):
    ctx: ta.Optional[antlr4.ParserRuleContext] = dc.field(None, kwonly=True, check_type=(antlr4.ParserRuleContext, None))  # noqa


class _ParseVisitor(CVisitor):

    def visit(self, ctx: antlr4.ParserRuleContext):
        check.isinstance(ctx, antlr4.ParserRuleContext)
        ret = ctx.accept(self)
        if ret is not None:
            # FIXME: ArgList is not a node
            if isinstance(ret, no.Node):
                if antlr4.ParserRuleContext not in ret.meta:
                    ret = dc.replace(ret, meta={**ret.meta, antlr4.ParserRuleContext: ctx})
            elif isinstance(ret, _Temp):
                if ret.ctx is None:
                    ret = dc.replace(ret, ctx=ctx)
            else:
                raise TypeError(ret)

        return ret

    def aggregateResult(self, aggregate, nextResult):
        return check.one_of(aggregate, nextResult, not_none=True, default=None)


def _parse(buf: str) -> CParser:
    lexer = CLexer(antlr4.InputStream(buf))
    lexer.removeErrorListeners()
    lexer.addErrorListener(antlr.SilentRaisingErrorListener())

    stream = antlr4.CommonTokenStream(lexer)
    stream.fill()

    parser = CParser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(antlr.SilentRaisingErrorListener())

    return parser


def parse(buf: str) -> no.Node:
    parser = _parse(buf)
    visitor = _ParseVisitor()
    root = parser.compilationUnit()

    try:
        return visitor.visit(root)
    except Exception:
        print(antlr.pformat(root).getvalue())
        raise
