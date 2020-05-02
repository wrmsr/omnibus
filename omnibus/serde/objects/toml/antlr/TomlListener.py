# flake8: noqa
# Generated from Toml.g4 by ANTLR 4.8
from ....._vendor.antlr4 import *
if __name__ is not None and "." in __name__:
    from .TomlParser import TomlParser
else:
    from TomlParser import TomlParser

# This class defines a complete listener for a parse tree produced by TomlParser.
class TomlListener(ParseTreeListener):

    # Enter a parse tree produced by TomlParser#document.
    def enterDocument(self, ctx:TomlParser.DocumentContext):
        pass

    # Exit a parse tree produced by TomlParser#document.
    def exitDocument(self, ctx:TomlParser.DocumentContext):
        pass


    # Enter a parse tree produced by TomlParser#expression.
    def enterExpression(self, ctx:TomlParser.ExpressionContext):
        pass

    # Exit a parse tree produced by TomlParser#expression.
    def exitExpression(self, ctx:TomlParser.ExpressionContext):
        pass


    # Enter a parse tree produced by TomlParser#comment.
    def enterComment(self, ctx:TomlParser.CommentContext):
        pass

    # Exit a parse tree produced by TomlParser#comment.
    def exitComment(self, ctx:TomlParser.CommentContext):
        pass


    # Enter a parse tree produced by TomlParser#keyValue.
    def enterKeyValue(self, ctx:TomlParser.KeyValueContext):
        pass

    # Exit a parse tree produced by TomlParser#keyValue.
    def exitKeyValue(self, ctx:TomlParser.KeyValueContext):
        pass


    # Enter a parse tree produced by TomlParser#key.
    def enterKey(self, ctx:TomlParser.KeyContext):
        pass

    # Exit a parse tree produced by TomlParser#key.
    def exitKey(self, ctx:TomlParser.KeyContext):
        pass


    # Enter a parse tree produced by TomlParser#simpleKey.
    def enterSimpleKey(self, ctx:TomlParser.SimpleKeyContext):
        pass

    # Exit a parse tree produced by TomlParser#simpleKey.
    def exitSimpleKey(self, ctx:TomlParser.SimpleKeyContext):
        pass


    # Enter a parse tree produced by TomlParser#unquotedKey.
    def enterUnquotedKey(self, ctx:TomlParser.UnquotedKeyContext):
        pass

    # Exit a parse tree produced by TomlParser#unquotedKey.
    def exitUnquotedKey(self, ctx:TomlParser.UnquotedKeyContext):
        pass


    # Enter a parse tree produced by TomlParser#quotedKey.
    def enterQuotedKey(self, ctx:TomlParser.QuotedKeyContext):
        pass

    # Exit a parse tree produced by TomlParser#quotedKey.
    def exitQuotedKey(self, ctx:TomlParser.QuotedKeyContext):
        pass


    # Enter a parse tree produced by TomlParser#dottedKey.
    def enterDottedKey(self, ctx:TomlParser.DottedKeyContext):
        pass

    # Exit a parse tree produced by TomlParser#dottedKey.
    def exitDottedKey(self, ctx:TomlParser.DottedKeyContext):
        pass


    # Enter a parse tree produced by TomlParser#value.
    def enterValue(self, ctx:TomlParser.ValueContext):
        pass

    # Exit a parse tree produced by TomlParser#value.
    def exitValue(self, ctx:TomlParser.ValueContext):
        pass


    # Enter a parse tree produced by TomlParser#string.
    def enterString(self, ctx:TomlParser.StringContext):
        pass

    # Exit a parse tree produced by TomlParser#string.
    def exitString(self, ctx:TomlParser.StringContext):
        pass


    # Enter a parse tree produced by TomlParser#integer.
    def enterInteger(self, ctx:TomlParser.IntegerContext):
        pass

    # Exit a parse tree produced by TomlParser#integer.
    def exitInteger(self, ctx:TomlParser.IntegerContext):
        pass


    # Enter a parse tree produced by TomlParser#floatingPoint.
    def enterFloatingPoint(self, ctx:TomlParser.FloatingPointContext):
        pass

    # Exit a parse tree produced by TomlParser#floatingPoint.
    def exitFloatingPoint(self, ctx:TomlParser.FloatingPointContext):
        pass


    # Enter a parse tree produced by TomlParser#boolean.
    def enterBoolean(self, ctx:TomlParser.BooleanContext):
        pass

    # Exit a parse tree produced by TomlParser#boolean.
    def exitBoolean(self, ctx:TomlParser.BooleanContext):
        pass


    # Enter a parse tree produced by TomlParser#dateTime.
    def enterDateTime(self, ctx:TomlParser.DateTimeContext):
        pass

    # Exit a parse tree produced by TomlParser#dateTime.
    def exitDateTime(self, ctx:TomlParser.DateTimeContext):
        pass


    # Enter a parse tree produced by TomlParser#array.
    def enterArray(self, ctx:TomlParser.ArrayContext):
        pass

    # Exit a parse tree produced by TomlParser#array.
    def exitArray(self, ctx:TomlParser.ArrayContext):
        pass


    # Enter a parse tree produced by TomlParser#arrayValues.
    def enterArrayValues(self, ctx:TomlParser.ArrayValuesContext):
        pass

    # Exit a parse tree produced by TomlParser#arrayValues.
    def exitArrayValues(self, ctx:TomlParser.ArrayValuesContext):
        pass


    # Enter a parse tree produced by TomlParser#commentOrNl.
    def enterCommentOrNl(self, ctx:TomlParser.CommentOrNlContext):
        pass

    # Exit a parse tree produced by TomlParser#commentOrNl.
    def exitCommentOrNl(self, ctx:TomlParser.CommentOrNlContext):
        pass


    # Enter a parse tree produced by TomlParser#table.
    def enterTable(self, ctx:TomlParser.TableContext):
        pass

    # Exit a parse tree produced by TomlParser#table.
    def exitTable(self, ctx:TomlParser.TableContext):
        pass


    # Enter a parse tree produced by TomlParser#standardTable.
    def enterStandardTable(self, ctx:TomlParser.StandardTableContext):
        pass

    # Exit a parse tree produced by TomlParser#standardTable.
    def exitStandardTable(self, ctx:TomlParser.StandardTableContext):
        pass


    # Enter a parse tree produced by TomlParser#inlineTable.
    def enterInlineTable(self, ctx:TomlParser.InlineTableContext):
        pass

    # Exit a parse tree produced by TomlParser#inlineTable.
    def exitInlineTable(self, ctx:TomlParser.InlineTableContext):
        pass


    # Enter a parse tree produced by TomlParser#inlineTableKeyvals.
    def enterInlineTableKeyvals(self, ctx:TomlParser.InlineTableKeyvalsContext):
        pass

    # Exit a parse tree produced by TomlParser#inlineTableKeyvals.
    def exitInlineTableKeyvals(self, ctx:TomlParser.InlineTableKeyvalsContext):
        pass


    # Enter a parse tree produced by TomlParser#inlineTableKeyvalsNonEmpty.
    def enterInlineTableKeyvalsNonEmpty(self, ctx:TomlParser.InlineTableKeyvalsNonEmptyContext):
        pass

    # Exit a parse tree produced by TomlParser#inlineTableKeyvalsNonEmpty.
    def exitInlineTableKeyvalsNonEmpty(self, ctx:TomlParser.InlineTableKeyvalsNonEmptyContext):
        pass


    # Enter a parse tree produced by TomlParser#arrayTable.
    def enterArrayTable(self, ctx:TomlParser.ArrayTableContext):
        pass

    # Exit a parse tree produced by TomlParser#arrayTable.
    def exitArrayTable(self, ctx:TomlParser.ArrayTableContext):
        pass



del TomlParser
