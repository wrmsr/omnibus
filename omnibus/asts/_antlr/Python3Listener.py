# flake8: noqa
# Generated from Python3.g4 by ANTLR 4.8
from ..._vendor.antlr4 import *
if __name__ is not None and "." in __name__:
    from .Python3Parser import Python3Parser
else:
    from Python3Parser import Python3Parser

# This class defines a complete listener for a parse tree produced by Python3Parser.
class Python3Listener(ParseTreeListener):

    # Enter a parse tree produced by Python3Parser#singleInput.
    def enterSingleInput(self, ctx:Python3Parser.SingleInputContext):
        pass

    # Exit a parse tree produced by Python3Parser#singleInput.
    def exitSingleInput(self, ctx:Python3Parser.SingleInputContext):
        pass


    # Enter a parse tree produced by Python3Parser#fileInput.
    def enterFileInput(self, ctx:Python3Parser.FileInputContext):
        pass

    # Exit a parse tree produced by Python3Parser#fileInput.
    def exitFileInput(self, ctx:Python3Parser.FileInputContext):
        pass


    # Enter a parse tree produced by Python3Parser#evalInput.
    def enterEvalInput(self, ctx:Python3Parser.EvalInputContext):
        pass

    # Exit a parse tree produced by Python3Parser#evalInput.
    def exitEvalInput(self, ctx:Python3Parser.EvalInputContext):
        pass


    # Enter a parse tree produced by Python3Parser#decorator.
    def enterDecorator(self, ctx:Python3Parser.DecoratorContext):
        pass

    # Exit a parse tree produced by Python3Parser#decorator.
    def exitDecorator(self, ctx:Python3Parser.DecoratorContext):
        pass


    # Enter a parse tree produced by Python3Parser#decorators.
    def enterDecorators(self, ctx:Python3Parser.DecoratorsContext):
        pass

    # Exit a parse tree produced by Python3Parser#decorators.
    def exitDecorators(self, ctx:Python3Parser.DecoratorsContext):
        pass


    # Enter a parse tree produced by Python3Parser#decorated.
    def enterDecorated(self, ctx:Python3Parser.DecoratedContext):
        pass

    # Exit a parse tree produced by Python3Parser#decorated.
    def exitDecorated(self, ctx:Python3Parser.DecoratedContext):
        pass


    # Enter a parse tree produced by Python3Parser#asyncFuncDef.
    def enterAsyncFuncDef(self, ctx:Python3Parser.AsyncFuncDefContext):
        pass

    # Exit a parse tree produced by Python3Parser#asyncFuncDef.
    def exitAsyncFuncDef(self, ctx:Python3Parser.AsyncFuncDefContext):
        pass


    # Enter a parse tree produced by Python3Parser#funcDef.
    def enterFuncDef(self, ctx:Python3Parser.FuncDefContext):
        pass

    # Exit a parse tree produced by Python3Parser#funcDef.
    def exitFuncDef(self, ctx:Python3Parser.FuncDefContext):
        pass


    # Enter a parse tree produced by Python3Parser#parameters.
    def enterParameters(self, ctx:Python3Parser.ParametersContext):
        pass

    # Exit a parse tree produced by Python3Parser#parameters.
    def exitParameters(self, ctx:Python3Parser.ParametersContext):
        pass


    # Enter a parse tree produced by Python3Parser#typedArgsList.
    def enterTypedArgsList(self, ctx:Python3Parser.TypedArgsListContext):
        pass

    # Exit a parse tree produced by Python3Parser#typedArgsList.
    def exitTypedArgsList(self, ctx:Python3Parser.TypedArgsListContext):
        pass


    # Enter a parse tree produced by Python3Parser#tpDef.
    def enterTpDef(self, ctx:Python3Parser.TpDefContext):
        pass

    # Exit a parse tree produced by Python3Parser#tpDef.
    def exitTpDef(self, ctx:Python3Parser.TpDefContext):
        pass


    # Enter a parse tree produced by Python3Parser#varargsList.
    def enterVarargsList(self, ctx:Python3Parser.VarargsListContext):
        pass

    # Exit a parse tree produced by Python3Parser#varargsList.
    def exitVarargsList(self, ctx:Python3Parser.VarargsListContext):
        pass


    # Enter a parse tree produced by Python3Parser#vfpDef.
    def enterVfpDef(self, ctx:Python3Parser.VfpDefContext):
        pass

    # Exit a parse tree produced by Python3Parser#vfpDef.
    def exitVfpDef(self, ctx:Python3Parser.VfpDefContext):
        pass


    # Enter a parse tree produced by Python3Parser#stmt.
    def enterStmt(self, ctx:Python3Parser.StmtContext):
        pass

    # Exit a parse tree produced by Python3Parser#stmt.
    def exitStmt(self, ctx:Python3Parser.StmtContext):
        pass


    # Enter a parse tree produced by Python3Parser#simpleStmt.
    def enterSimpleStmt(self, ctx:Python3Parser.SimpleStmtContext):
        pass

    # Exit a parse tree produced by Python3Parser#simpleStmt.
    def exitSimpleStmt(self, ctx:Python3Parser.SimpleStmtContext):
        pass


    # Enter a parse tree produced by Python3Parser#smallStmt.
    def enterSmallStmt(self, ctx:Python3Parser.SmallStmtContext):
        pass

    # Exit a parse tree produced by Python3Parser#smallStmt.
    def exitSmallStmt(self, ctx:Python3Parser.SmallStmtContext):
        pass


    # Enter a parse tree produced by Python3Parser#exprStmt.
    def enterExprStmt(self, ctx:Python3Parser.ExprStmtContext):
        pass

    # Exit a parse tree produced by Python3Parser#exprStmt.
    def exitExprStmt(self, ctx:Python3Parser.ExprStmtContext):
        pass


    # Enter a parse tree produced by Python3Parser#annAssign.
    def enterAnnAssign(self, ctx:Python3Parser.AnnAssignContext):
        pass

    # Exit a parse tree produced by Python3Parser#annAssign.
    def exitAnnAssign(self, ctx:Python3Parser.AnnAssignContext):
        pass


    # Enter a parse tree produced by Python3Parser#testlistStarExpr.
    def enterTestlistStarExpr(self, ctx:Python3Parser.TestlistStarExprContext):
        pass

    # Exit a parse tree produced by Python3Parser#testlistStarExpr.
    def exitTestlistStarExpr(self, ctx:Python3Parser.TestlistStarExprContext):
        pass


    # Enter a parse tree produced by Python3Parser#augAssign.
    def enterAugAssign(self, ctx:Python3Parser.AugAssignContext):
        pass

    # Exit a parse tree produced by Python3Parser#augAssign.
    def exitAugAssign(self, ctx:Python3Parser.AugAssignContext):
        pass


    # Enter a parse tree produced by Python3Parser#delStmt.
    def enterDelStmt(self, ctx:Python3Parser.DelStmtContext):
        pass

    # Exit a parse tree produced by Python3Parser#delStmt.
    def exitDelStmt(self, ctx:Python3Parser.DelStmtContext):
        pass


    # Enter a parse tree produced by Python3Parser#passStmt.
    def enterPassStmt(self, ctx:Python3Parser.PassStmtContext):
        pass

    # Exit a parse tree produced by Python3Parser#passStmt.
    def exitPassStmt(self, ctx:Python3Parser.PassStmtContext):
        pass


    # Enter a parse tree produced by Python3Parser#flowStmt.
    def enterFlowStmt(self, ctx:Python3Parser.FlowStmtContext):
        pass

    # Exit a parse tree produced by Python3Parser#flowStmt.
    def exitFlowStmt(self, ctx:Python3Parser.FlowStmtContext):
        pass


    # Enter a parse tree produced by Python3Parser#breakStmt.
    def enterBreakStmt(self, ctx:Python3Parser.BreakStmtContext):
        pass

    # Exit a parse tree produced by Python3Parser#breakStmt.
    def exitBreakStmt(self, ctx:Python3Parser.BreakStmtContext):
        pass


    # Enter a parse tree produced by Python3Parser#continueStmt.
    def enterContinueStmt(self, ctx:Python3Parser.ContinueStmtContext):
        pass

    # Exit a parse tree produced by Python3Parser#continueStmt.
    def exitContinueStmt(self, ctx:Python3Parser.ContinueStmtContext):
        pass


    # Enter a parse tree produced by Python3Parser#returnStmt.
    def enterReturnStmt(self, ctx:Python3Parser.ReturnStmtContext):
        pass

    # Exit a parse tree produced by Python3Parser#returnStmt.
    def exitReturnStmt(self, ctx:Python3Parser.ReturnStmtContext):
        pass


    # Enter a parse tree produced by Python3Parser#yieldStmt.
    def enterYieldStmt(self, ctx:Python3Parser.YieldStmtContext):
        pass

    # Exit a parse tree produced by Python3Parser#yieldStmt.
    def exitYieldStmt(self, ctx:Python3Parser.YieldStmtContext):
        pass


    # Enter a parse tree produced by Python3Parser#raiseStmt.
    def enterRaiseStmt(self, ctx:Python3Parser.RaiseStmtContext):
        pass

    # Exit a parse tree produced by Python3Parser#raiseStmt.
    def exitRaiseStmt(self, ctx:Python3Parser.RaiseStmtContext):
        pass


    # Enter a parse tree produced by Python3Parser#importStmt.
    def enterImportStmt(self, ctx:Python3Parser.ImportStmtContext):
        pass

    # Exit a parse tree produced by Python3Parser#importStmt.
    def exitImportStmt(self, ctx:Python3Parser.ImportStmtContext):
        pass


    # Enter a parse tree produced by Python3Parser#importName.
    def enterImportName(self, ctx:Python3Parser.ImportNameContext):
        pass

    # Exit a parse tree produced by Python3Parser#importName.
    def exitImportName(self, ctx:Python3Parser.ImportNameContext):
        pass


    # Enter a parse tree produced by Python3Parser#importFrom.
    def enterImportFrom(self, ctx:Python3Parser.ImportFromContext):
        pass

    # Exit a parse tree produced by Python3Parser#importFrom.
    def exitImportFrom(self, ctx:Python3Parser.ImportFromContext):
        pass


    # Enter a parse tree produced by Python3Parser#importAsName.
    def enterImportAsName(self, ctx:Python3Parser.ImportAsNameContext):
        pass

    # Exit a parse tree produced by Python3Parser#importAsName.
    def exitImportAsName(self, ctx:Python3Parser.ImportAsNameContext):
        pass


    # Enter a parse tree produced by Python3Parser#dottedAsName.
    def enterDottedAsName(self, ctx:Python3Parser.DottedAsNameContext):
        pass

    # Exit a parse tree produced by Python3Parser#dottedAsName.
    def exitDottedAsName(self, ctx:Python3Parser.DottedAsNameContext):
        pass


    # Enter a parse tree produced by Python3Parser#importAsNames.
    def enterImportAsNames(self, ctx:Python3Parser.ImportAsNamesContext):
        pass

    # Exit a parse tree produced by Python3Parser#importAsNames.
    def exitImportAsNames(self, ctx:Python3Parser.ImportAsNamesContext):
        pass


    # Enter a parse tree produced by Python3Parser#dottedAsNames.
    def enterDottedAsNames(self, ctx:Python3Parser.DottedAsNamesContext):
        pass

    # Exit a parse tree produced by Python3Parser#dottedAsNames.
    def exitDottedAsNames(self, ctx:Python3Parser.DottedAsNamesContext):
        pass


    # Enter a parse tree produced by Python3Parser#dottedName.
    def enterDottedName(self, ctx:Python3Parser.DottedNameContext):
        pass

    # Exit a parse tree produced by Python3Parser#dottedName.
    def exitDottedName(self, ctx:Python3Parser.DottedNameContext):
        pass


    # Enter a parse tree produced by Python3Parser#globalStmt.
    def enterGlobalStmt(self, ctx:Python3Parser.GlobalStmtContext):
        pass

    # Exit a parse tree produced by Python3Parser#globalStmt.
    def exitGlobalStmt(self, ctx:Python3Parser.GlobalStmtContext):
        pass


    # Enter a parse tree produced by Python3Parser#nonlocalStmt.
    def enterNonlocalStmt(self, ctx:Python3Parser.NonlocalStmtContext):
        pass

    # Exit a parse tree produced by Python3Parser#nonlocalStmt.
    def exitNonlocalStmt(self, ctx:Python3Parser.NonlocalStmtContext):
        pass


    # Enter a parse tree produced by Python3Parser#assertStmt.
    def enterAssertStmt(self, ctx:Python3Parser.AssertStmtContext):
        pass

    # Exit a parse tree produced by Python3Parser#assertStmt.
    def exitAssertStmt(self, ctx:Python3Parser.AssertStmtContext):
        pass


    # Enter a parse tree produced by Python3Parser#compoundStmt.
    def enterCompoundStmt(self, ctx:Python3Parser.CompoundStmtContext):
        pass

    # Exit a parse tree produced by Python3Parser#compoundStmt.
    def exitCompoundStmt(self, ctx:Python3Parser.CompoundStmtContext):
        pass


    # Enter a parse tree produced by Python3Parser#asyncStmt.
    def enterAsyncStmt(self, ctx:Python3Parser.AsyncStmtContext):
        pass

    # Exit a parse tree produced by Python3Parser#asyncStmt.
    def exitAsyncStmt(self, ctx:Python3Parser.AsyncStmtContext):
        pass


    # Enter a parse tree produced by Python3Parser#ifStmt.
    def enterIfStmt(self, ctx:Python3Parser.IfStmtContext):
        pass

    # Exit a parse tree produced by Python3Parser#ifStmt.
    def exitIfStmt(self, ctx:Python3Parser.IfStmtContext):
        pass


    # Enter a parse tree produced by Python3Parser#whileStmt.
    def enterWhileStmt(self, ctx:Python3Parser.WhileStmtContext):
        pass

    # Exit a parse tree produced by Python3Parser#whileStmt.
    def exitWhileStmt(self, ctx:Python3Parser.WhileStmtContext):
        pass


    # Enter a parse tree produced by Python3Parser#forStmt.
    def enterForStmt(self, ctx:Python3Parser.ForStmtContext):
        pass

    # Exit a parse tree produced by Python3Parser#forStmt.
    def exitForStmt(self, ctx:Python3Parser.ForStmtContext):
        pass


    # Enter a parse tree produced by Python3Parser#tryStmt.
    def enterTryStmt(self, ctx:Python3Parser.TryStmtContext):
        pass

    # Exit a parse tree produced by Python3Parser#tryStmt.
    def exitTryStmt(self, ctx:Python3Parser.TryStmtContext):
        pass


    # Enter a parse tree produced by Python3Parser#withStmt.
    def enterWithStmt(self, ctx:Python3Parser.WithStmtContext):
        pass

    # Exit a parse tree produced by Python3Parser#withStmt.
    def exitWithStmt(self, ctx:Python3Parser.WithStmtContext):
        pass


    # Enter a parse tree produced by Python3Parser#withItem.
    def enterWithItem(self, ctx:Python3Parser.WithItemContext):
        pass

    # Exit a parse tree produced by Python3Parser#withItem.
    def exitWithItem(self, ctx:Python3Parser.WithItemContext):
        pass


    # Enter a parse tree produced by Python3Parser#exceptClause.
    def enterExceptClause(self, ctx:Python3Parser.ExceptClauseContext):
        pass

    # Exit a parse tree produced by Python3Parser#exceptClause.
    def exitExceptClause(self, ctx:Python3Parser.ExceptClauseContext):
        pass


    # Enter a parse tree produced by Python3Parser#suite.
    def enterSuite(self, ctx:Python3Parser.SuiteContext):
        pass

    # Exit a parse tree produced by Python3Parser#suite.
    def exitSuite(self, ctx:Python3Parser.SuiteContext):
        pass


    # Enter a parse tree produced by Python3Parser#test.
    def enterTest(self, ctx:Python3Parser.TestContext):
        pass

    # Exit a parse tree produced by Python3Parser#test.
    def exitTest(self, ctx:Python3Parser.TestContext):
        pass


    # Enter a parse tree produced by Python3Parser#testNocond.
    def enterTestNocond(self, ctx:Python3Parser.TestNocondContext):
        pass

    # Exit a parse tree produced by Python3Parser#testNocond.
    def exitTestNocond(self, ctx:Python3Parser.TestNocondContext):
        pass


    # Enter a parse tree produced by Python3Parser#lambaDef.
    def enterLambaDef(self, ctx:Python3Parser.LambaDefContext):
        pass

    # Exit a parse tree produced by Python3Parser#lambaDef.
    def exitLambaDef(self, ctx:Python3Parser.LambaDefContext):
        pass


    # Enter a parse tree produced by Python3Parser#lambaDefNoCond.
    def enterLambaDefNoCond(self, ctx:Python3Parser.LambaDefNoCondContext):
        pass

    # Exit a parse tree produced by Python3Parser#lambaDefNoCond.
    def exitLambaDefNoCond(self, ctx:Python3Parser.LambaDefNoCondContext):
        pass


    # Enter a parse tree produced by Python3Parser#orTest.
    def enterOrTest(self, ctx:Python3Parser.OrTestContext):
        pass

    # Exit a parse tree produced by Python3Parser#orTest.
    def exitOrTest(self, ctx:Python3Parser.OrTestContext):
        pass


    # Enter a parse tree produced by Python3Parser#andTest.
    def enterAndTest(self, ctx:Python3Parser.AndTestContext):
        pass

    # Exit a parse tree produced by Python3Parser#andTest.
    def exitAndTest(self, ctx:Python3Parser.AndTestContext):
        pass


    # Enter a parse tree produced by Python3Parser#notTest.
    def enterNotTest(self, ctx:Python3Parser.NotTestContext):
        pass

    # Exit a parse tree produced by Python3Parser#notTest.
    def exitNotTest(self, ctx:Python3Parser.NotTestContext):
        pass


    # Enter a parse tree produced by Python3Parser#comparison.
    def enterComparison(self, ctx:Python3Parser.ComparisonContext):
        pass

    # Exit a parse tree produced by Python3Parser#comparison.
    def exitComparison(self, ctx:Python3Parser.ComparisonContext):
        pass


    # Enter a parse tree produced by Python3Parser#compOp.
    def enterCompOp(self, ctx:Python3Parser.CompOpContext):
        pass

    # Exit a parse tree produced by Python3Parser#compOp.
    def exitCompOp(self, ctx:Python3Parser.CompOpContext):
        pass


    # Enter a parse tree produced by Python3Parser#starExpr.
    def enterStarExpr(self, ctx:Python3Parser.StarExprContext):
        pass

    # Exit a parse tree produced by Python3Parser#starExpr.
    def exitStarExpr(self, ctx:Python3Parser.StarExprContext):
        pass


    # Enter a parse tree produced by Python3Parser#expr.
    def enterExpr(self, ctx:Python3Parser.ExprContext):
        pass

    # Exit a parse tree produced by Python3Parser#expr.
    def exitExpr(self, ctx:Python3Parser.ExprContext):
        pass


    # Enter a parse tree produced by Python3Parser#xorExpr.
    def enterXorExpr(self, ctx:Python3Parser.XorExprContext):
        pass

    # Exit a parse tree produced by Python3Parser#xorExpr.
    def exitXorExpr(self, ctx:Python3Parser.XorExprContext):
        pass


    # Enter a parse tree produced by Python3Parser#andExpr.
    def enterAndExpr(self, ctx:Python3Parser.AndExprContext):
        pass

    # Exit a parse tree produced by Python3Parser#andExpr.
    def exitAndExpr(self, ctx:Python3Parser.AndExprContext):
        pass


    # Enter a parse tree produced by Python3Parser#shiftExpr.
    def enterShiftExpr(self, ctx:Python3Parser.ShiftExprContext):
        pass

    # Exit a parse tree produced by Python3Parser#shiftExpr.
    def exitShiftExpr(self, ctx:Python3Parser.ShiftExprContext):
        pass


    # Enter a parse tree produced by Python3Parser#arithExpr.
    def enterArithExpr(self, ctx:Python3Parser.ArithExprContext):
        pass

    # Exit a parse tree produced by Python3Parser#arithExpr.
    def exitArithExpr(self, ctx:Python3Parser.ArithExprContext):
        pass


    # Enter a parse tree produced by Python3Parser#term.
    def enterTerm(self, ctx:Python3Parser.TermContext):
        pass

    # Exit a parse tree produced by Python3Parser#term.
    def exitTerm(self, ctx:Python3Parser.TermContext):
        pass


    # Enter a parse tree produced by Python3Parser#factor.
    def enterFactor(self, ctx:Python3Parser.FactorContext):
        pass

    # Exit a parse tree produced by Python3Parser#factor.
    def exitFactor(self, ctx:Python3Parser.FactorContext):
        pass


    # Enter a parse tree produced by Python3Parser#power.
    def enterPower(self, ctx:Python3Parser.PowerContext):
        pass

    # Exit a parse tree produced by Python3Parser#power.
    def exitPower(self, ctx:Python3Parser.PowerContext):
        pass


    # Enter a parse tree produced by Python3Parser#atomExpr.
    def enterAtomExpr(self, ctx:Python3Parser.AtomExprContext):
        pass

    # Exit a parse tree produced by Python3Parser#atomExpr.
    def exitAtomExpr(self, ctx:Python3Parser.AtomExprContext):
        pass


    # Enter a parse tree produced by Python3Parser#atom.
    def enterAtom(self, ctx:Python3Parser.AtomContext):
        pass

    # Exit a parse tree produced by Python3Parser#atom.
    def exitAtom(self, ctx:Python3Parser.AtomContext):
        pass


    # Enter a parse tree produced by Python3Parser#testlistComp.
    def enterTestlistComp(self, ctx:Python3Parser.TestlistCompContext):
        pass

    # Exit a parse tree produced by Python3Parser#testlistComp.
    def exitTestlistComp(self, ctx:Python3Parser.TestlistCompContext):
        pass


    # Enter a parse tree produced by Python3Parser#trailer.
    def enterTrailer(self, ctx:Python3Parser.TrailerContext):
        pass

    # Exit a parse tree produced by Python3Parser#trailer.
    def exitTrailer(self, ctx:Python3Parser.TrailerContext):
        pass


    # Enter a parse tree produced by Python3Parser#subscriptlist.
    def enterSubscriptlist(self, ctx:Python3Parser.SubscriptlistContext):
        pass

    # Exit a parse tree produced by Python3Parser#subscriptlist.
    def exitSubscriptlist(self, ctx:Python3Parser.SubscriptlistContext):
        pass


    # Enter a parse tree produced by Python3Parser#subscript.
    def enterSubscript(self, ctx:Python3Parser.SubscriptContext):
        pass

    # Exit a parse tree produced by Python3Parser#subscript.
    def exitSubscript(self, ctx:Python3Parser.SubscriptContext):
        pass


    # Enter a parse tree produced by Python3Parser#sliceOp.
    def enterSliceOp(self, ctx:Python3Parser.SliceOpContext):
        pass

    # Exit a parse tree produced by Python3Parser#sliceOp.
    def exitSliceOp(self, ctx:Python3Parser.SliceOpContext):
        pass


    # Enter a parse tree produced by Python3Parser#exprList.
    def enterExprList(self, ctx:Python3Parser.ExprListContext):
        pass

    # Exit a parse tree produced by Python3Parser#exprList.
    def exitExprList(self, ctx:Python3Parser.ExprListContext):
        pass


    # Enter a parse tree produced by Python3Parser#testList.
    def enterTestList(self, ctx:Python3Parser.TestListContext):
        pass

    # Exit a parse tree produced by Python3Parser#testList.
    def exitTestList(self, ctx:Python3Parser.TestListContext):
        pass


    # Enter a parse tree produced by Python3Parser#dictOrSetMaker.
    def enterDictOrSetMaker(self, ctx:Python3Parser.DictOrSetMakerContext):
        pass

    # Exit a parse tree produced by Python3Parser#dictOrSetMaker.
    def exitDictOrSetMaker(self, ctx:Python3Parser.DictOrSetMakerContext):
        pass


    # Enter a parse tree produced by Python3Parser#classDef.
    def enterClassDef(self, ctx:Python3Parser.ClassDefContext):
        pass

    # Exit a parse tree produced by Python3Parser#classDef.
    def exitClassDef(self, ctx:Python3Parser.ClassDefContext):
        pass


    # Enter a parse tree produced by Python3Parser#arglist.
    def enterArglist(self, ctx:Python3Parser.ArglistContext):
        pass

    # Exit a parse tree produced by Python3Parser#arglist.
    def exitArglist(self, ctx:Python3Parser.ArglistContext):
        pass


    # Enter a parse tree produced by Python3Parser#argument.
    def enterArgument(self, ctx:Python3Parser.ArgumentContext):
        pass

    # Exit a parse tree produced by Python3Parser#argument.
    def exitArgument(self, ctx:Python3Parser.ArgumentContext):
        pass


    # Enter a parse tree produced by Python3Parser#compIter.
    def enterCompIter(self, ctx:Python3Parser.CompIterContext):
        pass

    # Exit a parse tree produced by Python3Parser#compIter.
    def exitCompIter(self, ctx:Python3Parser.CompIterContext):
        pass


    # Enter a parse tree produced by Python3Parser#compFor.
    def enterCompFor(self, ctx:Python3Parser.CompForContext):
        pass

    # Exit a parse tree produced by Python3Parser#compFor.
    def exitCompFor(self, ctx:Python3Parser.CompForContext):
        pass


    # Enter a parse tree produced by Python3Parser#compIf.
    def enterCompIf(self, ctx:Python3Parser.CompIfContext):
        pass

    # Exit a parse tree produced by Python3Parser#compIf.
    def exitCompIf(self, ctx:Python3Parser.CompIfContext):
        pass


    # Enter a parse tree produced by Python3Parser#encodingDecl.
    def enterEncodingDecl(self, ctx:Python3Parser.EncodingDeclContext):
        pass

    # Exit a parse tree produced by Python3Parser#encodingDecl.
    def exitEncodingDecl(self, ctx:Python3Parser.EncodingDeclContext):
        pass


    # Enter a parse tree produced by Python3Parser#yieldExpr.
    def enterYieldExpr(self, ctx:Python3Parser.YieldExprContext):
        pass

    # Exit a parse tree produced by Python3Parser#yieldExpr.
    def exitYieldExpr(self, ctx:Python3Parser.YieldExprContext):
        pass


    # Enter a parse tree produced by Python3Parser#yieldArg.
    def enterYieldArg(self, ctx:Python3Parser.YieldArgContext):
        pass

    # Exit a parse tree produced by Python3Parser#yieldArg.
    def exitYieldArg(self, ctx:Python3Parser.YieldArgContext):
        pass



del Python3Parser
