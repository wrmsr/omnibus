from . import nodes as n
from .. import antlr
from .._vendor import antlr4
from ._antlr.Python3Lexer import Python3Lexer
from ._antlr.Python3Parser import Python3Parser
from ._antlr.Python3Visitor import Python3Visitor


class _ParseVisitor(Python3Visitor):

    def visitArithExpr(self, ctx: Python3Parser.ArithExprContext) -> n.Node:
        return super().visitArithExpr(ctx)


def parse(buf: str) -> n.Node:
    lexer = Python3Lexer(antlr4.InputStream(buf))
    lexer.removeErrorListeners()
    lexer.addErrorListener(antlr.SilentRaisingErrorListener())

    stream = antlr4.CommonTokenStream(lexer)
    stream.fill()

    parser = Python3Parser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(antlr.SilentRaisingErrorListener())

    visitor = _ParseVisitor()
    return visitor.visit(parser.singleInput())
