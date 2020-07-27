# flake8: noqa
# type: ignore
# Generated from SimpleSql.g4 by ANTLR 4.8
from ...._vendor.antlr4 import *
if __name__ is not None and "." in __name__:
    from .SimpleSqlParser import SimpleSqlParser
else:
    from SimpleSqlParser import SimpleSqlParser

# This class defines a complete generic visitor for a parse tree produced by SimpleSqlParser.

class SimpleSqlVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by SimpleSqlParser#singleStatement.
    def visitSingleStatement(self, ctx:SimpleSqlParser.SingleStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSqlParser#select.
    def visitSelect(self, ctx:SimpleSqlParser.SelectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSqlParser#cteSelect.
    def visitCteSelect(self, ctx:SimpleSqlParser.CteSelectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSqlParser#cte.
    def visitCte(self, ctx:SimpleSqlParser.CteContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSqlParser#unionSelect.
    def visitUnionSelect(self, ctx:SimpleSqlParser.UnionSelectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSqlParser#unionItem.
    def visitUnionItem(self, ctx:SimpleSqlParser.UnionItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSqlParser#primarySelect.
    def visitPrimarySelect(self, ctx:SimpleSqlParser.PrimarySelectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSqlParser#allSelectItem.
    def visitAllSelectItem(self, ctx:SimpleSqlParser.AllSelectItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSqlParser#expressionSelectItem.
    def visitExpressionSelectItem(self, ctx:SimpleSqlParser.ExpressionSelectItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSqlParser#expression.
    def visitExpression(self, ctx:SimpleSqlParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSqlParser#binaryBooleanExpression.
    def visitBinaryBooleanExpression(self, ctx:SimpleSqlParser.BinaryBooleanExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSqlParser#predicatedBooleanExpression.
    def visitPredicatedBooleanExpression(self, ctx:SimpleSqlParser.PredicatedBooleanExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSqlParser#unaryBooleanExpression.
    def visitUnaryBooleanExpression(self, ctx:SimpleSqlParser.UnaryBooleanExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSqlParser#castBooleanExpression.
    def visitCastBooleanExpression(self, ctx:SimpleSqlParser.CastBooleanExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSqlParser#cmpPredicate.
    def visitCmpPredicate(self, ctx:SimpleSqlParser.CmpPredicateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSqlParser#isNullPredicate.
    def visitIsNullPredicate(self, ctx:SimpleSqlParser.IsNullPredicateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSqlParser#inListPredicate.
    def visitInListPredicate(self, ctx:SimpleSqlParser.InListPredicateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSqlParser#inSelectPredicate.
    def visitInSelectPredicate(self, ctx:SimpleSqlParser.InSelectPredicateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSqlParser#likePredicate.
    def visitLikePredicate(self, ctx:SimpleSqlParser.LikePredicateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSqlParser#primaryValueExpression.
    def visitPrimaryValueExpression(self, ctx:SimpleSqlParser.PrimaryValueExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSqlParser#unaryValueExpression.
    def visitUnaryValueExpression(self, ctx:SimpleSqlParser.UnaryValueExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSqlParser#arithValueExpression.
    def visitArithValueExpression(self, ctx:SimpleSqlParser.ArithValueExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSqlParser#functionCallExpression.
    def visitFunctionCallExpression(self, ctx:SimpleSqlParser.FunctionCallExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSqlParser#starFunctionCallExpression.
    def visitStarFunctionCallExpression(self, ctx:SimpleSqlParser.StarFunctionCallExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSqlParser#caseExpression.
    def visitCaseExpression(self, ctx:SimpleSqlParser.CaseExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSqlParser#selectExpression.
    def visitSelectExpression(self, ctx:SimpleSqlParser.SelectExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSqlParser#parenExpression.
    def visitParenExpression(self, ctx:SimpleSqlParser.ParenExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSqlParser#simplePrimaryExpression.
    def visitSimplePrimaryExpression(self, ctx:SimpleSqlParser.SimplePrimaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSqlParser#simpleExpression.
    def visitSimpleExpression(self, ctx:SimpleSqlParser.SimpleExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSqlParser#caseItem.
    def visitCaseItem(self, ctx:SimpleSqlParser.CaseItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSqlParser#over.
    def visitOver(self, ctx:SimpleSqlParser.OverContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSqlParser#sortItem.
    def visitSortItem(self, ctx:SimpleSqlParser.SortItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSqlParser#aliasedRelation.
    def visitAliasedRelation(self, ctx:SimpleSqlParser.AliasedRelationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSqlParser#joinRelation.
    def visitJoinRelation(self, ctx:SimpleSqlParser.JoinRelationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSqlParser#selectRelation.
    def visitSelectRelation(self, ctx:SimpleSqlParser.SelectRelationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSqlParser#tableRelation.
    def visitTableRelation(self, ctx:SimpleSqlParser.TableRelationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSqlParser#parenRelation.
    def visitParenRelation(self, ctx:SimpleSqlParser.ParenRelationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSqlParser#groupBy.
    def visitGroupBy(self, ctx:SimpleSqlParser.GroupByContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSqlParser#qualifiedName.
    def visitQualifiedName(self, ctx:SimpleSqlParser.QualifiedNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSqlParser#identifierList.
    def visitIdentifierList(self, ctx:SimpleSqlParser.IdentifierListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSqlParser#identifier.
    def visitIdentifier(self, ctx:SimpleSqlParser.IdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSqlParser#quotedIdentifier.
    def visitQuotedIdentifier(self, ctx:SimpleSqlParser.QuotedIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSqlParser#integerNumber.
    def visitIntegerNumber(self, ctx:SimpleSqlParser.IntegerNumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSqlParser#decimalNumber.
    def visitDecimalNumber(self, ctx:SimpleSqlParser.DecimalNumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSqlParser#floatNumber.
    def visitFloatNumber(self, ctx:SimpleSqlParser.FloatNumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSqlParser#string.
    def visitString(self, ctx:SimpleSqlParser.StringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSqlParser#null.
    def visitNull(self, ctx:SimpleSqlParser.NullContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSqlParser#true.
    def visitTrue(self, ctx:SimpleSqlParser.TrueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSqlParser#false.
    def visitFalse(self, ctx:SimpleSqlParser.FalseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSqlParser#setQuantifier.
    def visitSetQuantifier(self, ctx:SimpleSqlParser.SetQuantifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSqlParser#joinType.
    def visitJoinType(self, ctx:SimpleSqlParser.JoinTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSqlParser#cmpOp.
    def visitCmpOp(self, ctx:SimpleSqlParser.CmpOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSqlParser#arithOp.
    def visitArithOp(self, ctx:SimpleSqlParser.ArithOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSqlParser#unaryOp.
    def visitUnaryOp(self, ctx:SimpleSqlParser.UnaryOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSqlParser#unquotedIdentifier.
    def visitUnquotedIdentifier(self, ctx:SimpleSqlParser.UnquotedIdentifierContext):
        return self.visitChildren(ctx)



del SimpleSqlParser
