import typing as ta

from .... import antlr
from ...._vendor import antlr4
from ._antlr.DotLexer import DotLexer
from ._antlr.DotParser import DotParser
from ._antlr.DotVisitor import DotVisitor


class _ParseVisitor(DotVisitor):
    pass


def parse(buf: str) -> ta.Any:
    lexer = DotLexer(antlr4.InputStream(buf))
    lexer.removeErrorListeners()
    lexer.addErrorListener(antlr.SilentRaisingErrorListener())

    stream = antlr4.CommonTokenStream(lexer)
    stream.fill()

    parser = DotParser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(antlr.SilentRaisingErrorListener())

    visitor = _ParseVisitor()
    return visitor.visit(parser.graph())
