# flake8: noqa
# type: ignore
# Generated from SimpleSql.g4 by ANTLR 4.8
from ...._vendor.antlr4 import *
if __name__ is not None and "." in __name__:
    from .SimpleSqlParser import SimpleSqlParser
else:
    from SimpleSqlParser import SimpleSqlParser

# This class defines a complete listener for a parse tree produced by SimpleSqlParser.
class SimpleSqlListener(ParseTreeListener):

    # Enter a parse tree produced by SimpleSqlParser#singleStatement.
    def enterSingleStatement(self, ctx:SimpleSqlParser.SingleStatementContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#singleStatement.
    def exitSingleStatement(self, ctx:SimpleSqlParser.SingleStatementContext):
        pass


    # Enter a parse tree produced by SimpleSqlParser#select.
    def enterSelect(self, ctx:SimpleSqlParser.SelectContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#select.
    def exitSelect(self, ctx:SimpleSqlParser.SelectContext):
        pass


    # Enter a parse tree produced by SimpleSqlParser#cteSelect.
    def enterCteSelect(self, ctx:SimpleSqlParser.CteSelectContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#cteSelect.
    def exitCteSelect(self, ctx:SimpleSqlParser.CteSelectContext):
        pass


    # Enter a parse tree produced by SimpleSqlParser#cte.
    def enterCte(self, ctx:SimpleSqlParser.CteContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#cte.
    def exitCte(self, ctx:SimpleSqlParser.CteContext):
        pass


    # Enter a parse tree produced by SimpleSqlParser#unionSelect.
    def enterUnionSelect(self, ctx:SimpleSqlParser.UnionSelectContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#unionSelect.
    def exitUnionSelect(self, ctx:SimpleSqlParser.UnionSelectContext):
        pass


    # Enter a parse tree produced by SimpleSqlParser#unionItem.
    def enterUnionItem(self, ctx:SimpleSqlParser.UnionItemContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#unionItem.
    def exitUnionItem(self, ctx:SimpleSqlParser.UnionItemContext):
        pass


    # Enter a parse tree produced by SimpleSqlParser#primarySelect.
    def enterPrimarySelect(self, ctx:SimpleSqlParser.PrimarySelectContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#primarySelect.
    def exitPrimarySelect(self, ctx:SimpleSqlParser.PrimarySelectContext):
        pass


    # Enter a parse tree produced by SimpleSqlParser#allSelectItem.
    def enterAllSelectItem(self, ctx:SimpleSqlParser.AllSelectItemContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#allSelectItem.
    def exitAllSelectItem(self, ctx:SimpleSqlParser.AllSelectItemContext):
        pass


    # Enter a parse tree produced by SimpleSqlParser#expressionSelectItem.
    def enterExpressionSelectItem(self, ctx:SimpleSqlParser.ExpressionSelectItemContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#expressionSelectItem.
    def exitExpressionSelectItem(self, ctx:SimpleSqlParser.ExpressionSelectItemContext):
        pass


    # Enter a parse tree produced by SimpleSqlParser#expression.
    def enterExpression(self, ctx:SimpleSqlParser.ExpressionContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#expression.
    def exitExpression(self, ctx:SimpleSqlParser.ExpressionContext):
        pass


    # Enter a parse tree produced by SimpleSqlParser#binaryBooleanExpression.
    def enterBinaryBooleanExpression(self, ctx:SimpleSqlParser.BinaryBooleanExpressionContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#binaryBooleanExpression.
    def exitBinaryBooleanExpression(self, ctx:SimpleSqlParser.BinaryBooleanExpressionContext):
        pass


    # Enter a parse tree produced by SimpleSqlParser#predicatedBooleanExpression.
    def enterPredicatedBooleanExpression(self, ctx:SimpleSqlParser.PredicatedBooleanExpressionContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#predicatedBooleanExpression.
    def exitPredicatedBooleanExpression(self, ctx:SimpleSqlParser.PredicatedBooleanExpressionContext):
        pass


    # Enter a parse tree produced by SimpleSqlParser#unaryBooleanExpression.
    def enterUnaryBooleanExpression(self, ctx:SimpleSqlParser.UnaryBooleanExpressionContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#unaryBooleanExpression.
    def exitUnaryBooleanExpression(self, ctx:SimpleSqlParser.UnaryBooleanExpressionContext):
        pass


    # Enter a parse tree produced by SimpleSqlParser#castBooleanExpression.
    def enterCastBooleanExpression(self, ctx:SimpleSqlParser.CastBooleanExpressionContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#castBooleanExpression.
    def exitCastBooleanExpression(self, ctx:SimpleSqlParser.CastBooleanExpressionContext):
        pass


    # Enter a parse tree produced by SimpleSqlParser#cmpPredicate.
    def enterCmpPredicate(self, ctx:SimpleSqlParser.CmpPredicateContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#cmpPredicate.
    def exitCmpPredicate(self, ctx:SimpleSqlParser.CmpPredicateContext):
        pass


    # Enter a parse tree produced by SimpleSqlParser#isNullPredicate.
    def enterIsNullPredicate(self, ctx:SimpleSqlParser.IsNullPredicateContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#isNullPredicate.
    def exitIsNullPredicate(self, ctx:SimpleSqlParser.IsNullPredicateContext):
        pass


    # Enter a parse tree produced by SimpleSqlParser#inListPredicate.
    def enterInListPredicate(self, ctx:SimpleSqlParser.InListPredicateContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#inListPredicate.
    def exitInListPredicate(self, ctx:SimpleSqlParser.InListPredicateContext):
        pass


    # Enter a parse tree produced by SimpleSqlParser#inSelectPredicate.
    def enterInSelectPredicate(self, ctx:SimpleSqlParser.InSelectPredicateContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#inSelectPredicate.
    def exitInSelectPredicate(self, ctx:SimpleSqlParser.InSelectPredicateContext):
        pass


    # Enter a parse tree produced by SimpleSqlParser#likePredicate.
    def enterLikePredicate(self, ctx:SimpleSqlParser.LikePredicateContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#likePredicate.
    def exitLikePredicate(self, ctx:SimpleSqlParser.LikePredicateContext):
        pass


    # Enter a parse tree produced by SimpleSqlParser#primaryValueExpression.
    def enterPrimaryValueExpression(self, ctx:SimpleSqlParser.PrimaryValueExpressionContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#primaryValueExpression.
    def exitPrimaryValueExpression(self, ctx:SimpleSqlParser.PrimaryValueExpressionContext):
        pass


    # Enter a parse tree produced by SimpleSqlParser#unaryValueExpression.
    def enterUnaryValueExpression(self, ctx:SimpleSqlParser.UnaryValueExpressionContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#unaryValueExpression.
    def exitUnaryValueExpression(self, ctx:SimpleSqlParser.UnaryValueExpressionContext):
        pass


    # Enter a parse tree produced by SimpleSqlParser#arithValueExpression.
    def enterArithValueExpression(self, ctx:SimpleSqlParser.ArithValueExpressionContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#arithValueExpression.
    def exitArithValueExpression(self, ctx:SimpleSqlParser.ArithValueExpressionContext):
        pass


    # Enter a parse tree produced by SimpleSqlParser#functionCallExpression.
    def enterFunctionCallExpression(self, ctx:SimpleSqlParser.FunctionCallExpressionContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#functionCallExpression.
    def exitFunctionCallExpression(self, ctx:SimpleSqlParser.FunctionCallExpressionContext):
        pass


    # Enter a parse tree produced by SimpleSqlParser#starFunctionCallExpression.
    def enterStarFunctionCallExpression(self, ctx:SimpleSqlParser.StarFunctionCallExpressionContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#starFunctionCallExpression.
    def exitStarFunctionCallExpression(self, ctx:SimpleSqlParser.StarFunctionCallExpressionContext):
        pass


    # Enter a parse tree produced by SimpleSqlParser#caseExpression.
    def enterCaseExpression(self, ctx:SimpleSqlParser.CaseExpressionContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#caseExpression.
    def exitCaseExpression(self, ctx:SimpleSqlParser.CaseExpressionContext):
        pass


    # Enter a parse tree produced by SimpleSqlParser#selectExpression.
    def enterSelectExpression(self, ctx:SimpleSqlParser.SelectExpressionContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#selectExpression.
    def exitSelectExpression(self, ctx:SimpleSqlParser.SelectExpressionContext):
        pass


    # Enter a parse tree produced by SimpleSqlParser#parenExpression.
    def enterParenExpression(self, ctx:SimpleSqlParser.ParenExpressionContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#parenExpression.
    def exitParenExpression(self, ctx:SimpleSqlParser.ParenExpressionContext):
        pass


    # Enter a parse tree produced by SimpleSqlParser#simplePrimaryExpression.
    def enterSimplePrimaryExpression(self, ctx:SimpleSqlParser.SimplePrimaryExpressionContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#simplePrimaryExpression.
    def exitSimplePrimaryExpression(self, ctx:SimpleSqlParser.SimplePrimaryExpressionContext):
        pass


    # Enter a parse tree produced by SimpleSqlParser#simpleExpression.
    def enterSimpleExpression(self, ctx:SimpleSqlParser.SimpleExpressionContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#simpleExpression.
    def exitSimpleExpression(self, ctx:SimpleSqlParser.SimpleExpressionContext):
        pass


    # Enter a parse tree produced by SimpleSqlParser#caseItem.
    def enterCaseItem(self, ctx:SimpleSqlParser.CaseItemContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#caseItem.
    def exitCaseItem(self, ctx:SimpleSqlParser.CaseItemContext):
        pass


    # Enter a parse tree produced by SimpleSqlParser#over.
    def enterOver(self, ctx:SimpleSqlParser.OverContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#over.
    def exitOver(self, ctx:SimpleSqlParser.OverContext):
        pass


    # Enter a parse tree produced by SimpleSqlParser#sortItem.
    def enterSortItem(self, ctx:SimpleSqlParser.SortItemContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#sortItem.
    def exitSortItem(self, ctx:SimpleSqlParser.SortItemContext):
        pass


    # Enter a parse tree produced by SimpleSqlParser#aliasedRelation.
    def enterAliasedRelation(self, ctx:SimpleSqlParser.AliasedRelationContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#aliasedRelation.
    def exitAliasedRelation(self, ctx:SimpleSqlParser.AliasedRelationContext):
        pass


    # Enter a parse tree produced by SimpleSqlParser#joinRelation.
    def enterJoinRelation(self, ctx:SimpleSqlParser.JoinRelationContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#joinRelation.
    def exitJoinRelation(self, ctx:SimpleSqlParser.JoinRelationContext):
        pass


    # Enter a parse tree produced by SimpleSqlParser#selectRelation.
    def enterSelectRelation(self, ctx:SimpleSqlParser.SelectRelationContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#selectRelation.
    def exitSelectRelation(self, ctx:SimpleSqlParser.SelectRelationContext):
        pass


    # Enter a parse tree produced by SimpleSqlParser#tableRelation.
    def enterTableRelation(self, ctx:SimpleSqlParser.TableRelationContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#tableRelation.
    def exitTableRelation(self, ctx:SimpleSqlParser.TableRelationContext):
        pass


    # Enter a parse tree produced by SimpleSqlParser#parenRelation.
    def enterParenRelation(self, ctx:SimpleSqlParser.ParenRelationContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#parenRelation.
    def exitParenRelation(self, ctx:SimpleSqlParser.ParenRelationContext):
        pass


    # Enter a parse tree produced by SimpleSqlParser#groupBy.
    def enterGroupBy(self, ctx:SimpleSqlParser.GroupByContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#groupBy.
    def exitGroupBy(self, ctx:SimpleSqlParser.GroupByContext):
        pass


    # Enter a parse tree produced by SimpleSqlParser#qualifiedName.
    def enterQualifiedName(self, ctx:SimpleSqlParser.QualifiedNameContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#qualifiedName.
    def exitQualifiedName(self, ctx:SimpleSqlParser.QualifiedNameContext):
        pass


    # Enter a parse tree produced by SimpleSqlParser#identifierList.
    def enterIdentifierList(self, ctx:SimpleSqlParser.IdentifierListContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#identifierList.
    def exitIdentifierList(self, ctx:SimpleSqlParser.IdentifierListContext):
        pass


    # Enter a parse tree produced by SimpleSqlParser#identifier.
    def enterIdentifier(self, ctx:SimpleSqlParser.IdentifierContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#identifier.
    def exitIdentifier(self, ctx:SimpleSqlParser.IdentifierContext):
        pass


    # Enter a parse tree produced by SimpleSqlParser#quotedIdentifier.
    def enterQuotedIdentifier(self, ctx:SimpleSqlParser.QuotedIdentifierContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#quotedIdentifier.
    def exitQuotedIdentifier(self, ctx:SimpleSqlParser.QuotedIdentifierContext):
        pass


    # Enter a parse tree produced by SimpleSqlParser#integerNumber.
    def enterIntegerNumber(self, ctx:SimpleSqlParser.IntegerNumberContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#integerNumber.
    def exitIntegerNumber(self, ctx:SimpleSqlParser.IntegerNumberContext):
        pass


    # Enter a parse tree produced by SimpleSqlParser#decimalNumber.
    def enterDecimalNumber(self, ctx:SimpleSqlParser.DecimalNumberContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#decimalNumber.
    def exitDecimalNumber(self, ctx:SimpleSqlParser.DecimalNumberContext):
        pass


    # Enter a parse tree produced by SimpleSqlParser#floatNumber.
    def enterFloatNumber(self, ctx:SimpleSqlParser.FloatNumberContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#floatNumber.
    def exitFloatNumber(self, ctx:SimpleSqlParser.FloatNumberContext):
        pass


    # Enter a parse tree produced by SimpleSqlParser#string.
    def enterString(self, ctx:SimpleSqlParser.StringContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#string.
    def exitString(self, ctx:SimpleSqlParser.StringContext):
        pass


    # Enter a parse tree produced by SimpleSqlParser#null.
    def enterNull(self, ctx:SimpleSqlParser.NullContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#null.
    def exitNull(self, ctx:SimpleSqlParser.NullContext):
        pass


    # Enter a parse tree produced by SimpleSqlParser#true.
    def enterTrue(self, ctx:SimpleSqlParser.TrueContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#true.
    def exitTrue(self, ctx:SimpleSqlParser.TrueContext):
        pass


    # Enter a parse tree produced by SimpleSqlParser#false.
    def enterFalse(self, ctx:SimpleSqlParser.FalseContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#false.
    def exitFalse(self, ctx:SimpleSqlParser.FalseContext):
        pass


    # Enter a parse tree produced by SimpleSqlParser#setQuantifier.
    def enterSetQuantifier(self, ctx:SimpleSqlParser.SetQuantifierContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#setQuantifier.
    def exitSetQuantifier(self, ctx:SimpleSqlParser.SetQuantifierContext):
        pass


    # Enter a parse tree produced by SimpleSqlParser#joinType.
    def enterJoinType(self, ctx:SimpleSqlParser.JoinTypeContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#joinType.
    def exitJoinType(self, ctx:SimpleSqlParser.JoinTypeContext):
        pass


    # Enter a parse tree produced by SimpleSqlParser#cmpOp.
    def enterCmpOp(self, ctx:SimpleSqlParser.CmpOpContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#cmpOp.
    def exitCmpOp(self, ctx:SimpleSqlParser.CmpOpContext):
        pass


    # Enter a parse tree produced by SimpleSqlParser#arithOp.
    def enterArithOp(self, ctx:SimpleSqlParser.ArithOpContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#arithOp.
    def exitArithOp(self, ctx:SimpleSqlParser.ArithOpContext):
        pass


    # Enter a parse tree produced by SimpleSqlParser#unaryOp.
    def enterUnaryOp(self, ctx:SimpleSqlParser.UnaryOpContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#unaryOp.
    def exitUnaryOp(self, ctx:SimpleSqlParser.UnaryOpContext):
        pass


    # Enter a parse tree produced by SimpleSqlParser#unquotedIdentifier.
    def enterUnquotedIdentifier(self, ctx:SimpleSqlParser.UnquotedIdentifierContext):
        pass

    # Exit a parse tree produced by SimpleSqlParser#unquotedIdentifier.
    def exitUnquotedIdentifier(self, ctx:SimpleSqlParser.UnquotedIdentifierContext):
        pass



del SimpleSqlParser
