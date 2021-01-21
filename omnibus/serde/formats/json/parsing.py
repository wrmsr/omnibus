from ...._vendor import antlr4
from ._antlr import JsonLexer  # type: ignore
from ._antlr import JsonParser  # type: ignore
from ._antlr import JsonVisitor  # type: ignore


def parse(buf):
    lexer = JsonLexer(antlr4.InputStream(buf))
    stream = antlr4.CommonTokenStream(lexer)
    stream.fill()
    parser = JsonParser(stream)

    visitor = JsonVisitor()
    return visitor.visit(parser.json())
