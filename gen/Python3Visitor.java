// Generated from /Users/spinlock/src/wrmsr/omnibus/omnibus/asts/Python3.g4 by ANTLR 4.8
import org.antlr.v4.runtime.tree.ParseTreeVisitor;

/**
 * This interface defines a complete generic visitor for a parse tree produced
 * by {@link Python3Parser}.
 *
 * @param <T> The return type of the visit operation. Use {@link Void} for
 * operations with no return type.
 */
public interface Python3Visitor<T> extends ParseTreeVisitor<T> {
	/**
	 * Visit a parse tree produced by {@link Python3Parser#singleInput}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSingleInput(Python3Parser.SingleInputContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#fileInput}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFileInput(Python3Parser.FileInputContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#evalInput}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEvalInput(Python3Parser.EvalInputContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#decorator}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDecorator(Python3Parser.DecoratorContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#decorators}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDecorators(Python3Parser.DecoratorsContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#decorated}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDecorated(Python3Parser.DecoratedContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#asyncFuncdef}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAsyncFuncdef(Python3Parser.AsyncFuncdefContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#funcdef}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFuncdef(Python3Parser.FuncdefContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#parameters}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitParameters(Python3Parser.ParametersContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#typedargslist}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTypedargslist(Python3Parser.TypedargslistContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#tfpdef}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTfpdef(Python3Parser.TfpdefContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#varargslist}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitVarargslist(Python3Parser.VarargslistContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#vfpdef}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitVfpdef(Python3Parser.VfpdefContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#stmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitStmt(Python3Parser.StmtContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#simpleStmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSimpleStmt(Python3Parser.SimpleStmtContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#smallStmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSmallStmt(Python3Parser.SmallStmtContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#exprStmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitExprStmt(Python3Parser.ExprStmtContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#annassign}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAnnassign(Python3Parser.AnnassignContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#testlistStarExpr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTestlistStarExpr(Python3Parser.TestlistStarExprContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#augassign}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAugassign(Python3Parser.AugassignContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#delStmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDelStmt(Python3Parser.DelStmtContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#passStmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPassStmt(Python3Parser.PassStmtContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#flowStmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFlowStmt(Python3Parser.FlowStmtContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#breakStmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitBreakStmt(Python3Parser.BreakStmtContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#continue_stmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitContinue_stmt(Python3Parser.Continue_stmtContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#returnStmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitReturnStmt(Python3Parser.ReturnStmtContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#yieldStmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitYieldStmt(Python3Parser.YieldStmtContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#raiseStmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitRaiseStmt(Python3Parser.RaiseStmtContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#importStmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitImportStmt(Python3Parser.ImportStmtContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#importName}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitImportName(Python3Parser.ImportNameContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#importFrom}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitImportFrom(Python3Parser.ImportFromContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#importAsName}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitImportAsName(Python3Parser.ImportAsNameContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#dottedAsName}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDottedAsName(Python3Parser.DottedAsNameContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#importAsNames}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitImportAsNames(Python3Parser.ImportAsNamesContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#dottedAsNames}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDottedAsNames(Python3Parser.DottedAsNamesContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#dottedName}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDottedName(Python3Parser.DottedNameContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#globalStmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGlobalStmt(Python3Parser.GlobalStmtContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#nonlocalStmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitNonlocalStmt(Python3Parser.NonlocalStmtContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#assertStmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAssertStmt(Python3Parser.AssertStmtContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#compoundStmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCompoundStmt(Python3Parser.CompoundStmtContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#asyncStmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAsyncStmt(Python3Parser.AsyncStmtContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#ifStmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitIfStmt(Python3Parser.IfStmtContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#whileStmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitWhileStmt(Python3Parser.WhileStmtContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#forStmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitForStmt(Python3Parser.ForStmtContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#tryStmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTryStmt(Python3Parser.TryStmtContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#withStmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitWithStmt(Python3Parser.WithStmtContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#withItem}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitWithItem(Python3Parser.WithItemContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#exceptClause}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitExceptClause(Python3Parser.ExceptClauseContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#suite}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSuite(Python3Parser.SuiteContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#test}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTest(Python3Parser.TestContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#testNocond}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTestNocond(Python3Parser.TestNocondContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#lambdef}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLambdef(Python3Parser.LambdefContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#lambdefNocond}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLambdefNocond(Python3Parser.LambdefNocondContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#orTest}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitOrTest(Python3Parser.OrTestContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#andTest}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAndTest(Python3Parser.AndTestContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#notTest}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitNotTest(Python3Parser.NotTestContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#comparison}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitComparison(Python3Parser.ComparisonContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#compOp}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCompOp(Python3Parser.CompOpContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#starExpr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitStarExpr(Python3Parser.StarExprContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#expr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitExpr(Python3Parser.ExprContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#xorExpr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitXorExpr(Python3Parser.XorExprContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#andExpr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAndExpr(Python3Parser.AndExprContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#shiftExpr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitShiftExpr(Python3Parser.ShiftExprContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#arithExpr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitArithExpr(Python3Parser.ArithExprContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#term}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTerm(Python3Parser.TermContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#factor}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFactor(Python3Parser.FactorContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#power}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPower(Python3Parser.PowerContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#atomExpr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAtomExpr(Python3Parser.AtomExprContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#atom}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAtom(Python3Parser.AtomContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#testlistComp}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTestlistComp(Python3Parser.TestlistCompContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#trailer}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTrailer(Python3Parser.TrailerContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#subscriptlist}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSubscriptlist(Python3Parser.SubscriptlistContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#subscript}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSubscript(Python3Parser.SubscriptContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#sliceop}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSliceop(Python3Parser.SliceopContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#exprlist}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitExprlist(Python3Parser.ExprlistContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#testlist}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTestlist(Python3Parser.TestlistContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#dictorsetmaker}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDictorsetmaker(Python3Parser.DictorsetmakerContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#classdef}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitClassdef(Python3Parser.ClassdefContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#arglist}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitArglist(Python3Parser.ArglistContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#argument}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitArgument(Python3Parser.ArgumentContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#compIter}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCompIter(Python3Parser.CompIterContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#compFor}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCompFor(Python3Parser.CompForContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#compIf}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCompIf(Python3Parser.CompIfContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#encodingDecl}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEncodingDecl(Python3Parser.EncodingDeclContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#yieldExpr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitYieldExpr(Python3Parser.YieldExprContext ctx);
	/**
	 * Visit a parse tree produced by {@link Python3Parser#yieldArg}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitYieldArg(Python3Parser.YieldArgContext ctx);
}