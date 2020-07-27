# flake8: noqa
# type: ignore
# Generated from Toml.g4 by ANTLR 4.8
from ....._vendor.antlr4 import *
if __name__ is not None and "." in __name__:
    from .TomlParser import TomlParser
else:
    from TomlParser import TomlParser

# This class defines a complete generic visitor for a parse tree produced by TomlParser.

class TomlVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by TomlParser#document.
    def visitDocument(self, ctx:TomlParser.DocumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TomlParser#expression.
    def visitExpression(self, ctx:TomlParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TomlParser#comment.
    def visitComment(self, ctx:TomlParser.CommentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TomlParser#keyValue.
    def visitKeyValue(self, ctx:TomlParser.KeyValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TomlParser#key.
    def visitKey(self, ctx:TomlParser.KeyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TomlParser#simpleKey.
    def visitSimpleKey(self, ctx:TomlParser.SimpleKeyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TomlParser#unquotedKey.
    def visitUnquotedKey(self, ctx:TomlParser.UnquotedKeyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TomlParser#quotedKey.
    def visitQuotedKey(self, ctx:TomlParser.QuotedKeyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TomlParser#dottedKey.
    def visitDottedKey(self, ctx:TomlParser.DottedKeyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TomlParser#value.
    def visitValue(self, ctx:TomlParser.ValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TomlParser#string.
    def visitString(self, ctx:TomlParser.StringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TomlParser#integer.
    def visitInteger(self, ctx:TomlParser.IntegerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TomlParser#floatingPoint.
    def visitFloatingPoint(self, ctx:TomlParser.FloatingPointContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TomlParser#boolean.
    def visitBoolean(self, ctx:TomlParser.BooleanContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TomlParser#dateTime.
    def visitDateTime(self, ctx:TomlParser.DateTimeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TomlParser#array.
    def visitArray(self, ctx:TomlParser.ArrayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TomlParser#arrayValues.
    def visitArrayValues(self, ctx:TomlParser.ArrayValuesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TomlParser#commentOrNl.
    def visitCommentOrNl(self, ctx:TomlParser.CommentOrNlContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TomlParser#table.
    def visitTable(self, ctx:TomlParser.TableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TomlParser#standardTable.
    def visitStandardTable(self, ctx:TomlParser.StandardTableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TomlParser#inlineTable.
    def visitInlineTable(self, ctx:TomlParser.InlineTableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TomlParser#inlineTableKeyvals.
    def visitInlineTableKeyvals(self, ctx:TomlParser.InlineTableKeyvalsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TomlParser#inlineTableKeyvalsNonEmpty.
    def visitInlineTableKeyvalsNonEmpty(self, ctx:TomlParser.InlineTableKeyvalsNonEmptyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TomlParser#arrayTable.
    def visitArrayTable(self, ctx:TomlParser.ArrayTableContext):
        return self.visitChildren(ctx)



del TomlParser
