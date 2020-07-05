from . import nodes as n
from .. import antlr
from .._vendor import antlr4
from ._antlr.Python3Lexer import Python3Lexer
from ._antlr.Python3Parser import Python3Parser
from ._antlr.Python3Visitor import Python3Visitor


class _ParseVisitor(Python3Visitor):

    def visitArithExpr(self, ctx: Python3Parser.ArithExprContext) -> n.Node:
        return super().visitArithExpr(ctx)

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
    return visitor.visit(root)
