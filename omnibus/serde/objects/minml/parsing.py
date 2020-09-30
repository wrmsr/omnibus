"""
TODO:
 - codify yaml interop - special idents?
  - ** REJECT ** ambiguous idents? also yaml control codes and shit
 - json5? https://json5.org/ - doesn't do default_object_value tho

https://golang.org/pkg/reflect/#StructTag lol
/*+ materialization: {wait_time_s: 3600} */
"""
import typing as ta

from .... import antlr
from .... import check
from .... import lang
from ...._vendor import antlr4
from ._antlr.MinmlLexer import MinmlLexer
from ._antlr.MinmlParser import MinmlParser
from ._antlr.MinmlVisitor import MinmlVisitor


class NULL(lang.Marker):
    pass


class _ParseVisitor(MinmlVisitor):

    def __init__(
            self,
            *,
            null_value: ta.Any = NULL,
            default_object_value: ta.Any = True,
            non_strict_keys: bool = False,
    ) -> None:
        super().__init__()

        self._null_value = null_value
        self._default_object_value = default_object_value
        self._non_strict_keys = non_strict_keys

    def visit(self, ctx: antlr4.ParserRuleContext):
        check.isinstance(ctx, antlr4.ParserRuleContext)
        return ctx.accept(self)

    def aggregateResult(self, aggregate, nextResult):
        if aggregate is not None:
            check.none(nextResult)
            return aggregate
        else:
            check.none(aggregate)
            return nextResult

    def visitArray(self, ctx: MinmlParser.ArrayContext):
        return [self.visit(e) for e in ctx.value()]

    def visitFalse(self, ctx: MinmlParser.FalseContext):
        return False

    def visitIdentifier(self, ctx:MinmlParser.IdentifierContext):
        return ctx.IDENTIFIER().getText()

    def visitNull(self, ctx: MinmlParser.NullContext):
        return self._null_value

    def visitNumber(self, ctx: MinmlParser.NumberContext):
        txt = ctx.getText()
        if txt.startswith('0x'):
            return int(txt, 16)
        elif '.' in txt:
            return float(txt)
        else:
            return int(txt)

    def visitObj(self, ctx: MinmlParser.ObjContext):
        dct = {}
        for pair in ctx.pair():
            key, value = self.visit(pair)
            if not self._non_strict_keys:
                check.not_in(key, dct)
            dct[key] = value
        return dct

    def visitPair(self, ctx: MinmlParser.PairContext):
        key = self.visit(ctx.k)
        value = self.visit(ctx.v) if ctx.v is not None else self._default_object_value
        return key, value

    def visitTrue(self, ctx: MinmlParser.TrueContext):
        return True

    def visitString(self, ctx: MinmlParser.StringContext):
        txt = ctx.getText()
        check.state(
            (txt.startswith('"') and txt.endswith('"')) or
            (txt.startswith("'") and txt.endswith("'")))
        return txt[1:-1]


def parse(buf: str) -> ta.Any:
    lexer = MinmlLexer(antlr4.InputStream(buf))
    lexer.removeErrorListeners()
    lexer.addErrorListener(antlr.SilentRaisingErrorListener())

    stream = antlr4.CommonTokenStream(lexer)
    stream.fill()

    parser = MinmlParser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(antlr.SilentRaisingErrorListener())

    visitor = _ParseVisitor()
    return check.not_none(visitor.visit(parser.root()))
