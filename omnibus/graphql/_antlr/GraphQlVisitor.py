# flake8: noqa
# Generated from GraphQl.g4 by ANTLR 4.8
from ..._vendor.antlr4 import *
if __name__ is not None and "." in __name__:
    from .GraphQlParser import GraphQlParser
else:
    from GraphQlParser import GraphQlParser

# This class defines a complete generic visitor for a parse tree produced by GraphQlParser.

class GraphQlVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by GraphQlParser#document.
    def visitDocument(self, ctx:GraphQlParser.DocumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#definition.
    def visitDefinition(self, ctx:GraphQlParser.DefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#executableDefinition.
    def visitExecutableDefinition(self, ctx:GraphQlParser.ExecutableDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#operationDefinition.
    def visitOperationDefinition(self, ctx:GraphQlParser.OperationDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#operationType.
    def visitOperationType(self, ctx:GraphQlParser.OperationTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#selectionSet.
    def visitSelectionSet(self, ctx:GraphQlParser.SelectionSetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#selection.
    def visitSelection(self, ctx:GraphQlParser.SelectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#field.
    def visitField(self, ctx:GraphQlParser.FieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#arguments.
    def visitArguments(self, ctx:GraphQlParser.ArgumentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#argument.
    def visitArgument(self, ctx:GraphQlParser.ArgumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#alias.
    def visitAlias(self, ctx:GraphQlParser.AliasContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#fragmentSpread.
    def visitFragmentSpread(self, ctx:GraphQlParser.FragmentSpreadContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#fragmentDefinition.
    def visitFragmentDefinition(self, ctx:GraphQlParser.FragmentDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#fragmentName.
    def visitFragmentName(self, ctx:GraphQlParser.FragmentNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#typeCondition.
    def visitTypeCondition(self, ctx:GraphQlParser.TypeConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#inlineFragment.
    def visitInlineFragment(self, ctx:GraphQlParser.InlineFragmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#value.
    def visitValue(self, ctx:GraphQlParser.ValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#intValue.
    def visitIntValue(self, ctx:GraphQlParser.IntValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#floatValue.
    def visitFloatValue(self, ctx:GraphQlParser.FloatValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#booleanValue.
    def visitBooleanValue(self, ctx:GraphQlParser.BooleanValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#stringValue.
    def visitStringValue(self, ctx:GraphQlParser.StringValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#nullValue.
    def visitNullValue(self, ctx:GraphQlParser.NullValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#enumValue.
    def visitEnumValue(self, ctx:GraphQlParser.EnumValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#listValue.
    def visitListValue(self, ctx:GraphQlParser.ListValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#objectValue.
    def visitObjectValue(self, ctx:GraphQlParser.ObjectValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#objectField.
    def visitObjectField(self, ctx:GraphQlParser.ObjectFieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#variable.
    def visitVariable(self, ctx:GraphQlParser.VariableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#variableDefinitions.
    def visitVariableDefinitions(self, ctx:GraphQlParser.VariableDefinitionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#variableDefinition.
    def visitVariableDefinition(self, ctx:GraphQlParser.VariableDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#defaultValue.
    def visitDefaultValue(self, ctx:GraphQlParser.DefaultValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#type_.
    def visitType_(self, ctx:GraphQlParser.Type_Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#namedType.
    def visitNamedType(self, ctx:GraphQlParser.NamedTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#listType.
    def visitListType(self, ctx:GraphQlParser.ListTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#directives.
    def visitDirectives(self, ctx:GraphQlParser.DirectivesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#directive.
    def visitDirective(self, ctx:GraphQlParser.DirectiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#typeSystemDefinition.
    def visitTypeSystemDefinition(self, ctx:GraphQlParser.TypeSystemDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#typeSystemExtension.
    def visitTypeSystemExtension(self, ctx:GraphQlParser.TypeSystemExtensionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#schemaDefinition.
    def visitSchemaDefinition(self, ctx:GraphQlParser.SchemaDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#rootOperationTypeDefinition.
    def visitRootOperationTypeDefinition(self, ctx:GraphQlParser.RootOperationTypeDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#schemaExtension.
    def visitSchemaExtension(self, ctx:GraphQlParser.SchemaExtensionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#operationTypeDefinition.
    def visitOperationTypeDefinition(self, ctx:GraphQlParser.OperationTypeDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#description.
    def visitDescription(self, ctx:GraphQlParser.DescriptionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#typeDefinition.
    def visitTypeDefinition(self, ctx:GraphQlParser.TypeDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#typeExtension.
    def visitTypeExtension(self, ctx:GraphQlParser.TypeExtensionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#scalarTypeDefinition.
    def visitScalarTypeDefinition(self, ctx:GraphQlParser.ScalarTypeDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#scalarTypeExtension.
    def visitScalarTypeExtension(self, ctx:GraphQlParser.ScalarTypeExtensionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#objectTypeDefinition.
    def visitObjectTypeDefinition(self, ctx:GraphQlParser.ObjectTypeDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#implementsInterfaces.
    def visitImplementsInterfaces(self, ctx:GraphQlParser.ImplementsInterfacesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#fieldsDefinition.
    def visitFieldsDefinition(self, ctx:GraphQlParser.FieldsDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#fieldDefinition.
    def visitFieldDefinition(self, ctx:GraphQlParser.FieldDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#argumentsDefinition.
    def visitArgumentsDefinition(self, ctx:GraphQlParser.ArgumentsDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#inputValueDefinition.
    def visitInputValueDefinition(self, ctx:GraphQlParser.InputValueDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#objectTypeExtension.
    def visitObjectTypeExtension(self, ctx:GraphQlParser.ObjectTypeExtensionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#interfaceTypeDefinition.
    def visitInterfaceTypeDefinition(self, ctx:GraphQlParser.InterfaceTypeDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#interfaceTypeExtension.
    def visitInterfaceTypeExtension(self, ctx:GraphQlParser.InterfaceTypeExtensionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#unionTypeDefinition.
    def visitUnionTypeDefinition(self, ctx:GraphQlParser.UnionTypeDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#unionMemberTypes.
    def visitUnionMemberTypes(self, ctx:GraphQlParser.UnionMemberTypesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#unionTypeExtension.
    def visitUnionTypeExtension(self, ctx:GraphQlParser.UnionTypeExtensionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#enumTypeDefinition.
    def visitEnumTypeDefinition(self, ctx:GraphQlParser.EnumTypeDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#enumValuesDefinition.
    def visitEnumValuesDefinition(self, ctx:GraphQlParser.EnumValuesDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#enumValueDefinition.
    def visitEnumValueDefinition(self, ctx:GraphQlParser.EnumValueDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#enumTypeExtension.
    def visitEnumTypeExtension(self, ctx:GraphQlParser.EnumTypeExtensionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#inputObjectTypeDefinition.
    def visitInputObjectTypeDefinition(self, ctx:GraphQlParser.InputObjectTypeDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#inputFieldsDefinition.
    def visitInputFieldsDefinition(self, ctx:GraphQlParser.InputFieldsDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#inputObjectTypeExtension.
    def visitInputObjectTypeExtension(self, ctx:GraphQlParser.InputObjectTypeExtensionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#directiveDefinition.
    def visitDirectiveDefinition(self, ctx:GraphQlParser.DirectiveDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#directiveLocations.
    def visitDirectiveLocations(self, ctx:GraphQlParser.DirectiveLocationsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#directiveLocation.
    def visitDirectiveLocation(self, ctx:GraphQlParser.DirectiveLocationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#executableDirectiveLocation.
    def visitExecutableDirectiveLocation(self, ctx:GraphQlParser.ExecutableDirectiveLocationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#typeSystemDirectiveLocation.
    def visitTypeSystemDirectiveLocation(self, ctx:GraphQlParser.TypeSystemDirectiveLocationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphQlParser#name.
    def visitName(self, ctx:GraphQlParser.NameContext):
        return self.visitChildren(ctx)



del GraphQlParser
