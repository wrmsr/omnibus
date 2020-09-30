# flake8: noqa
# Generated from Minml.g4 by ANTLR 4.8
from omnibus._vendor.antlr4 import *
if __name__ is not None and "." in __name__:
    from .MinmlParser import MinmlParser
else:
    from MinmlParser import MinmlParser

# This class defines a complete listener for a parse tree produced by MinmlParser.
class MinmlListener(ParseTreeListener):

    # Enter a parse tree produced by MinmlParser#root.
    def enterRoot(self, ctx:MinmlParser.RootContext):
        pass

    # Exit a parse tree produced by MinmlParser#root.
    def exitRoot(self, ctx:MinmlParser.RootContext):
        pass


    # Enter a parse tree produced by MinmlParser#value.
    def enterValue(self, ctx:MinmlParser.ValueContext):
        pass

    # Exit a parse tree produced by MinmlParser#value.
    def exitValue(self, ctx:MinmlParser.ValueContext):
        pass


    # Enter a parse tree produced by MinmlParser#obj.
    def enterObj(self, ctx:MinmlParser.ObjContext):
        pass

    # Exit a parse tree produced by MinmlParser#obj.
    def exitObj(self, ctx:MinmlParser.ObjContext):
        pass


    # Enter a parse tree produced by MinmlParser#pair.
    def enterPair(self, ctx:MinmlParser.PairContext):
        pass

    # Exit a parse tree produced by MinmlParser#pair.
    def exitPair(self, ctx:MinmlParser.PairContext):
        pass


    # Enter a parse tree produced by MinmlParser#array.
    def enterArray(self, ctx:MinmlParser.ArrayContext):
        pass

    # Exit a parse tree produced by MinmlParser#array.
    def exitArray(self, ctx:MinmlParser.ArrayContext):
        pass


    # Enter a parse tree produced by MinmlParser#identifier.
    def enterIdentifier(self, ctx:MinmlParser.IdentifierContext):
        pass

    # Exit a parse tree produced by MinmlParser#identifier.
    def exitIdentifier(self, ctx:MinmlParser.IdentifierContext):
        pass


    # Enter a parse tree produced by MinmlParser#string.
    def enterString(self, ctx:MinmlParser.StringContext):
        pass

    # Exit a parse tree produced by MinmlParser#string.
    def exitString(self, ctx:MinmlParser.StringContext):
        pass


    # Enter a parse tree produced by MinmlParser#number.
    def enterNumber(self, ctx:MinmlParser.NumberContext):
        pass

    # Exit a parse tree produced by MinmlParser#number.
    def exitNumber(self, ctx:MinmlParser.NumberContext):
        pass


    # Enter a parse tree produced by MinmlParser#true.
    def enterTrue(self, ctx:MinmlParser.TrueContext):
        pass

    # Exit a parse tree produced by MinmlParser#true.
    def exitTrue(self, ctx:MinmlParser.TrueContext):
        pass


    # Enter a parse tree produced by MinmlParser#false.
    def enterFalse(self, ctx:MinmlParser.FalseContext):
        pass

    # Exit a parse tree produced by MinmlParser#false.
    def exitFalse(self, ctx:MinmlParser.FalseContext):
        pass


    # Enter a parse tree produced by MinmlParser#null.
    def enterNull(self, ctx:MinmlParser.NullContext):
        pass

    # Exit a parse tree produced by MinmlParser#null.
    def exitNull(self, ctx:MinmlParser.NullContext):
        pass



del MinmlParser
