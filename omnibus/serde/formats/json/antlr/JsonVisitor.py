# flake8: noqa
# Generated from Json.g4 by ANTLR 4.8
from ....._vendor.antlr4 import *
if __name__ is not None and "." in __name__:
    from .JsonParser import JsonParser
else:
    from JsonParser import JsonParser

# This class defines a complete generic visitor for a parse tree produced by JsonParser.

class JsonVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by JsonParser#json.
    def visitJson(self, ctx:JsonParser.JsonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JsonParser#obj.
    def visitObj(self, ctx:JsonParser.ObjContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JsonParser#pair.
    def visitPair(self, ctx:JsonParser.PairContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JsonParser#array.
    def visitArray(self, ctx:JsonParser.ArrayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JsonParser#value.
    def visitValue(self, ctx:JsonParser.ValueContext):
        return self.visitChildren(ctx)



del JsonParser
