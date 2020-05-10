import os.path

from ..._vendor import antlr4
from .._antlr.GraphQlLexer import GraphQlLexer
from .._antlr.GraphQlListener import GraphQlListener
from .._antlr.GraphQlParser import GraphQlParser


class GraphQlPrintListener(GraphQlListener):

    def __init__(
            self,
            stream: antlr4.BufferedTokenStream.BufferedTokenStream,
            parser: GraphQlParser
    ) -> None:
        super().__init__()
        self._stream = stream
        self._parser = parser

    def enterField(self, ctx: GraphQlParser.FieldContext):
        print(ctx)
        print(ctx.start.tokenIndex)
        for t in (self._stream.getHiddenTokensToRight(ctx.start.tokenIndex, 2) or []):
            print(t.text)


def test_graphql():
    with open(os.path.join(os.path.dirname(__file__), 'examples/example.graphql'), 'r') as f:
        buf = f.read()
    lexer = GraphQlLexer(antlr4.InputStream(buf))
    stream = antlr4.CommonTokenStream(lexer)
    stream.fill()
    parser = GraphQlParser(stream)
    tree = parser.document()
    printer = GraphQlPrintListener(stream, parser)
    walker = antlr4.ParseTreeWalker()
    walker.walk(printer, tree)
