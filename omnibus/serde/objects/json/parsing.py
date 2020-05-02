from ...._vendor import antlr4
from .antlr.JsonLexer import JsonLexer
from .antlr.JsonParser import JsonParser
from .antlr.JsonVisitor import JsonVisitor


def parse(buf):
    lexer = JsonLexer(antlr4.InputStream(buf))
    stream = antlr4.CommonTokenStream(lexer)
    stream.fill()
    parser = JsonParser(stream)

    visitor = JsonVisitor()
    return visitor.visit(parser.json())
