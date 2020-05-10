// Generated from /Users/spinlock/src/wrmsr/omnibus/omnibus/asts/Python3.g4 by ANTLR 4.8
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link Python3Parser}.
 */
public interface Python3Listener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link Python3Parser#singleInput}.
	 * @param ctx the parse tree
	 */
	void enterSingleInput(Python3Parser.SingleInputContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#singleInput}.
	 * @param ctx the parse tree
	 */
	void exitSingleInput(Python3Parser.SingleInputContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#fileInput}.
	 * @param ctx the parse tree
	 */
	void enterFileInput(Python3Parser.FileInputContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#fileInput}.
	 * @param ctx the parse tree
	 */
	void exitFileInput(Python3Parser.FileInputContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#evalInput}.
	 * @param ctx the parse tree
	 */
	void enterEvalInput(Python3Parser.EvalInputContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#evalInput}.
	 * @param ctx the parse tree
	 */
	void exitEvalInput(Python3Parser.EvalInputContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#decorator}.
	 * @param ctx the parse tree
	 */
	void enterDecorator(Python3Parser.DecoratorContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#decorator}.
	 * @param ctx the parse tree
	 */
	void exitDecorator(Python3Parser.DecoratorContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#decorators}.
	 * @param ctx the parse tree
	 */
	void enterDecorators(Python3Parser.DecoratorsContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#decorators}.
	 * @param ctx the parse tree
	 */
	void exitDecorators(Python3Parser.DecoratorsContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#decorated}.
	 * @param ctx the parse tree
	 */
	void enterDecorated(Python3Parser.DecoratedContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#decorated}.
	 * @param ctx the parse tree
	 */
	void exitDecorated(Python3Parser.DecoratedContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#asyncFuncdef}.
	 * @param ctx the parse tree
	 */
	void enterAsyncFuncdef(Python3Parser.AsyncFuncdefContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#asyncFuncdef}.
	 * @param ctx the parse tree
	 */
	void exitAsyncFuncdef(Python3Parser.AsyncFuncdefContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#funcdef}.
	 * @param ctx the parse tree
	 */
	void enterFuncdef(Python3Parser.FuncdefContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#funcdef}.
	 * @param ctx the parse tree
	 */
	void exitFuncdef(Python3Parser.FuncdefContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#parameters}.
	 * @param ctx the parse tree
	 */
	void enterParameters(Python3Parser.ParametersContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#parameters}.
	 * @param ctx the parse tree
	 */
	void exitParameters(Python3Parser.ParametersContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#typedargslist}.
	 * @param ctx the parse tree
	 */
	void enterTypedargslist(Python3Parser.TypedargslistContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#typedargslist}.
	 * @param ctx the parse tree
	 */
	void exitTypedargslist(Python3Parser.TypedargslistContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#tfpdef}.
	 * @param ctx the parse tree
	 */
	void enterTfpdef(Python3Parser.TfpdefContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#tfpdef}.
	 * @param ctx the parse tree
	 */
	void exitTfpdef(Python3Parser.TfpdefContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#varargslist}.
	 * @param ctx the parse tree
	 */
	void enterVarargslist(Python3Parser.VarargslistContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#varargslist}.
	 * @param ctx the parse tree
	 */
	void exitVarargslist(Python3Parser.VarargslistContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#vfpdef}.
	 * @param ctx the parse tree
	 */
	void enterVfpdef(Python3Parser.VfpdefContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#vfpdef}.
	 * @param ctx the parse tree
	 */
	void exitVfpdef(Python3Parser.VfpdefContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#stmt}.
	 * @param ctx the parse tree
	 */
	void enterStmt(Python3Parser.StmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#stmt}.
	 * @param ctx the parse tree
	 */
	void exitStmt(Python3Parser.StmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#simpleStmt}.
	 * @param ctx the parse tree
	 */
	void enterSimpleStmt(Python3Parser.SimpleStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#simpleStmt}.
	 * @param ctx the parse tree
	 */
	void exitSimpleStmt(Python3Parser.SimpleStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#smallStmt}.
	 * @param ctx the parse tree
	 */
	void enterSmallStmt(Python3Parser.SmallStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#smallStmt}.
	 * @param ctx the parse tree
	 */
	void exitSmallStmt(Python3Parser.SmallStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#exprStmt}.
	 * @param ctx the parse tree
	 */
	void enterExprStmt(Python3Parser.ExprStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#exprStmt}.
	 * @param ctx the parse tree
	 */
	void exitExprStmt(Python3Parser.ExprStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#annassign}.
	 * @param ctx the parse tree
	 */
	void enterAnnassign(Python3Parser.AnnassignContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#annassign}.
	 * @param ctx the parse tree
	 */
	void exitAnnassign(Python3Parser.AnnassignContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#testlistStarExpr}.
	 * @param ctx the parse tree
	 */
	void enterTestlistStarExpr(Python3Parser.TestlistStarExprContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#testlistStarExpr}.
	 * @param ctx the parse tree
	 */
	void exitTestlistStarExpr(Python3Parser.TestlistStarExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#augassign}.
	 * @param ctx the parse tree
	 */
	void enterAugassign(Python3Parser.AugassignContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#augassign}.
	 * @param ctx the parse tree
	 */
	void exitAugassign(Python3Parser.AugassignContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#delStmt}.
	 * @param ctx the parse tree
	 */
	void enterDelStmt(Python3Parser.DelStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#delStmt}.
	 * @param ctx the parse tree
	 */
	void exitDelStmt(Python3Parser.DelStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#passStmt}.
	 * @param ctx the parse tree
	 */
	void enterPassStmt(Python3Parser.PassStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#passStmt}.
	 * @param ctx the parse tree
	 */
	void exitPassStmt(Python3Parser.PassStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#flowStmt}.
	 * @param ctx the parse tree
	 */
	void enterFlowStmt(Python3Parser.FlowStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#flowStmt}.
	 * @param ctx the parse tree
	 */
	void exitFlowStmt(Python3Parser.FlowStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#breakStmt}.
	 * @param ctx the parse tree
	 */
	void enterBreakStmt(Python3Parser.BreakStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#breakStmt}.
	 * @param ctx the parse tree
	 */
	void exitBreakStmt(Python3Parser.BreakStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#continue_stmt}.
	 * @param ctx the parse tree
	 */
	void enterContinue_stmt(Python3Parser.Continue_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#continue_stmt}.
	 * @param ctx the parse tree
	 */
	void exitContinue_stmt(Python3Parser.Continue_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#returnStmt}.
	 * @param ctx the parse tree
	 */
	void enterReturnStmt(Python3Parser.ReturnStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#returnStmt}.
	 * @param ctx the parse tree
	 */
	void exitReturnStmt(Python3Parser.ReturnStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#yieldStmt}.
	 * @param ctx the parse tree
	 */
	void enterYieldStmt(Python3Parser.YieldStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#yieldStmt}.
	 * @param ctx the parse tree
	 */
	void exitYieldStmt(Python3Parser.YieldStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#raiseStmt}.
	 * @param ctx the parse tree
	 */
	void enterRaiseStmt(Python3Parser.RaiseStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#raiseStmt}.
	 * @param ctx the parse tree
	 */
	void exitRaiseStmt(Python3Parser.RaiseStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#importStmt}.
	 * @param ctx the parse tree
	 */
	void enterImportStmt(Python3Parser.ImportStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#importStmt}.
	 * @param ctx the parse tree
	 */
	void exitImportStmt(Python3Parser.ImportStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#importName}.
	 * @param ctx the parse tree
	 */
	void enterImportName(Python3Parser.ImportNameContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#importName}.
	 * @param ctx the parse tree
	 */
	void exitImportName(Python3Parser.ImportNameContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#importFrom}.
	 * @param ctx the parse tree
	 */
	void enterImportFrom(Python3Parser.ImportFromContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#importFrom}.
	 * @param ctx the parse tree
	 */
	void exitImportFrom(Python3Parser.ImportFromContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#importAsName}.
	 * @param ctx the parse tree
	 */
	void enterImportAsName(Python3Parser.ImportAsNameContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#importAsName}.
	 * @param ctx the parse tree
	 */
	void exitImportAsName(Python3Parser.ImportAsNameContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#dottedAsName}.
	 * @param ctx the parse tree
	 */
	void enterDottedAsName(Python3Parser.DottedAsNameContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#dottedAsName}.
	 * @param ctx the parse tree
	 */
	void exitDottedAsName(Python3Parser.DottedAsNameContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#importAsNames}.
	 * @param ctx the parse tree
	 */
	void enterImportAsNames(Python3Parser.ImportAsNamesContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#importAsNames}.
	 * @param ctx the parse tree
	 */
	void exitImportAsNames(Python3Parser.ImportAsNamesContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#dottedAsNames}.
	 * @param ctx the parse tree
	 */
	void enterDottedAsNames(Python3Parser.DottedAsNamesContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#dottedAsNames}.
	 * @param ctx the parse tree
	 */
	void exitDottedAsNames(Python3Parser.DottedAsNamesContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#dottedName}.
	 * @param ctx the parse tree
	 */
	void enterDottedName(Python3Parser.DottedNameContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#dottedName}.
	 * @param ctx the parse tree
	 */
	void exitDottedName(Python3Parser.DottedNameContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#globalStmt}.
	 * @param ctx the parse tree
	 */
	void enterGlobalStmt(Python3Parser.GlobalStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#globalStmt}.
	 * @param ctx the parse tree
	 */
	void exitGlobalStmt(Python3Parser.GlobalStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#nonlocalStmt}.
	 * @param ctx the parse tree
	 */
	void enterNonlocalStmt(Python3Parser.NonlocalStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#nonlocalStmt}.
	 * @param ctx the parse tree
	 */
	void exitNonlocalStmt(Python3Parser.NonlocalStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#assertStmt}.
	 * @param ctx the parse tree
	 */
	void enterAssertStmt(Python3Parser.AssertStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#assertStmt}.
	 * @param ctx the parse tree
	 */
	void exitAssertStmt(Python3Parser.AssertStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#compoundStmt}.
	 * @param ctx the parse tree
	 */
	void enterCompoundStmt(Python3Parser.CompoundStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#compoundStmt}.
	 * @param ctx the parse tree
	 */
	void exitCompoundStmt(Python3Parser.CompoundStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#asyncStmt}.
	 * @param ctx the parse tree
	 */
	void enterAsyncStmt(Python3Parser.AsyncStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#asyncStmt}.
	 * @param ctx the parse tree
	 */
	void exitAsyncStmt(Python3Parser.AsyncStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#ifStmt}.
	 * @param ctx the parse tree
	 */
	void enterIfStmt(Python3Parser.IfStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#ifStmt}.
	 * @param ctx the parse tree
	 */
	void exitIfStmt(Python3Parser.IfStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#whileStmt}.
	 * @param ctx the parse tree
	 */
	void enterWhileStmt(Python3Parser.WhileStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#whileStmt}.
	 * @param ctx the parse tree
	 */
	void exitWhileStmt(Python3Parser.WhileStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#forStmt}.
	 * @param ctx the parse tree
	 */
	void enterForStmt(Python3Parser.ForStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#forStmt}.
	 * @param ctx the parse tree
	 */
	void exitForStmt(Python3Parser.ForStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#tryStmt}.
	 * @param ctx the parse tree
	 */
	void enterTryStmt(Python3Parser.TryStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#tryStmt}.
	 * @param ctx the parse tree
	 */
	void exitTryStmt(Python3Parser.TryStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#withStmt}.
	 * @param ctx the parse tree
	 */
	void enterWithStmt(Python3Parser.WithStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#withStmt}.
	 * @param ctx the parse tree
	 */
	void exitWithStmt(Python3Parser.WithStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#withItem}.
	 * @param ctx the parse tree
	 */
	void enterWithItem(Python3Parser.WithItemContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#withItem}.
	 * @param ctx the parse tree
	 */
	void exitWithItem(Python3Parser.WithItemContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#exceptClause}.
	 * @param ctx the parse tree
	 */
	void enterExceptClause(Python3Parser.ExceptClauseContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#exceptClause}.
	 * @param ctx the parse tree
	 */
	void exitExceptClause(Python3Parser.ExceptClauseContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#suite}.
	 * @param ctx the parse tree
	 */
	void enterSuite(Python3Parser.SuiteContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#suite}.
	 * @param ctx the parse tree
	 */
	void exitSuite(Python3Parser.SuiteContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#test}.
	 * @param ctx the parse tree
	 */
	void enterTest(Python3Parser.TestContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#test}.
	 * @param ctx the parse tree
	 */
	void exitTest(Python3Parser.TestContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#testNocond}.
	 * @param ctx the parse tree
	 */
	void enterTestNocond(Python3Parser.TestNocondContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#testNocond}.
	 * @param ctx the parse tree
	 */
	void exitTestNocond(Python3Parser.TestNocondContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#lambdef}.
	 * @param ctx the parse tree
	 */
	void enterLambdef(Python3Parser.LambdefContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#lambdef}.
	 * @param ctx the parse tree
	 */
	void exitLambdef(Python3Parser.LambdefContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#lambdefNocond}.
	 * @param ctx the parse tree
	 */
	void enterLambdefNocond(Python3Parser.LambdefNocondContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#lambdefNocond}.
	 * @param ctx the parse tree
	 */
	void exitLambdefNocond(Python3Parser.LambdefNocondContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#orTest}.
	 * @param ctx the parse tree
	 */
	void enterOrTest(Python3Parser.OrTestContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#orTest}.
	 * @param ctx the parse tree
	 */
	void exitOrTest(Python3Parser.OrTestContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#andTest}.
	 * @param ctx the parse tree
	 */
	void enterAndTest(Python3Parser.AndTestContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#andTest}.
	 * @param ctx the parse tree
	 */
	void exitAndTest(Python3Parser.AndTestContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#notTest}.
	 * @param ctx the parse tree
	 */
	void enterNotTest(Python3Parser.NotTestContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#notTest}.
	 * @param ctx the parse tree
	 */
	void exitNotTest(Python3Parser.NotTestContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#comparison}.
	 * @param ctx the parse tree
	 */
	void enterComparison(Python3Parser.ComparisonContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#comparison}.
	 * @param ctx the parse tree
	 */
	void exitComparison(Python3Parser.ComparisonContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#compOp}.
	 * @param ctx the parse tree
	 */
	void enterCompOp(Python3Parser.CompOpContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#compOp}.
	 * @param ctx the parse tree
	 */
	void exitCompOp(Python3Parser.CompOpContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#starExpr}.
	 * @param ctx the parse tree
	 */
	void enterStarExpr(Python3Parser.StarExprContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#starExpr}.
	 * @param ctx the parse tree
	 */
	void exitStarExpr(Python3Parser.StarExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#expr}.
	 * @param ctx the parse tree
	 */
	void enterExpr(Python3Parser.ExprContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#expr}.
	 * @param ctx the parse tree
	 */
	void exitExpr(Python3Parser.ExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#xorExpr}.
	 * @param ctx the parse tree
	 */
	void enterXorExpr(Python3Parser.XorExprContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#xorExpr}.
	 * @param ctx the parse tree
	 */
	void exitXorExpr(Python3Parser.XorExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#andExpr}.
	 * @param ctx the parse tree
	 */
	void enterAndExpr(Python3Parser.AndExprContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#andExpr}.
	 * @param ctx the parse tree
	 */
	void exitAndExpr(Python3Parser.AndExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#shiftExpr}.
	 * @param ctx the parse tree
	 */
	void enterShiftExpr(Python3Parser.ShiftExprContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#shiftExpr}.
	 * @param ctx the parse tree
	 */
	void exitShiftExpr(Python3Parser.ShiftExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#arithExpr}.
	 * @param ctx the parse tree
	 */
	void enterArithExpr(Python3Parser.ArithExprContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#arithExpr}.
	 * @param ctx the parse tree
	 */
	void exitArithExpr(Python3Parser.ArithExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#term}.
	 * @param ctx the parse tree
	 */
	void enterTerm(Python3Parser.TermContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#term}.
	 * @param ctx the parse tree
	 */
	void exitTerm(Python3Parser.TermContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#factor}.
	 * @param ctx the parse tree
	 */
	void enterFactor(Python3Parser.FactorContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#factor}.
	 * @param ctx the parse tree
	 */
	void exitFactor(Python3Parser.FactorContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#power}.
	 * @param ctx the parse tree
	 */
	void enterPower(Python3Parser.PowerContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#power}.
	 * @param ctx the parse tree
	 */
	void exitPower(Python3Parser.PowerContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#atomExpr}.
	 * @param ctx the parse tree
	 */
	void enterAtomExpr(Python3Parser.AtomExprContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#atomExpr}.
	 * @param ctx the parse tree
	 */
	void exitAtomExpr(Python3Parser.AtomExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#atom}.
	 * @param ctx the parse tree
	 */
	void enterAtom(Python3Parser.AtomContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#atom}.
	 * @param ctx the parse tree
	 */
	void exitAtom(Python3Parser.AtomContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#testlistComp}.
	 * @param ctx the parse tree
	 */
	void enterTestlistComp(Python3Parser.TestlistCompContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#testlistComp}.
	 * @param ctx the parse tree
	 */
	void exitTestlistComp(Python3Parser.TestlistCompContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#trailer}.
	 * @param ctx the parse tree
	 */
	void enterTrailer(Python3Parser.TrailerContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#trailer}.
	 * @param ctx the parse tree
	 */
	void exitTrailer(Python3Parser.TrailerContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#subscriptlist}.
	 * @param ctx the parse tree
	 */
	void enterSubscriptlist(Python3Parser.SubscriptlistContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#subscriptlist}.
	 * @param ctx the parse tree
	 */
	void exitSubscriptlist(Python3Parser.SubscriptlistContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#subscript}.
	 * @param ctx the parse tree
	 */
	void enterSubscript(Python3Parser.SubscriptContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#subscript}.
	 * @param ctx the parse tree
	 */
	void exitSubscript(Python3Parser.SubscriptContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#sliceop}.
	 * @param ctx the parse tree
	 */
	void enterSliceop(Python3Parser.SliceopContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#sliceop}.
	 * @param ctx the parse tree
	 */
	void exitSliceop(Python3Parser.SliceopContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#exprlist}.
	 * @param ctx the parse tree
	 */
	void enterExprlist(Python3Parser.ExprlistContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#exprlist}.
	 * @param ctx the parse tree
	 */
	void exitExprlist(Python3Parser.ExprlistContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#testlist}.
	 * @param ctx the parse tree
	 */
	void enterTestlist(Python3Parser.TestlistContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#testlist}.
	 * @param ctx the parse tree
	 */
	void exitTestlist(Python3Parser.TestlistContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#dictorsetmaker}.
	 * @param ctx the parse tree
	 */
	void enterDictorsetmaker(Python3Parser.DictorsetmakerContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#dictorsetmaker}.
	 * @param ctx the parse tree
	 */
	void exitDictorsetmaker(Python3Parser.DictorsetmakerContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#classdef}.
	 * @param ctx the parse tree
	 */
	void enterClassdef(Python3Parser.ClassdefContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#classdef}.
	 * @param ctx the parse tree
	 */
	void exitClassdef(Python3Parser.ClassdefContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#arglist}.
	 * @param ctx the parse tree
	 */
	void enterArglist(Python3Parser.ArglistContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#arglist}.
	 * @param ctx the parse tree
	 */
	void exitArglist(Python3Parser.ArglistContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#argument}.
	 * @param ctx the parse tree
	 */
	void enterArgument(Python3Parser.ArgumentContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#argument}.
	 * @param ctx the parse tree
	 */
	void exitArgument(Python3Parser.ArgumentContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#compIter}.
	 * @param ctx the parse tree
	 */
	void enterCompIter(Python3Parser.CompIterContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#compIter}.
	 * @param ctx the parse tree
	 */
	void exitCompIter(Python3Parser.CompIterContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#compFor}.
	 * @param ctx the parse tree
	 */
	void enterCompFor(Python3Parser.CompForContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#compFor}.
	 * @param ctx the parse tree
	 */
	void exitCompFor(Python3Parser.CompForContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#compIf}.
	 * @param ctx the parse tree
	 */
	void enterCompIf(Python3Parser.CompIfContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#compIf}.
	 * @param ctx the parse tree
	 */
	void exitCompIf(Python3Parser.CompIfContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#encodingDecl}.
	 * @param ctx the parse tree
	 */
	void enterEncodingDecl(Python3Parser.EncodingDeclContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#encodingDecl}.
	 * @param ctx the parse tree
	 */
	void exitEncodingDecl(Python3Parser.EncodingDeclContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#yieldExpr}.
	 * @param ctx the parse tree
	 */
	void enterYieldExpr(Python3Parser.YieldExprContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#yieldExpr}.
	 * @param ctx the parse tree
	 */
	void exitYieldExpr(Python3Parser.YieldExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link Python3Parser#yieldArg}.
	 * @param ctx the parse tree
	 */
	void enterYieldArg(Python3Parser.YieldArgContext ctx);
	/**
	 * Exit a parse tree produced by {@link Python3Parser#yieldArg}.
	 * @param ctx the parse tree
	 */
	void exitYieldArg(Python3Parser.YieldArgContext ctx);
}