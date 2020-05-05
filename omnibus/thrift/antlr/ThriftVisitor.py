# flake8: noqa
# Generated from Thrift.g4 by ANTLR 4.8
from ..._vendor.antlr4 import *
if __name__ is not None and "." in __name__:
    from .ThriftParser import ThriftParser
else:
    from ThriftParser import ThriftParser

# This class defines a complete generic visitor for a parse tree produced by ThriftParser.

class ThriftVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by ThriftParser#document.
    def visitDocument(self, ctx:ThriftParser.DocumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThriftParser#header.
    def visitHeader(self, ctx:ThriftParser.HeaderContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThriftParser#include.
    def visitInclude(self, ctx:ThriftParser.IncludeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThriftParser#cppInclude.
    def visitCppInclude(self, ctx:ThriftParser.CppIncludeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThriftParser#namespace.
    def visitNamespace(self, ctx:ThriftParser.NamespaceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThriftParser#namespaceScope.
    def visitNamespaceScope(self, ctx:ThriftParser.NamespaceScopeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThriftParser#definition.
    def visitDefinition(self, ctx:ThriftParser.DefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThriftParser#const.
    def visitConst(self, ctx:ThriftParser.ConstContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThriftParser#typedef.
    def visitTypedef(self, ctx:ThriftParser.TypedefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThriftParser#enum.
    def visitEnum(self, ctx:ThriftParser.EnumContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThriftParser#senum.
    def visitSenum(self, ctx:ThriftParser.SenumContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThriftParser#struct.
    def visitStruct(self, ctx:ThriftParser.StructContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThriftParser#union.
    def visitUnion(self, ctx:ThriftParser.UnionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThriftParser#exception.
    def visitException(self, ctx:ThriftParser.ExceptionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThriftParser#service.
    def visitService(self, ctx:ThriftParser.ServiceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThriftParser#field.
    def visitField(self, ctx:ThriftParser.FieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThriftParser#fieldID.
    def visitFieldID(self, ctx:ThriftParser.FieldIDContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThriftParser#fieldReq.
    def visitFieldReq(self, ctx:ThriftParser.FieldReqContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThriftParser#xsdFieldOptions.
    def visitXsdFieldOptions(self, ctx:ThriftParser.XsdFieldOptionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThriftParser#xsdAttrs.
    def visitXsdAttrs(self, ctx:ThriftParser.XsdAttrsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThriftParser#function.
    def visitFunction(self, ctx:ThriftParser.FunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThriftParser#functionType.
    def visitFunctionType(self, ctx:ThriftParser.FunctionTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThriftParser#throws_.
    def visitThrows_(self, ctx:ThriftParser.Throws_Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThriftParser#fieldType.
    def visitFieldType(self, ctx:ThriftParser.FieldTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThriftParser#definitionType.
    def visitDefinitionType(self, ctx:ThriftParser.DefinitionTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThriftParser#baseType.
    def visitBaseType(self, ctx:ThriftParser.BaseTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThriftParser#containerType.
    def visitContainerType(self, ctx:ThriftParser.ContainerTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThriftParser#mapType.
    def visitMapType(self, ctx:ThriftParser.MapTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThriftParser#setType.
    def visitSetType(self, ctx:ThriftParser.SetTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThriftParser#listType.
    def visitListType(self, ctx:ThriftParser.ListTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThriftParser#cppType.
    def visitCppType(self, ctx:ThriftParser.CppTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThriftParser#constValue.
    def visitConstValue(self, ctx:ThriftParser.ConstValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThriftParser#intConstant.
    def visitIntConstant(self, ctx:ThriftParser.IntConstantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThriftParser#doubleConstant.
    def visitDoubleConstant(self, ctx:ThriftParser.DoubleConstantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThriftParser#constList.
    def visitConstList(self, ctx:ThriftParser.ConstListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThriftParser#constMap.
    def visitConstMap(self, ctx:ThriftParser.ConstMapContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThriftParser#literal.
    def visitLiteral(self, ctx:ThriftParser.LiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThriftParser#listSeparator.
    def visitListSeparator(self, ctx:ThriftParser.ListSeparatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThriftParser#identifier.
    def visitIdentifier(self, ctx:ThriftParser.IdentifierContext):
        return self.visitChildren(ctx)



del ThriftParser
