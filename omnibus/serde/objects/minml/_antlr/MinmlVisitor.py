# flake8: noqa
# Generated from Minml.g4 by ANTLR 4.8
from omnibus._vendor.antlr4 import *
if __name__ is not None and "." in __name__:
    from .MinmlParser import MinmlParser
else:
    from MinmlParser import MinmlParser

# This class defines a complete generic visitor for a parse tree produced by MinmlParser.

class MinmlVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by MinmlParser#root.
    def visitRoot(self, ctx:MinmlParser.RootContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MinmlParser#value.
    def visitValue(self, ctx:MinmlParser.ValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MinmlParser#obj.
    def visitObj(self, ctx:MinmlParser.ObjContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MinmlParser#pair.
    def visitPair(self, ctx:MinmlParser.PairContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MinmlParser#array.
    def visitArray(self, ctx:MinmlParser.ArrayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MinmlParser#identifier.
    def visitIdentifier(self, ctx:MinmlParser.IdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MinmlParser#string.
    def visitString(self, ctx:MinmlParser.StringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MinmlParser#number.
    def visitNumber(self, ctx:MinmlParser.NumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MinmlParser#true.
    def visitTrue(self, ctx:MinmlParser.TrueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MinmlParser#false.
    def visitFalse(self, ctx:MinmlParser.FalseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MinmlParser#null.
    def visitNull(self, ctx:MinmlParser.NullContext):
        return self.visitChildren(ctx)



del MinmlParser
