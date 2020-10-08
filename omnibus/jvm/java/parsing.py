import typing as ta

from ... import antlr
from ... import lang  # noqa
from ..._vendor import antlr4
from ._antlr.Java8Lexer import Java8Lexer  # type: ignore
from ._antlr.Java8Parser import Java8Parser  # type: ignore
from ._antlr.Java8Visitor import Java8Visitor  # type: ignore


T = ta.TypeVar('T')


class _ParseVisitor(Java8Visitor):

    def aggregateResult(self, aggregate, nextResult):
        # return lang.xor(aggregate, nextResult, test=lang.is_not_none)
        return super().aggregateResult(aggregate, nextResult)


def parse(buf: str) -> ta.Any:
    lexer = Java8Lexer(antlr4.InputStream(buf))
    lexer.removeErrorListeners()
    lexer.addErrorListener(antlr.SilentRaisingErrorListener())

    stream = antlr4.CommonTokenStream(lexer)
    stream.fill()

    parser = Java8Parser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(antlr.SilentRaisingErrorListener())

    visitor = _ParseVisitor()
    root = parser.compilationUnit()
    print(antlr.pformat(root).getvalue())
    return visitor.visit(root)
