# flake8: noqa
# Generated from Thrift.g4 by ANTLR 4.8
from ..._vendor.antlr4 import *
if __name__ is not None and "." in __name__:
    from .ThriftParser import ThriftParser
else:
    from ThriftParser import ThriftParser

# This class defines a complete listener for a parse tree produced by ThriftParser.
class ThriftListener(ParseTreeListener):

    # Enter a parse tree produced by ThriftParser#document.
    def enterDocument(self, ctx:ThriftParser.DocumentContext):
        pass

    # Exit a parse tree produced by ThriftParser#document.
    def exitDocument(self, ctx:ThriftParser.DocumentContext):
        pass


    # Enter a parse tree produced by ThriftParser#header.
    def enterHeader(self, ctx:ThriftParser.HeaderContext):
        pass

    # Exit a parse tree produced by ThriftParser#header.
    def exitHeader(self, ctx:ThriftParser.HeaderContext):
        pass


    # Enter a parse tree produced by ThriftParser#include.
    def enterInclude(self, ctx:ThriftParser.IncludeContext):
        pass

    # Exit a parse tree produced by ThriftParser#include.
    def exitInclude(self, ctx:ThriftParser.IncludeContext):
        pass


    # Enter a parse tree produced by ThriftParser#cppInclude.
    def enterCppInclude(self, ctx:ThriftParser.CppIncludeContext):
        pass

    # Exit a parse tree produced by ThriftParser#cppInclude.
    def exitCppInclude(self, ctx:ThriftParser.CppIncludeContext):
        pass


    # Enter a parse tree produced by ThriftParser#namespace.
    def enterNamespace(self, ctx:ThriftParser.NamespaceContext):
        pass

    # Exit a parse tree produced by ThriftParser#namespace.
    def exitNamespace(self, ctx:ThriftParser.NamespaceContext):
        pass


    # Enter a parse tree produced by ThriftParser#namespaceScope.
    def enterNamespaceScope(self, ctx:ThriftParser.NamespaceScopeContext):
        pass

    # Exit a parse tree produced by ThriftParser#namespaceScope.
    def exitNamespaceScope(self, ctx:ThriftParser.NamespaceScopeContext):
        pass


    # Enter a parse tree produced by ThriftParser#definition.
    def enterDefinition(self, ctx:ThriftParser.DefinitionContext):
        pass

    # Exit a parse tree produced by ThriftParser#definition.
    def exitDefinition(self, ctx:ThriftParser.DefinitionContext):
        pass


    # Enter a parse tree produced by ThriftParser#const.
    def enterConst(self, ctx:ThriftParser.ConstContext):
        pass

    # Exit a parse tree produced by ThriftParser#const.
    def exitConst(self, ctx:ThriftParser.ConstContext):
        pass


    # Enter a parse tree produced by ThriftParser#typedef.
    def enterTypedef(self, ctx:ThriftParser.TypedefContext):
        pass

    # Exit a parse tree produced by ThriftParser#typedef.
    def exitTypedef(self, ctx:ThriftParser.TypedefContext):
        pass


    # Enter a parse tree produced by ThriftParser#enum.
    def enterEnum(self, ctx:ThriftParser.EnumContext):
        pass

    # Exit a parse tree produced by ThriftParser#enum.
    def exitEnum(self, ctx:ThriftParser.EnumContext):
        pass


    # Enter a parse tree produced by ThriftParser#senum.
    def enterSenum(self, ctx:ThriftParser.SenumContext):
        pass

    # Exit a parse tree produced by ThriftParser#senum.
    def exitSenum(self, ctx:ThriftParser.SenumContext):
        pass


    # Enter a parse tree produced by ThriftParser#struct.
    def enterStruct(self, ctx:ThriftParser.StructContext):
        pass

    # Exit a parse tree produced by ThriftParser#struct.
    def exitStruct(self, ctx:ThriftParser.StructContext):
        pass


    # Enter a parse tree produced by ThriftParser#union.
    def enterUnion(self, ctx:ThriftParser.UnionContext):
        pass

    # Exit a parse tree produced by ThriftParser#union.
    def exitUnion(self, ctx:ThriftParser.UnionContext):
        pass


    # Enter a parse tree produced by ThriftParser#exception.
    def enterException(self, ctx:ThriftParser.ExceptionContext):
        pass

    # Exit a parse tree produced by ThriftParser#exception.
    def exitException(self, ctx:ThriftParser.ExceptionContext):
        pass


    # Enter a parse tree produced by ThriftParser#service.
    def enterService(self, ctx:ThriftParser.ServiceContext):
        pass

    # Exit a parse tree produced by ThriftParser#service.
    def exitService(self, ctx:ThriftParser.ServiceContext):
        pass


    # Enter a parse tree produced by ThriftParser#field.
    def enterField(self, ctx:ThriftParser.FieldContext):
        pass

    # Exit a parse tree produced by ThriftParser#field.
    def exitField(self, ctx:ThriftParser.FieldContext):
        pass


    # Enter a parse tree produced by ThriftParser#fieldID.
    def enterFieldID(self, ctx:ThriftParser.FieldIDContext):
        pass

    # Exit a parse tree produced by ThriftParser#fieldID.
    def exitFieldID(self, ctx:ThriftParser.FieldIDContext):
        pass


    # Enter a parse tree produced by ThriftParser#fieldReq.
    def enterFieldReq(self, ctx:ThriftParser.FieldReqContext):
        pass

    # Exit a parse tree produced by ThriftParser#fieldReq.
    def exitFieldReq(self, ctx:ThriftParser.FieldReqContext):
        pass


    # Enter a parse tree produced by ThriftParser#xsdFieldOptions.
    def enterXsdFieldOptions(self, ctx:ThriftParser.XsdFieldOptionsContext):
        pass

    # Exit a parse tree produced by ThriftParser#xsdFieldOptions.
    def exitXsdFieldOptions(self, ctx:ThriftParser.XsdFieldOptionsContext):
        pass


    # Enter a parse tree produced by ThriftParser#xsdAttrs.
    def enterXsdAttrs(self, ctx:ThriftParser.XsdAttrsContext):
        pass

    # Exit a parse tree produced by ThriftParser#xsdAttrs.
    def exitXsdAttrs(self, ctx:ThriftParser.XsdAttrsContext):
        pass


    # Enter a parse tree produced by ThriftParser#function.
    def enterFunction(self, ctx:ThriftParser.FunctionContext):
        pass

    # Exit a parse tree produced by ThriftParser#function.
    def exitFunction(self, ctx:ThriftParser.FunctionContext):
        pass


    # Enter a parse tree produced by ThriftParser#functionType.
    def enterFunctionType(self, ctx:ThriftParser.FunctionTypeContext):
        pass

    # Exit a parse tree produced by ThriftParser#functionType.
    def exitFunctionType(self, ctx:ThriftParser.FunctionTypeContext):
        pass


    # Enter a parse tree produced by ThriftParser#throws_.
    def enterThrows_(self, ctx:ThriftParser.Throws_Context):
        pass

    # Exit a parse tree produced by ThriftParser#throws_.
    def exitThrows_(self, ctx:ThriftParser.Throws_Context):
        pass


    # Enter a parse tree produced by ThriftParser#fieldType.
    def enterFieldType(self, ctx:ThriftParser.FieldTypeContext):
        pass

    # Exit a parse tree produced by ThriftParser#fieldType.
    def exitFieldType(self, ctx:ThriftParser.FieldTypeContext):
        pass


    # Enter a parse tree produced by ThriftParser#definitionType.
    def enterDefinitionType(self, ctx:ThriftParser.DefinitionTypeContext):
        pass

    # Exit a parse tree produced by ThriftParser#definitionType.
    def exitDefinitionType(self, ctx:ThriftParser.DefinitionTypeContext):
        pass


    # Enter a parse tree produced by ThriftParser#baseType.
    def enterBaseType(self, ctx:ThriftParser.BaseTypeContext):
        pass

    # Exit a parse tree produced by ThriftParser#baseType.
    def exitBaseType(self, ctx:ThriftParser.BaseTypeContext):
        pass


    # Enter a parse tree produced by ThriftParser#containerType.
    def enterContainerType(self, ctx:ThriftParser.ContainerTypeContext):
        pass

    # Exit a parse tree produced by ThriftParser#containerType.
    def exitContainerType(self, ctx:ThriftParser.ContainerTypeContext):
        pass


    # Enter a parse tree produced by ThriftParser#mapType.
    def enterMapType(self, ctx:ThriftParser.MapTypeContext):
        pass

    # Exit a parse tree produced by ThriftParser#mapType.
    def exitMapType(self, ctx:ThriftParser.MapTypeContext):
        pass


    # Enter a parse tree produced by ThriftParser#setType.
    def enterSetType(self, ctx:ThriftParser.SetTypeContext):
        pass

    # Exit a parse tree produced by ThriftParser#setType.
    def exitSetType(self, ctx:ThriftParser.SetTypeContext):
        pass


    # Enter a parse tree produced by ThriftParser#listType.
    def enterListType(self, ctx:ThriftParser.ListTypeContext):
        pass

    # Exit a parse tree produced by ThriftParser#listType.
    def exitListType(self, ctx:ThriftParser.ListTypeContext):
        pass


    # Enter a parse tree produced by ThriftParser#cppType.
    def enterCppType(self, ctx:ThriftParser.CppTypeContext):
        pass

    # Exit a parse tree produced by ThriftParser#cppType.
    def exitCppType(self, ctx:ThriftParser.CppTypeContext):
        pass


    # Enter a parse tree produced by ThriftParser#constValue.
    def enterConstValue(self, ctx:ThriftParser.ConstValueContext):
        pass

    # Exit a parse tree produced by ThriftParser#constValue.
    def exitConstValue(self, ctx:ThriftParser.ConstValueContext):
        pass


    # Enter a parse tree produced by ThriftParser#intConstant.
    def enterIntConstant(self, ctx:ThriftParser.IntConstantContext):
        pass

    # Exit a parse tree produced by ThriftParser#intConstant.
    def exitIntConstant(self, ctx:ThriftParser.IntConstantContext):
        pass


    # Enter a parse tree produced by ThriftParser#doubleConstant.
    def enterDoubleConstant(self, ctx:ThriftParser.DoubleConstantContext):
        pass

    # Exit a parse tree produced by ThriftParser#doubleConstant.
    def exitDoubleConstant(self, ctx:ThriftParser.DoubleConstantContext):
        pass


    # Enter a parse tree produced by ThriftParser#constList.
    def enterConstList(self, ctx:ThriftParser.ConstListContext):
        pass

    # Exit a parse tree produced by ThriftParser#constList.
    def exitConstList(self, ctx:ThriftParser.ConstListContext):
        pass


    # Enter a parse tree produced by ThriftParser#constMap.
    def enterConstMap(self, ctx:ThriftParser.ConstMapContext):
        pass

    # Exit a parse tree produced by ThriftParser#constMap.
    def exitConstMap(self, ctx:ThriftParser.ConstMapContext):
        pass


    # Enter a parse tree produced by ThriftParser#literal.
    def enterLiteral(self, ctx:ThriftParser.LiteralContext):
        pass

    # Exit a parse tree produced by ThriftParser#literal.
    def exitLiteral(self, ctx:ThriftParser.LiteralContext):
        pass


    # Enter a parse tree produced by ThriftParser#listSeparator.
    def enterListSeparator(self, ctx:ThriftParser.ListSeparatorContext):
        pass

    # Exit a parse tree produced by ThriftParser#listSeparator.
    def exitListSeparator(self, ctx:ThriftParser.ListSeparatorContext):
        pass


    # Enter a parse tree produced by ThriftParser#identifier.
    def enterIdentifier(self, ctx:ThriftParser.IdentifierContext):
        pass

    # Exit a parse tree produced by ThriftParser#identifier.
    def exitIdentifier(self, ctx:ThriftParser.IdentifierContext):
        pass



del ThriftParser
