# flake8: noqa
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


    # Visit a parse tree produced by Python3Parser#asyncFuncdef.
    def visitAsyncFuncdef(self, ctx:Python3Parser.AsyncFuncdefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#funcdef.
    def visitFuncdef(self, ctx:Python3Parser.FuncdefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#parameters.
    def visitParameters(self, ctx:Python3Parser.ParametersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#typedargslist.
    def visitTypedargslist(self, ctx:Python3Parser.TypedargslistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#tfpdef.
    def visitTfpdef(self, ctx:Python3Parser.TfpdefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#varargslist.
    def visitVarargslist(self, ctx:Python3Parser.VarargslistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#vfpdef.
    def visitVfpdef(self, ctx:Python3Parser.VfpdefContext):
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


    # Visit a parse tree produced by Python3Parser#annassign.
    def visitAnnassign(self, ctx:Python3Parser.AnnassignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#testlistStarExpr.
    def visitTestlistStarExpr(self, ctx:Python3Parser.TestlistStarExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#augassign.
    def visitAugassign(self, ctx:Python3Parser.AugassignContext):
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


    # Visit a parse tree produced by Python3Parser#continue_stmt.
    def visitContinue_stmt(self, ctx:Python3Parser.Continue_stmtContext):
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


    # Visit a parse tree produced by Python3Parser#testNocond.
    def visitTestNocond(self, ctx:Python3Parser.TestNocondContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#lambdef.
    def visitLambdef(self, ctx:Python3Parser.LambdefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#lambdefNocond.
    def visitLambdefNocond(self, ctx:Python3Parser.LambdefNocondContext):
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


    # Visit a parse tree produced by Python3Parser#xorExpr.
    def visitXorExpr(self, ctx:Python3Parser.XorExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#andExpr.
    def visitAndExpr(self, ctx:Python3Parser.AndExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#shiftExpr.
    def visitShiftExpr(self, ctx:Python3Parser.ShiftExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#arithExpr.
    def visitArithExpr(self, ctx:Python3Parser.ArithExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#term.
    def visitTerm(self, ctx:Python3Parser.TermContext):
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


    # Visit a parse tree produced by Python3Parser#atom.
    def visitAtom(self, ctx:Python3Parser.AtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#testlistComp.
    def visitTestlistComp(self, ctx:Python3Parser.TestlistCompContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#trailer.
    def visitTrailer(self, ctx:Python3Parser.TrailerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#subscriptlist.
    def visitSubscriptlist(self, ctx:Python3Parser.SubscriptlistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#subscript.
    def visitSubscript(self, ctx:Python3Parser.SubscriptContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#sliceop.
    def visitSliceop(self, ctx:Python3Parser.SliceopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#exprlist.
    def visitExprlist(self, ctx:Python3Parser.ExprlistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#testlist.
    def visitTestlist(self, ctx:Python3Parser.TestlistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#dictorsetmaker.
    def visitDictorsetmaker(self, ctx:Python3Parser.DictorsetmakerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#classdef.
    def visitClassdef(self, ctx:Python3Parser.ClassdefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#arglist.
    def visitArglist(self, ctx:Python3Parser.ArglistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Python3Parser#argument.
    def visitArgument(self, ctx:Python3Parser.ArgumentContext):
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
