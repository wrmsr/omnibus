import os.path

from ..._vendor import antlr4
from .._antlr.GraphqlLexer import GraphqlLexer
from .._antlr.GraphqlListener import GraphqlListener
from .._antlr.GraphqlParser import GraphqlParser


class GraphqlPrintListener(GraphqlListener):

    def __init__(
            self,
            stream: antlr4.BufferedTokenStream.BufferedTokenStream,
            parser: GraphqlParser
    ) -> None:
        super().__init__()
        self._stream = stream
        self._parser = parser

    def enterField(self, ctx: GraphqlParser.FieldContext):
        print(ctx)
        print(ctx.start.tokenIndex)
        for t in (self._stream.getHiddenTokensToRight(ctx.start.tokenIndex, 2) or []):
            print(t.text)


def test_graphql():
    with open(os.path.join(os.path.dirname(__file__), 'examples/example.graphql'), 'r') as f:
        buf = f.read()
    lexer = GraphqlLexer(antlr4.InputStream(buf))
    stream = antlr4.CommonTokenStream(lexer)
    stream.fill()
    parser = GraphqlParser(stream)
    tree = parser.document()
    printer = GraphqlPrintListener(stream, parser)
    walker = antlr4.ParseTreeWalker()
    walker.walk(printer, tree)
