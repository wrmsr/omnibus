# flake8: noqa
# Generated from Hocon.g4 by ANTLR 4.8
from ...._vendor.antlr4 import *
if __name__ is not None and "." in __name__:
    from .HoconParser import HoconParser
else:
    from HoconParser import HoconParser

# This class defines a complete listener for a parse tree produced by HoconParser.
class HoconListener(ParseTreeListener):

    # Enter a parse tree produced by HoconParser#path.
    def enterPath(self, ctx:HoconParser.PathContext):
        pass

    # Exit a parse tree produced by HoconParser#path.
    def exitPath(self, ctx:HoconParser.PathContext):
        pass


    # Enter a parse tree produced by HoconParser#key.
    def enterKey(self, ctx:HoconParser.KeyContext):
        pass

    # Exit a parse tree produced by HoconParser#key.
    def exitKey(self, ctx:HoconParser.KeyContext):
        pass


    # Enter a parse tree produced by HoconParser#hocon.
    def enterHocon(self, ctx:HoconParser.HoconContext):
        pass

    # Exit a parse tree produced by HoconParser#hocon.
    def exitHocon(self, ctx:HoconParser.HoconContext):
        pass


    # Enter a parse tree produced by HoconParser#obj.
    def enterObj(self, ctx:HoconParser.ObjContext):
        pass

    # Exit a parse tree produced by HoconParser#obj.
    def exitObj(self, ctx:HoconParser.ObjContext):
        pass


    # Enter a parse tree produced by HoconParser#prop.
    def enterProp(self, ctx:HoconParser.PropContext):
        pass

    # Exit a parse tree produced by HoconParser#prop.
    def exitProp(self, ctx:HoconParser.PropContext):
        pass


    # Enter a parse tree produced by HoconParser#rawstring.
    def enterRawstring(self, ctx:HoconParser.RawstringContext):
        pass

    # Exit a parse tree produced by HoconParser#rawstring.
    def exitRawstring(self, ctx:HoconParser.RawstringContext):
        pass


    # Enter a parse tree produced by HoconParser#v_string.
    def enterV_string(self, ctx:HoconParser.V_stringContext):
        pass

    # Exit a parse tree produced by HoconParser#v_string.
    def exitV_string(self, ctx:HoconParser.V_stringContext):
        pass


    # Enter a parse tree produced by HoconParser#v_rawstring.
    def enterV_rawstring(self, ctx:HoconParser.V_rawstringContext):
        pass

    # Exit a parse tree produced by HoconParser#v_rawstring.
    def exitV_rawstring(self, ctx:HoconParser.V_rawstringContext):
        pass


    # Enter a parse tree produced by HoconParser#v_reference.
    def enterV_reference(self, ctx:HoconParser.V_referenceContext):
        pass

    # Exit a parse tree produced by HoconParser#v_reference.
    def exitV_reference(self, ctx:HoconParser.V_referenceContext):
        pass


    # Enter a parse tree produced by HoconParser#objectBegin.
    def enterObjectBegin(self, ctx:HoconParser.ObjectBeginContext):
        pass

    # Exit a parse tree produced by HoconParser#objectBegin.
    def exitObjectBegin(self, ctx:HoconParser.ObjectBeginContext):
        pass


    # Enter a parse tree produced by HoconParser#objectEnd.
    def enterObjectEnd(self, ctx:HoconParser.ObjectEndContext):
        pass

    # Exit a parse tree produced by HoconParser#objectEnd.
    def exitObjectEnd(self, ctx:HoconParser.ObjectEndContext):
        pass


    # Enter a parse tree produced by HoconParser#objectData.
    def enterObjectData(self, ctx:HoconParser.ObjectDataContext):
        pass

    # Exit a parse tree produced by HoconParser#objectData.
    def exitObjectData(self, ctx:HoconParser.ObjectDataContext):
        pass


    # Enter a parse tree produced by HoconParser#arrayData.
    def enterArrayData(self, ctx:HoconParser.ArrayDataContext):
        pass

    # Exit a parse tree produced by HoconParser#arrayData.
    def exitArrayData(self, ctx:HoconParser.ArrayDataContext):
        pass


    # Enter a parse tree produced by HoconParser#stringData.
    def enterStringData(self, ctx:HoconParser.StringDataContext):
        pass

    # Exit a parse tree produced by HoconParser#stringData.
    def exitStringData(self, ctx:HoconParser.StringDataContext):
        pass


    # Enter a parse tree produced by HoconParser#referenceData.
    def enterReferenceData(self, ctx:HoconParser.ReferenceDataContext):
        pass

    # Exit a parse tree produced by HoconParser#referenceData.
    def exitReferenceData(self, ctx:HoconParser.ReferenceDataContext):
        pass


    # Enter a parse tree produced by HoconParser#numberData.
    def enterNumberData(self, ctx:HoconParser.NumberDataContext):
        pass

    # Exit a parse tree produced by HoconParser#numberData.
    def exitNumberData(self, ctx:HoconParser.NumberDataContext):
        pass


    # Enter a parse tree produced by HoconParser#arrayBegin.
    def enterArrayBegin(self, ctx:HoconParser.ArrayBeginContext):
        pass

    # Exit a parse tree produced by HoconParser#arrayBegin.
    def exitArrayBegin(self, ctx:HoconParser.ArrayBeginContext):
        pass


    # Enter a parse tree produced by HoconParser#arrayEnd.
    def enterArrayEnd(self, ctx:HoconParser.ArrayEndContext):
        pass

    # Exit a parse tree produced by HoconParser#arrayEnd.
    def exitArrayEnd(self, ctx:HoconParser.ArrayEndContext):
        pass


    # Enter a parse tree produced by HoconParser#array.
    def enterArray(self, ctx:HoconParser.ArrayContext):
        pass

    # Exit a parse tree produced by HoconParser#array.
    def exitArray(self, ctx:HoconParser.ArrayContext):
        pass


    # Enter a parse tree produced by HoconParser#arrayString.
    def enterArrayString(self, ctx:HoconParser.ArrayStringContext):
        pass

    # Exit a parse tree produced by HoconParser#arrayString.
    def exitArrayString(self, ctx:HoconParser.ArrayStringContext):
        pass


    # Enter a parse tree produced by HoconParser#arrayReference.
    def enterArrayReference(self, ctx:HoconParser.ArrayReferenceContext):
        pass

    # Exit a parse tree produced by HoconParser#arrayReference.
    def exitArrayReference(self, ctx:HoconParser.ArrayReferenceContext):
        pass


    # Enter a parse tree produced by HoconParser#arrayNumber.
    def enterArrayNumber(self, ctx:HoconParser.ArrayNumberContext):
        pass

    # Exit a parse tree produced by HoconParser#arrayNumber.
    def exitArrayNumber(self, ctx:HoconParser.ArrayNumberContext):
        pass


    # Enter a parse tree produced by HoconParser#arrayObj.
    def enterArrayObj(self, ctx:HoconParser.ArrayObjContext):
        pass

    # Exit a parse tree produced by HoconParser#arrayObj.
    def exitArrayObj(self, ctx:HoconParser.ArrayObjContext):
        pass


    # Enter a parse tree produced by HoconParser#arrayArray.
    def enterArrayArray(self, ctx:HoconParser.ArrayArrayContext):
        pass

    # Exit a parse tree produced by HoconParser#arrayArray.
    def exitArrayArray(self, ctx:HoconParser.ArrayArrayContext):
        pass


    # Enter a parse tree produced by HoconParser#arrayValue.
    def enterArrayValue(self, ctx:HoconParser.ArrayValueContext):
        pass

    # Exit a parse tree produced by HoconParser#arrayValue.
    def exitArrayValue(self, ctx:HoconParser.ArrayValueContext):
        pass



del HoconParser