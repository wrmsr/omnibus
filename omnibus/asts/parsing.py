import typing as ta

from . import nodes as no
from .. import antlr
from .. import check
from .. import collections as col
from .. import dataclasses as dc
from .. import lang
from .._vendor import antlr4
from ._antlr import Python3Lexer  # type: ignore
from ._antlr import Python3Parser  # type: ignore
from ._antlr import Python3Visitor  # type: ignore


T = ta.TypeVar('T')


class _Temp(dc.Enum, reorder=True):
    ctx: ta.Optional[antlr4.ParserRuleContext] = dc.field(None, kwonly=True, check_type=(antlr4.ParserRuleContext, None))  # noqa


class _Exprs(_Temp):
    args: ta.List[no.Expr] = dc.field(coerce=col.seq_of(check.of_isinstance(no.Expr)))


class _ParseVisitor(Python3Visitor):

    def visit(self, ctx: antlr4.ParserRuleContext):
        check.isinstance(ctx, antlr4.ParserRuleContext)
        ret = ctx.accept(self)
        if ret is not None:
            # FIXME: ArgList is not a node
            if isinstance(ret, no.Node):
                if antlr4.ParserRuleContext not in ret.meta:
                    ret = dc.replace(ret, meta={**ret.meta, antlr4.ParserRuleContext: ctx})
            elif isinstance(ret, _Temp):
                if ret.ctx is None:
                    ret = dc.replace(ret, ctx=ctx)
            else:
                raise TypeError(ret)

        return ret

    def aggregateResult(self, aggregate, nextResult):
        return check.one_of(aggregate, nextResult, not_none=True, default=None)

    def visitBinOpExprCont(self, left, conts, contfn):
        expr = check.isinstance(self.visit(left), no.Expr)
        for cont in conts:
            op = no.OPS_BY_GLYPH_BY_CLS[no.BinOp][cont.op.text]
            right = check.isinstance(self.visit(contfn(cont)), no.Expr)
            expr = no.BinExpr(expr, op, right)
        return expr

    def visitAndExpr(self, ctx: Python3Parser.AndExprContext):
        return self.visitBinOpExprCont(ctx.shiftExpr(), ctx.andExprCont(), lambda c: c.shiftExpr())

    def visitArgList(self, ctx: Python3Parser.ArgListContext):
        args = [check.isinstance(self.visit(arg), no.Expr) for arg in ctx.arg()]
        return _Exprs(args)

    def visitArithExpr(self, ctx: Python3Parser.ArithExprContext) -> no.Expr:
        return self.visitBinOpExprCont(ctx.term(), ctx.arithExprCont(), lambda c: c.term())

    def visitAtomExpr(self, ctx: Python3Parser.AtomExprContext):
        if ctx.AWAIT() is not None:
            raise NotImplementedError
        expr = check.isinstance(self.visit(ctx.atom()), no.Expr)
        trailers = [self.visit(t) for t in ctx.trailer()]
        for trailer in trailers:
            if isinstance(trailer, _Exprs):
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
            op = no.OPS_BY_GLYPH_BY_CLS[no.UnaryOp][ctx.op.text]
            value = self.visit(ctx.factor())
            return no.UnaryExpr(op, value)
        elif ctx.power() is not None:
            return self.visit(ctx.power())
        else:
            raise ValueError(ctx)

    def visitFileInput(self, ctx: Python3Parser.FileInputContext):
        stmts = [self.visit(s) for s in ctx.stmt()]
        return no.Body(stmts)

    def visitFuncDef(self, ctx: Python3Parser.FuncDefContext):
        args = check.isinstance(self.visit(ctx.parameters()), no.Args)
        returns = self.visit(ctx.test()) if ctx.test() is not None else None
        body = check.isinstance(self.visit(ctx.suite()), no.Stmt)
        return no.FunctionDef(
            name=ctx.NAME().getText(),
            args=args,
            body=[body],
            returns=returns,
        )

    def visitReturnStmt(self, ctx: Python3Parser.ReturnStmtContext):
        value = check.isinstance(self.visit(ctx.testList()), no.Expr) if ctx.testList() is not None else None
        return no.Return(value)

    def visitShiftExpr(self, ctx: Python3Parser.ShiftExprContext):
        return self.visitBinOpExprCont(ctx.arithExpr(), ctx.shiftExprCont(), lambda c: c.arithExpr())

    def visitSuite(self, ctx: Python3Parser.SuiteContext):
        if ctx.simpleStmt() is not None:
            check.state(not ctx.stmt())
            return check.isinstance(self.visit(ctx.simpleStmt()), no.Stmt)
        else:
            stmts = [self.visit(s) for s in ctx.stmt()]
            return no.Body(stmts)

    def visitTpDef(self, ctx: Python3Parser.TpDefContext):
        ann = self.visit(ctx.test()) if ctx.test() is not None else None
        return no.Arg(ctx.NAME().getText(), annotation=ann)

    def visitTpDefTest(self, ctx: Python3Parser.TpDefTestContext):
        arg = check.isinstance(self.visit(ctx.tpDef()), no.Arg)
        check.none(arg.default)
        default = check.isinstance(self.visit(ctx.test()), no.Expr) if ctx.test() is not None else None
        return dc.replace(arg, default=default)

    def visitTypedArgsList(self, ctx: Python3Parser.TypedArgsListContext):
        a0 = check.isinstance(self.visit(ctx.a0), no.Arg) if ctx.a0 is not None else None
        l0 = [check.isinstance(self.visit(a), no.Arg) for a in ctx.l0.tpDefTest()] if ctx.l0 is not None else None
        va = check.isinstance(self.visit(ctx.va), no.Arg) if ctx.va is not None else None
        l1 = [check.isinstance(self.visit(a), no.Arg) for a in ctx.l1.tpDefTest()] if ctx.l1 is not None else None
        vk = check.isinstance(self.visit(ctx.vk), no.Arg) if ctx.vk is not None else None
        l2 = [check.isinstance(self.visit(a), no.Arg) for a in ctx.l2.tpDefTest()] if ctx.l2 is not None else None

        if va is not None:
            check.none(va.default)
        if vk is not None:
            check.none(vk.default)

        if a0 is not None:
            check.none(l2)
            return no.Args(
                args=[a0, *(l0 or [])],
                vararg=va,
                kwonly_args=l1 or [],
                kwarg=vk,
            )

        else:
            raise NotImplementedError

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


class ParseMode(lang.AutoEnum):
    INPUT = ...
    FILE = ...
    EVAL = ...


def _get_parse_root(parser: Python3Parser, mode: ta.Union[ParseMode, str]) -> antlr4.ParserRuleContext:
    if isinstance(mode, str):
        mode = ParseMode[mode.upper()]
    elif not isinstance(mode, ParseMode):
        raise TypeError(mode)

    if mode == ParseMode.INPUT:
        return parser.singleInput()
    elif mode == ParseMode.FILE:
        return parser.fileInput()
    elif mode == ParseMode.EVAL:
        return parser.evalInput()
    else:
        raise ValueError(mode)


def parse(buf: str, mode: ta.Union[ParseMode, str] = ParseMode.INPUT) -> no.Node:
    parser = _parse(buf)
    visitor = _ParseVisitor()
    root = _get_parse_root(parser, mode)

    try:
        return visitor.visit(root)
    except Exception:
        print(antlr.pformat(root).getvalue())
        raise
