# flake8: noqa
# type: ignore
# Generated from Hocon.g4 by ANTLR 4.8
from ....._vendor.antlr4 import *
if __name__ is not None and "." in __name__:
    from .HoconParser import HoconParser
else:
    from HoconParser import HoconParser

# This class defines a complete generic visitor for a parse tree produced by HoconParser.

class HoconVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by HoconParser#hocon.
    def visitHocon(self, ctx:HoconParser.HoconContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HoconParser#prop.
    def visitProp(self, ctx:HoconParser.PropContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HoconParser#obj.
    def visitObj(self, ctx:HoconParser.ObjContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HoconParser#objectBegin.
    def visitObjectBegin(self, ctx:HoconParser.ObjectBeginContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HoconParser#objectEnd.
    def visitObjectEnd(self, ctx:HoconParser.ObjectEndContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HoconParser#objectData.
    def visitObjectData(self, ctx:HoconParser.ObjectDataContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HoconParser#arrayData.
    def visitArrayData(self, ctx:HoconParser.ArrayDataContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HoconParser#stringData.
    def visitStringData(self, ctx:HoconParser.StringDataContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HoconParser#referenceData.
    def visitReferenceData(self, ctx:HoconParser.ReferenceDataContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HoconParser#numberData.
    def visitNumberData(self, ctx:HoconParser.NumberDataContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HoconParser#key.
    def visitKey(self, ctx:HoconParser.KeyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HoconParser#path.
    def visitPath(self, ctx:HoconParser.PathContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HoconParser#arrayBegin.
    def visitArrayBegin(self, ctx:HoconParser.ArrayBeginContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HoconParser#arrayEnd.
    def visitArrayEnd(self, ctx:HoconParser.ArrayEndContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HoconParser#array.
    def visitArray(self, ctx:HoconParser.ArrayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HoconParser#arrayValue.
    def visitArrayValue(self, ctx:HoconParser.ArrayValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HoconParser#arrayString.
    def visitArrayString(self, ctx:HoconParser.ArrayStringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HoconParser#arrayReference.
    def visitArrayReference(self, ctx:HoconParser.ArrayReferenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HoconParser#arrayNumber.
    def visitArrayNumber(self, ctx:HoconParser.ArrayNumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HoconParser#arrayObj.
    def visitArrayObj(self, ctx:HoconParser.ArrayObjContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HoconParser#arrayArray.
    def visitArrayArray(self, ctx:HoconParser.ArrayArrayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HoconParser#v_string.
    def visitV_string(self, ctx:HoconParser.V_stringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HoconParser#v_rawstring.
    def visitV_rawstring(self, ctx:HoconParser.V_rawstringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HoconParser#v_reference.
    def visitV_reference(self, ctx:HoconParser.V_referenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HoconParser#rawstring.
    def visitRawstring(self, ctx:HoconParser.RawstringContext):
        return self.visitChildren(ctx)



del HoconParser
