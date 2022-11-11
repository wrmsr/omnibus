import typing as ta

from .. import antlr
from .. import lang  # noqa
from .._vendor import antlr4
from ._antlr import GoLexer  # type: ignore
from ._antlr import GoParser  # type: ignore
from ._antlr import GoVisitor  # type: ignore


T = ta.TypeVar('T')


class _ParseVisitor(GoVisitor):

    def aggregateResult(self, aggregate, nextResult):
        # return lang.xor(aggregate, nextResult, test=lang.is_not_none)
        return super().aggregateResult(aggregate, nextResult)


def parse(buf: str) -> ta.Any:
    lexer = GoLexer(antlr4.InputStream(buf))  # type: ignore
    lexer.removeErrorListeners()
    lexer.addErrorListener(antlr.SilentRaisingErrorListener())

    stream = antlr4.CommonTokenStream(lexer)  # type: ignore
    stream.fill()

    parser = GoParser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(antlr.SilentRaisingErrorListener())

    visitor = _ParseVisitor()
    root = parser.sourceFile()
    print(antlr.pformat(root).getvalue())  # type: ignore
    return visitor.visit(root)
