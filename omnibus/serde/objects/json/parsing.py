from ...._vendor import antlr4
from ._antlr.JsonLexer import JsonLexer  # type: ignore
from ._antlr.JsonParser import JsonParser  # type: ignore
from ._antlr.JsonVisitor import JsonVisitor  # type: ignore


def parse(buf):
    lexer = JsonLexer(antlr4.InputStream(buf))
    stream = antlr4.CommonTokenStream(lexer)
    stream.fill()
    parser = JsonParser(stream)

    visitor = JsonVisitor()
    return visitor.visit(parser.json())
