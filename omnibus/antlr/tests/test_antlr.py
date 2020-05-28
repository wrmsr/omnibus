import textwrap

from .. import antlr
from ._antlr.ChatLexer import ChatLexer
from ._antlr.ChatParser import ChatParser
from ._antlr.ChatVisitor import ChatVisitor


class MyVisitor(ChatVisitor):

    def visitCommand(self, ctx: ChatParser.CommandContext):
        print(ctx)
        return super().visitCommand(ctx)


def test_antlr():
    buf = textwrap.dedent("""
    barf says: hi // comment0
    // comment1
    xarf says: /* comment2 */ xi
    """).lstrip()

    parsed = antlr.parse(buf, ChatLexer, ChatParser)
    print(parsed)

    from pprint import pprint as pp
    pp(parsed.getTokenStream().tokenSource.inputStream)
    pp(parsed.getTokenStream().tokens)
    pp(parsed.getTokenStream().getText())
    MyVisitor().visit(parsed.chat())

    buf = textwrap.dedent("""
    barf says: hi
    xarf says: xi
    """).lstrip()

    parsed = antlr.parse(buf, ChatLexer, ChatParser)
    print(parsed)
    MyVisitor().visit(parsed.chat())
