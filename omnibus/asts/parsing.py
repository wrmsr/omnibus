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

    def visitBinOpExprCont(self, left, conts, contfn):
        expr = check.isinstance(self.visit(left), n.Expr)
        for cont in conts:
            op = _get_enum_value(cont.op.text, n.BinOp)
            right = check.isinstance(self.visit(contfn(cont)), n.Expr)
            expr = n.BinExpr(expr, op, right)
        return expr

    def visitArithExpr(self, ctx: Python3Parser.ArithExprContext) -> n.Expr:
        return self.visitBinOpExprCont(ctx.term(), ctx.arithExprCont(), lambda c: c.term())

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

    def visitExpr(self, ctx: Python3Parser.ExprContext):
        return self.visitBinOpExprCont(ctx.xorExpr(), ctx.exprCont(), lambda c: c.xorExpr())

    def visitExprStmt(self, ctx: Python3Parser.ExprStmtContext) -> n.Stmt:
        expr = check.isinstance(self.visit(ctx.testListStarExpr()), n.Expr)
        cont = ctx.exprStmtCont()
        if isinstance(cont, Python3Parser.AnnAssignExprStmtContContext):
            pass
        elif isinstance(cont, Python3Parser.AugAssignExprStmtContContext):
            pass
        elif isinstance(cont, Python3Parser.AssignExprStmtContContext):
            if cont.children:
                check.state(len(cont.children) % 2 == 0)
                exprs = [expr]
                for eq, child in zip(cont.children[::2], cont.children[1::2]):
                    check.state(check.isinstance(eq, antlr4.TerminalNode).getText() == '=')
                    child_expr = check.isinstance(self.visit(child), n.Expr)
                    exprs.append(child_expr)
                stmt = n.Assign(exprs[:-1], exprs[-1])
            else:
                stmt = n.ExprStmt(expr)
        else:
            raise TypeError(cont)
        return stmt

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
