import typing as ta

from . import nodes as no
from .. import antlr
from .. import check
from .. import dataclasses as dc
from .._vendor import antlr4
from ._antlr.Python3Lexer import Python3Lexer  # type: ignore
from ._antlr.Python3Parser import Python3Parser  # type: ignore
from ._antlr.Python3Visitor import Python3Visitor  # type: ignore


T = ta.TypeVar('T')


def _get_enum_value(value: ta.Any, cls: ta.Type[T]) -> T:
    return check.single([v for v in cls.__members__.values() if v.value == value])


class ArgList(ta.NamedTuple):
    args: ta.List[ta.Any]


class _ParseVisitor(Python3Visitor):

    def visit(self, ctx: antlr4.ParserRuleContext):
        check.isinstance(ctx, antlr4.ParserRuleContext)
        node = ctx.accept(self)
        if node is not None:
            # FIXME: ArgList is not a node
            # node = check.isinstance(node, no.Node)
            if isinstance(node, no.Node):
                if antlr4.ParserRuleContext not in node.meta:
                    node = dc.replace(node, meta={**node.meta, antlr4.ParserRuleContext: ctx})
        return node

    def aggregateResult(self, aggregate, nextResult):
        return check.one_of(aggregate, nextResult, not_none=True, default=None)

    def visitBinOpExprCont(self, left, conts, contfn):
        expr = check.isinstance(self.visit(left), no.Expr)
        for cont in conts:
            op = _get_enum_value(cont.op.text, no.BinOp)
            right = check.isinstance(self.visit(contfn(cont)), no.Expr)
            expr = no.BinExpr(expr, op, right)
        return expr

    def visitAndExpr(self, ctx: Python3Parser.AndExprContext):
        return self.visitBinOpExprCont(ctx.shiftExpr(), ctx.andExprCont(), lambda c: c.shiftExpr())

    def visitArgList(self, ctx: Python3Parser.ArgListContext):
        args = [check.isinstance(self.visit(arg), no.Expr) for arg in ctx.arg()]
        return ArgList(args)

    def visitArithExpr(self, ctx: Python3Parser.ArithExprContext) -> no.Expr:
        return self.visitBinOpExprCont(ctx.term(), ctx.arithExprCont(), lambda c: c.term())

    def visitAtomExpr(self, ctx: Python3Parser.AtomExprContext):
        if ctx.AWAIT() is not None:
            raise NotImplementedError
        expr = check.isinstance(self.visit(ctx.atom()), no.Expr)
        trailers = [self.visit(t) for t in ctx.trailer()]
        for trailer in trailers:
            if isinstance(trailer, ArgList):
                args = [check.isinstance(a, no.Expr) for a in trailer.args]
                expr = no.Call(expr, args)
            else:
                raise TypeError(trailer)
        return expr

    def visitBraacketAtom(self, ctx: Python3Parser.BraacketAtomContext):
        body = self.visit(ctx.testListComp())
        # FIXME: lol
        return no.List([body])

    def visitConst(self, ctx: Python3Parser.ConstContext):
        if ctx.NAME() is not None:
            return no.Name(ctx.NAME().getText())
        if ctx.NUMBER() is not None:
            txt = ctx.NUMBER().getText()
            try:
                val = int(txt)
            except ValueError:
                try:
                    val = float(txt)
                except ValueError:
                    val = complex(txt)
            return no.Constant(val)
        if ctx.STRING():
            return no.Constant(''.join(ctx.STRING()))
        txt = ctx.getText()
        if txt == '...':
            return no.Constant(Ellipsis)
        elif txt == 'None':
            return no.Constant(None)
        elif txt == 'True':
            return no.Constant(True)
        elif txt == 'False':
            return no.Constant(False)
        else:
            raise ValueError(ctx)

    def visitExpr(self, ctx: Python3Parser.ExprContext):
        return self.visitBinOpExprCont(ctx.xorExpr(), ctx.exprCont(), lambda c: c.xorExpr())

    def visitExprStmt(self, ctx: Python3Parser.ExprStmtContext) -> no.Stmt:
        expr = check.isinstance(self.visit(ctx.testListStarExpr()), no.Expr)
        cont = ctx.exprStmtCont()
        if isinstance(cont, Python3Parser.AnnAssignExprStmtContContext):
            raise NotImplementedError
        elif isinstance(cont, Python3Parser.AugAssignExprStmtContContext):
            raise NotImplementedError
        elif isinstance(cont, Python3Parser.AssignExprStmtContContext):
            if cont.children:
                check.state(len(cont.children) % 2 == 0)
                exprs = [expr]
                for eq, child in zip(cont.children[::2], cont.children[1::2]):
                    check.state(check.isinstance(eq, antlr4.TerminalNode).getText() == '=')
                    child_expr = check.isinstance(self.visit(child), no.Expr)
                    exprs.append(child_expr)
                stmt = no.Assign(exprs[:-1], exprs[-1])
            else:
                stmt = no.ExprStmt(expr)
        else:
            raise TypeError(cont)
        return stmt

    def visitFactor(self, ctx: Python3Parser.FactorContext):
        if ctx.factor() is not None:
            op = _get_enum_value(ctx.op.text, no.UnaryOp)
            value = self.visit(ctx.factor())
            return no.UnaryExpr(op, value)
        elif ctx.power() is not None:
            return self.visit(ctx.power())
        else:
            raise ValueError(ctx)

    def visitShiftExpr(self, ctx: Python3Parser.ShiftExprContext):
        return self.visitBinOpExprCont(ctx.arithExpr(), ctx.shiftExprCont(), lambda c: c.arithExpr())

    def visitXorExpr(self, ctx: Python3Parser.XorExprContext):
        return self.visitBinOpExprCont(ctx.andExpr(), ctx.xorExprCont(), lambda c: c.andExpr())


_ACCEL = True


def _parse(buf: str) -> Python3Parser:
    lexer = Python3Lexer(antlr4.InputStream(buf))
    lexer.removeErrorListeners()
    lexer.addErrorListener(antlr.SilentRaisingErrorListener())

    if _ACCEL:
        from ..antlr import _accel
        from .._vendor.antlr4.PredictionContext import PredictionContextCache
        lexer._interp = _accel.LexerATNSimulator(lexer, lexer.atn, lexer.decisionsToDFA, PredictionContextCache())
        lexer.decisionsToDFA = lexer._interp.decisionToDFA

    stream = antlr4.CommonTokenStream(lexer)
    stream.fill()

    parser = Python3Parser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(antlr.SilentRaisingErrorListener())

    return parser


def parse(buf: str) -> no.Node:
    parser = _parse(buf)
    visitor = _ParseVisitor()
    root = parser.singleInput()
    try:
        return visitor.visit(root)
    except Exception:
        print(antlr.pformat(root).getvalue())
        raise
