import os.path

from ..._vendor import antlr4
from .._antlr.ThriftLexer import ThriftLexer  # type: ignore
from .._antlr.ThriftListener import ThriftListener  # type: ignore
from .._antlr.ThriftParser import ThriftParser  # type: ignore


class ThriftPrintListener(ThriftListener):

    def __init__(
            self,
            stream: antlr4.BufferedTokenStream.BufferedTokenStream,
            parser: ThriftParser
    ) -> None:
        super().__init__()
        self._stream = stream
        self._parser = parser

    def enterService(self, ctx: ThriftParser.ServiceContext):
        print(ctx)
        print(ctx.start.tokenIndex)
        for t in (self._stream.getHiddenTokensToRight(ctx.start.tokenIndex, 2) or []):
            print(t.text)

    def enterField(self, ctx: ThriftParser.FieldContext):
        print(ctx)
        print(ctx.start.tokenIndex)
        for t in (self._stream.getHiddenTokensToRight(ctx.start.tokenIndex, 2) or []):
            print(t.text)


def test_thrift():
    with open(os.path.join(os.path.dirname(__file__), 'examples/example.thrift'), 'r') as f:
        buf = f.read()
    lexer = ThriftLexer(antlr4.InputStream(buf))
    stream = antlr4.CommonTokenStream(lexer)
    stream.fill()
    parser = ThriftParser(stream)
    tree = parser.document()
    printer = ThriftPrintListener(stream, parser)
    walker = antlr4.ParseTreeWalker()
    walker.walk(printer, tree)
