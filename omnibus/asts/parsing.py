import typing as ta

from . import nodes as n
from .. import antlr
from .. import check
from .. import lang
from .._vendor import antlr4
from ._antlr.Python3Lexer import Python3Lexer
from ._antlr.Python3Parser import Python3Parser
from ._antlr.Python3Visitor import Python3Visitor


T = ta.TypeVar('T')


def _get_enum_value(value: ta.Any, cls: ta.Type[T]) -> T:
    return check.single([v for v in cls.__members__.values() if v.value == value])


class _ParseVisitor(Python3Visitor):

    def aggregateResult(self, aggregate, nextResult):
        return lang.xor(aggregate, nextResult, test=lang.is_not_none)

    def visitArithExpr(self, ctx: Python3Parser.ArithExprContext) -> n.Expr:
        expr = check.isinstance(self.visit(ctx.term()), n.Expr)
        for cont in ctx.arithExprCont():
            op = _get_enum_value(cont.op.text, n.BinOp)
            right = check.isinstance(self.visit(cont.term()), n.Expr)
            expr = n.BinExpr(expr, op, right)
        return expr

    def visitConst(self, ctx: Python3Parser.ConstContext):
        if ctx.NAME() is not None:
            return n.Name(ctx.NAME().getText())
        if ctx.NUMBER() is not None:
            txt = ctx.NUMBER().getText()
            try:
                val = int(txt)
            except ValueError:
                try:
                    val = float(txt)
                except ValueError:
                    val = complex(txt)
            return n.Constant(val)
        if ctx.STRING():
            return n.Constant(''.join(ctx.STRING()))
        txt = ctx.getText()
        if txt == '...':
            return n.Constant(Ellipsis)
        elif txt == 'None':
            return n.Constant(None)
        elif txt == 'True':
            return n.Constant(True)
        elif txt == 'False':
            return n.Constant(False)
        else:
            raise ValueError(ctx)

    def visitExprStmt(self, ctx: Python3Parser.ExprStmtContext):
        return super().visitExprStmt(ctx)

    def visitFactor(self, ctx: Python3Parser.FactorContext):
        if ctx.factor() is not None:
            op = _get_enum_value(ctx.op.text, n.UnaryOp)
            value = self.visit(ctx.factor())
            return n.UnaryExpr(op, value)
        elif ctx.power() is not None:
            return self.visit(ctx.power())
        else:
            raise ValueError(ctx)


def parse(buf: str) -> n.Node:
    lexer = Python3Lexer(antlr4.InputStream(buf))
    lexer.removeErrorListeners()
    lexer.addErrorListener(antlr.SilentRaisingErrorListener())

    stream = antlr4.CommonTokenStream(lexer)
    stream.fill()

    parser = Python3Parser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(antlr.SilentRaisingErrorListener())

    visitor = _ParseVisitor()
    root = parser.singleInput()
    print(antlr.pformat(root).getvalue())
    return visitor.visit(root)
