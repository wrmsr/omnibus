import os.path

from ....._vendor import antlr4
from ..antlr.JsonLexer import JsonLexer
from ..antlr.JsonParser import JsonParser
from ..antlr.JsonVisitor import JsonVisitor


def test_json():
    with open(os.path.join(os.path.dirname(__file__), 'examples/example2.json'), 'r') as f:
        buf = f.read()
    lexer = JsonLexer(antlr4.InputStream(buf))
    stream = antlr4.CommonTokenStream(lexer)
    stream.fill()
    parser = JsonParser(stream)

    visitor = JsonVisitor()
    print(visitor.visit(parser.json()))
