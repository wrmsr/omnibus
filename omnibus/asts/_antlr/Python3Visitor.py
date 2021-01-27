# flake8: noqa
# type: ignore
# Generated from Python3.g4 by ANTLR 4.8
from ..._vendor.antlr4 import *
if __name__ is not None and "." in __name__:
    from .Python3Parser import Python3Parser
else:
    from Python3Parser import Python3Parser

# This class defines a complete generic visitor for a parse tree produced by Python3Parser.

class Python3Visitor(ParseTreeVisitor):

    # Visit a parse tree produced by Python3Parser#singleInput.
    def visitSingleInput(self, ctx:Python3Parser.SingleInputContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#fileInput.
    def visitFileInput(self, ctx:Python3Parser.FileInputContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#evalInput.
    def visitEvalInput(self, ctx:Python3Parser.EvalInputContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#decorator.
    def visitDecorator(self, ctx:Python3Parser.DecoratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#decorators.
    def visitDecorators(self, ctx:Python3Parser.DecoratorsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#decorated.
    def visitDecorated(self, ctx:Python3Parser.DecoratedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#asyncFuncDef.
    def visitAsyncFuncDef(self, ctx:Python3Parser.AsyncFuncDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#funcDef.
    def visitFuncDef(self, ctx:Python3Parser.FuncDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#parameters.
    def visitParameters(self, ctx:Python3Parser.ParametersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#typedArgsList.
    def visitTypedArgsList(self, ctx:Python3Parser.TypedArgsListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#tpDefTestList.
    def visitTpDefTestList(self, ctx:Python3Parser.TpDefTestListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#tpDefTest.
    def visitTpDefTest(self, ctx:Python3Parser.TpDefTestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#tpDef.
    def visitTpDef(self, ctx:Python3Parser.TpDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#varargsList.
    def visitVarargsList(self, ctx:Python3Parser.VarargsListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#vfpDef.
    def visitVfpDef(self, ctx:Python3Parser.VfpDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#stmt.
    def visitStmt(self, ctx:Python3Parser.StmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#simpleStmt.
    def visitSimpleStmt(self, ctx:Python3Parser.SimpleStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#smallStmt.
    def visitSmallStmt(self, ctx:Python3Parser.SmallStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#exprStmt.
    def visitExprStmt(self, ctx:Python3Parser.ExprStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#annAssignExprStmtCont.
    def visitAnnAssignExprStmtCont(self, ctx:Python3Parser.AnnAssignExprStmtContContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#augAssignExprStmtCont.
    def visitAugAssignExprStmtCont(self, ctx:Python3Parser.AugAssignExprStmtContContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#assignExprStmtCont.
    def visitAssignExprStmtCont(self, ctx:Python3Parser.AssignExprStmtContContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#annAssign.
    def visitAnnAssign(self, ctx:Python3Parser.AnnAssignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#testListStarExpr.
    def visitTestListStarExpr(self, ctx:Python3Parser.TestListStarExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#augAssign.
    def visitAugAssign(self, ctx:Python3Parser.AugAssignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#delStmt.
    def visitDelStmt(self, ctx:Python3Parser.DelStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#passStmt.
    def visitPassStmt(self, ctx:Python3Parser.PassStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#flowStmt.
    def visitFlowStmt(self, ctx:Python3Parser.FlowStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#breakStmt.
    def visitBreakStmt(self, ctx:Python3Parser.BreakStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#continueStmt.
    def visitContinueStmt(self, ctx:Python3Parser.ContinueStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#returnStmt.
    def visitReturnStmt(self, ctx:Python3Parser.ReturnStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#yieldStmt.
    def visitYieldStmt(self, ctx:Python3Parser.YieldStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#raiseStmt.
    def visitRaiseStmt(self, ctx:Python3Parser.RaiseStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#importStmt.
    def visitImportStmt(self, ctx:Python3Parser.ImportStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#importName.
    def visitImportName(self, ctx:Python3Parser.ImportNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#importFrom.
    def visitImportFrom(self, ctx:Python3Parser.ImportFromContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#importAsName.
    def visitImportAsName(self, ctx:Python3Parser.ImportAsNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#dottedAsName.
    def visitDottedAsName(self, ctx:Python3Parser.DottedAsNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#importAsNames.
    def visitImportAsNames(self, ctx:Python3Parser.ImportAsNamesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#dottedAsNames.
    def visitDottedAsNames(self, ctx:Python3Parser.DottedAsNamesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#dottedName.
    def visitDottedName(self, ctx:Python3Parser.DottedNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#globalStmt.
    def visitGlobalStmt(self, ctx:Python3Parser.GlobalStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#nonlocalStmt.
    def visitNonlocalStmt(self, ctx:Python3Parser.NonlocalStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#assertStmt.
    def visitAssertStmt(self, ctx:Python3Parser.AssertStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#compoundStmt.
    def visitCompoundStmt(self, ctx:Python3Parser.CompoundStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#asyncStmt.
    def visitAsyncStmt(self, ctx:Python3Parser.AsyncStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#ifStmt.
    def visitIfStmt(self, ctx:Python3Parser.IfStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#whileStmt.
    def visitWhileStmt(self, ctx:Python3Parser.WhileStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#forStmt.
    def visitForStmt(self, ctx:Python3Parser.ForStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#tryStmt.
    def visitTryStmt(self, ctx:Python3Parser.TryStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#withStmt.
    def visitWithStmt(self, ctx:Python3Parser.WithStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#withItem.
    def visitWithItem(self, ctx:Python3Parser.WithItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#exceptClause.
    def visitExceptClause(self, ctx:Python3Parser.ExceptClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#suite.
    def visitSuite(self, ctx:Python3Parser.SuiteContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#test.
    def visitTest(self, ctx:Python3Parser.TestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#testNoCond.
    def visitTestNoCond(self, ctx:Python3Parser.TestNoCondContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#lambaDef.
    def visitLambaDef(self, ctx:Python3Parser.LambaDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#lambaDefNoCond.
    def visitLambaDefNoCond(self, ctx:Python3Parser.LambaDefNoCondContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#orTest.
    def visitOrTest(self, ctx:Python3Parser.OrTestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#andTest.
    def visitAndTest(self, ctx:Python3Parser.AndTestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#notTest.
    def visitNotTest(self, ctx:Python3Parser.NotTestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#comparison.
    def visitComparison(self, ctx:Python3Parser.ComparisonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#compOp.
    def visitCompOp(self, ctx:Python3Parser.CompOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#starExpr.
    def visitStarExpr(self, ctx:Python3Parser.StarExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#expr.
    def visitExpr(self, ctx:Python3Parser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#exprCont.
    def visitExprCont(self, ctx:Python3Parser.ExprContContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#xorExpr.
    def visitXorExpr(self, ctx:Python3Parser.XorExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#xorExprCont.
    def visitXorExprCont(self, ctx:Python3Parser.XorExprContContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#andExpr.
    def visitAndExpr(self, ctx:Python3Parser.AndExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#andExprCont.
    def visitAndExprCont(self, ctx:Python3Parser.AndExprContContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#shiftExpr.
    def visitShiftExpr(self, ctx:Python3Parser.ShiftExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#shiftExprCont.
    def visitShiftExprCont(self, ctx:Python3Parser.ShiftExprContContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#arithExpr.
    def visitArithExpr(self, ctx:Python3Parser.ArithExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#arithExprCont.
    def visitArithExprCont(self, ctx:Python3Parser.ArithExprContContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#term.
    def visitTerm(self, ctx:Python3Parser.TermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#termCont.
    def visitTermCont(self, ctx:Python3Parser.TermContContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#factor.
    def visitFactor(self, ctx:Python3Parser.FactorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#power.
    def visitPower(self, ctx:Python3Parser.PowerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#atomExpr.
    def visitAtomExpr(self, ctx:Python3Parser.AtomExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#parenAtom.
    def visitParenAtom(self, ctx:Python3Parser.ParenAtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#braacketAtom.
    def visitBraacketAtom(self, ctx:Python3Parser.BraacketAtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#dictOrSetAtom.
    def visitDictOrSetAtom(self, ctx:Python3Parser.DictOrSetAtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#constAtom.
    def visitConstAtom(self, ctx:Python3Parser.ConstAtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#const.
    def visitConst(self, ctx:Python3Parser.ConstContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#testListComp.
    def visitTestListComp(self, ctx:Python3Parser.TestListCompContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#trailer.
    def visitTrailer(self, ctx:Python3Parser.TrailerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#subscriptList.
    def visitSubscriptList(self, ctx:Python3Parser.SubscriptListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#subscript.
    def visitSubscript(self, ctx:Python3Parser.SubscriptContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#sliceOp.
    def visitSliceOp(self, ctx:Python3Parser.SliceOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#exprList.
    def visitExprList(self, ctx:Python3Parser.ExprListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#testList.
    def visitTestList(self, ctx:Python3Parser.TestListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#dictOrSetMaker.
    def visitDictOrSetMaker(self, ctx:Python3Parser.DictOrSetMakerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#classDef.
    def visitClassDef(self, ctx:Python3Parser.ClassDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#argList.
    def visitArgList(self, ctx:Python3Parser.ArgListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#simpleArg.
    def visitSimpleArg(self, ctx:Python3Parser.SimpleArgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#compArg.
    def visitCompArg(self, ctx:Python3Parser.CompArgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#valueArg.
    def visitValueArg(self, ctx:Python3Parser.ValueArgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#starsArg.
    def visitStarsArg(self, ctx:Python3Parser.StarsArgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#starArg.
    def visitStarArg(self, ctx:Python3Parser.StarArgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#compIter.
    def visitCompIter(self, ctx:Python3Parser.CompIterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#compFor.
    def visitCompFor(self, ctx:Python3Parser.CompForContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#compIf.
    def visitCompIf(self, ctx:Python3Parser.CompIfContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#encodingDecl.
    def visitEncodingDecl(self, ctx:Python3Parser.EncodingDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#yieldExpr.
    def visitYieldExpr(self, ctx:Python3Parser.YieldExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#yieldArg.
    def visitYieldArg(self, ctx:Python3Parser.YieldArgContext):
        return self.visitChildren(ctx)



del Python3Parser
