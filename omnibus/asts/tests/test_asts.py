import os.path

from ..._vendor import antlr4
from ..antlr.Python3Lexer import Python3Lexer
from ..antlr.Python3Listener import Python3Listener
from ..antlr.Python3Parser import Python3Parser


class Python3PrintListener(Python3Listener):

    def __init__(
            self,
            stream: antlr4.BufferedTokenStream.BufferedTokenStream,
            parser: Python3Parser
    ) -> None:
        super().__init__()
        self._stream = stream
        self._parser = parser

    def enterCompoundStmt(self, ctx: Python3Parser.CompoundStmtContext):
        print(ctx)
        print(ctx.start.tokenIndex)
        for t in (self._stream.getHiddenTokensToRight(ctx.start.tokenIndex, 2) or []):
            print(t.text)


def test_internal():
    with open(os.path.join(os.path.dirname(__file__), 'test_asts.py'), 'r') as f:
        buf = f.read()
    lexer = Python3Lexer(antlr4.InputStream(buf))
    stream = antlr4.CommonTokenStream(lexer)
    stream.fill()
    parser = Python3Parser(stream)
    tree = parser.fileInput()
    printer = Python3PrintListener(stream, parser)
    walker = antlr4.ParseTreeWalker()
    walker.walk(printer, tree)
