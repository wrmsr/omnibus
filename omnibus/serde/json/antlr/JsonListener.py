# flake8: noqa
# Generated from Json.g4 by ANTLR 4.8
from ...._vendor.antlr4 import *
if __name__ is not None and "." in __name__:
    from .JsonParser import JsonParser
else:
    from JsonParser import JsonParser

# This class defines a complete listener for a parse tree produced by JsonParser.
class JsonListener(ParseTreeListener):

    # Enter a parse tree produced by JsonParser#json.
    def enterJson(self, ctx:JsonParser.JsonContext):
        pass

    # Exit a parse tree produced by JsonParser#json.
    def exitJson(self, ctx:JsonParser.JsonContext):
        pass


    # Enter a parse tree produced by JsonParser#obj.
    def enterObj(self, ctx:JsonParser.ObjContext):
        pass

    # Exit a parse tree produced by JsonParser#obj.
    def exitObj(self, ctx:JsonParser.ObjContext):
        pass


    # Enter a parse tree produced by JsonParser#pair.
    def enterPair(self, ctx:JsonParser.PairContext):
        pass

    # Exit a parse tree produced by JsonParser#pair.
    def exitPair(self, ctx:JsonParser.PairContext):
        pass


    # Enter a parse tree produced by JsonParser#array.
    def enterArray(self, ctx:JsonParser.ArrayContext):
        pass

    # Exit a parse tree produced by JsonParser#array.
    def exitArray(self, ctx:JsonParser.ArrayContext):
        pass


    # Enter a parse tree produced by JsonParser#value.
    def enterValue(self, ctx:JsonParser.ValueContext):
        pass

    # Exit a parse tree produced by JsonParser#value.
    def exitValue(self, ctx:JsonParser.ValueContext):
        pass



del JsonParser
