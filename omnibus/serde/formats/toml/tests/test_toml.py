import os.path

from ....._vendor import antlr4
from .._antlr.TomlLexer import TomlLexer  # type: ignore
from .._antlr.TomlParser import TomlParser  # type: ignore
from .._antlr.TomlVisitor import TomlVisitor  # type: ignore


def test_toml():
    with open(os.path.join(os.path.dirname(__file__), 'examples/example1.toml'), 'r') as f:
        buf = f.read()
    lexer = TomlLexer(antlr4.InputStream(buf))
    stream = antlr4.CommonTokenStream(lexer)
    stream.fill()
    parser = TomlParser(stream)

    visitor = TomlVisitor()
    print(visitor.visit(parser.document()))