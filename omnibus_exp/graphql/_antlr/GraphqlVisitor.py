# flake8: noqa
# type: ignore
# Generated from Graphql.g4 by ANTLR 4.8
from ..._vendor.antlr4 import *
if __name__ is not None and "." in __name__:
    from .GraphqlParser import GraphqlParser
else:
    from GraphqlParser import GraphqlParser

# This class defines a complete generic visitor for a parse tree produced by GraphqlParser.

class GraphqlVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by GraphqlParser#document.
    def visitDocument(self, ctx:GraphqlParser.DocumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#definition.
    def visitDefinition(self, ctx:GraphqlParser.DefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#executableDefinition.
    def visitExecutableDefinition(self, ctx:GraphqlParser.ExecutableDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#operationDefinition.
    def visitOperationDefinition(self, ctx:GraphqlParser.OperationDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#operationType.
    def visitOperationType(self, ctx:GraphqlParser.OperationTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#selectionSet.
    def visitSelectionSet(self, ctx:GraphqlParser.SelectionSetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#selection.
    def visitSelection(self, ctx:GraphqlParser.SelectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#field.
    def visitField(self, ctx:GraphqlParser.FieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#arguments.
    def visitArguments(self, ctx:GraphqlParser.ArgumentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#argument.
    def visitArgument(self, ctx:GraphqlParser.ArgumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#alias.
    def visitAlias(self, ctx:GraphqlParser.AliasContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#fragmentSpread.
    def visitFragmentSpread(self, ctx:GraphqlParser.FragmentSpreadContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#fragmentDefinition.
    def visitFragmentDefinition(self, ctx:GraphqlParser.FragmentDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#fragmentName.
    def visitFragmentName(self, ctx:GraphqlParser.FragmentNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#typeCondition.
    def visitTypeCondition(self, ctx:GraphqlParser.TypeConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#inlineFragment.
    def visitInlineFragment(self, ctx:GraphqlParser.InlineFragmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#value.
    def visitValue(self, ctx:GraphqlParser.ValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#intValue.
    def visitIntValue(self, ctx:GraphqlParser.IntValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#floatValue.
    def visitFloatValue(self, ctx:GraphqlParser.FloatValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#booleanValue.
    def visitBooleanValue(self, ctx:GraphqlParser.BooleanValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#stringValue.
    def visitStringValue(self, ctx:GraphqlParser.StringValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#nullValue.
    def visitNullValue(self, ctx:GraphqlParser.NullValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#enumValue.
    def visitEnumValue(self, ctx:GraphqlParser.EnumValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#listValue.
    def visitListValue(self, ctx:GraphqlParser.ListValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#objectValue.
    def visitObjectValue(self, ctx:GraphqlParser.ObjectValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#objectField.
    def visitObjectField(self, ctx:GraphqlParser.ObjectFieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#variable.
    def visitVariable(self, ctx:GraphqlParser.VariableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#variableDefinitions.
    def visitVariableDefinitions(self, ctx:GraphqlParser.VariableDefinitionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#variableDefinition.
    def visitVariableDefinition(self, ctx:GraphqlParser.VariableDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#defaultValue.
    def visitDefaultValue(self, ctx:GraphqlParser.DefaultValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#type_.
    def visitType_(self, ctx:GraphqlParser.Type_Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#namedType.
    def visitNamedType(self, ctx:GraphqlParser.NamedTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#listType.
    def visitListType(self, ctx:GraphqlParser.ListTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#directives.
    def visitDirectives(self, ctx:GraphqlParser.DirectivesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#directive.
    def visitDirective(self, ctx:GraphqlParser.DirectiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#typeSystemDefinition.
    def visitTypeSystemDefinition(self, ctx:GraphqlParser.TypeSystemDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#typeSystemExtension.
    def visitTypeSystemExtension(self, ctx:GraphqlParser.TypeSystemExtensionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#schemaDefinition.
    def visitSchemaDefinition(self, ctx:GraphqlParser.SchemaDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#rootOperationTypeDefinition.
    def visitRootOperationTypeDefinition(self, ctx:GraphqlParser.RootOperationTypeDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#schemaExtension.
    def visitSchemaExtension(self, ctx:GraphqlParser.SchemaExtensionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#operationTypeDefinition.
    def visitOperationTypeDefinition(self, ctx:GraphqlParser.OperationTypeDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#description.
    def visitDescription(self, ctx:GraphqlParser.DescriptionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#typeDefinition.
    def visitTypeDefinition(self, ctx:GraphqlParser.TypeDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#typeExtension.
    def visitTypeExtension(self, ctx:GraphqlParser.TypeExtensionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#scalarTypeDefinition.
    def visitScalarTypeDefinition(self, ctx:GraphqlParser.ScalarTypeDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#scalarTypeExtension.
    def visitScalarTypeExtension(self, ctx:GraphqlParser.ScalarTypeExtensionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#objectTypeDefinition.
    def visitObjectTypeDefinition(self, ctx:GraphqlParser.ObjectTypeDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#implementsInterfaces.
    def visitImplementsInterfaces(self, ctx:GraphqlParser.ImplementsInterfacesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#fieldsDefinition.
    def visitFieldsDefinition(self, ctx:GraphqlParser.FieldsDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#fieldDefinition.
    def visitFieldDefinition(self, ctx:GraphqlParser.FieldDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#argumentsDefinition.
    def visitArgumentsDefinition(self, ctx:GraphqlParser.ArgumentsDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#inputValueDefinition.
    def visitInputValueDefinition(self, ctx:GraphqlParser.InputValueDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#objectTypeExtension.
    def visitObjectTypeExtension(self, ctx:GraphqlParser.ObjectTypeExtensionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#interfaceTypeDefinition.
    def visitInterfaceTypeDefinition(self, ctx:GraphqlParser.InterfaceTypeDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#interfaceTypeExtension.
    def visitInterfaceTypeExtension(self, ctx:GraphqlParser.InterfaceTypeExtensionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#unionTypeDefinition.
    def visitUnionTypeDefinition(self, ctx:GraphqlParser.UnionTypeDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#unionMemberTypes.
    def visitUnionMemberTypes(self, ctx:GraphqlParser.UnionMemberTypesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#unionTypeExtension.
    def visitUnionTypeExtension(self, ctx:GraphqlParser.UnionTypeExtensionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#enumTypeDefinition.
    def visitEnumTypeDefinition(self, ctx:GraphqlParser.EnumTypeDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#enumValuesDefinition.
    def visitEnumValuesDefinition(self, ctx:GraphqlParser.EnumValuesDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#enumValueDefinition.
    def visitEnumValueDefinition(self, ctx:GraphqlParser.EnumValueDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#enumTypeExtension.
    def visitEnumTypeExtension(self, ctx:GraphqlParser.EnumTypeExtensionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#inputObjectTypeDefinition.
    def visitInputObjectTypeDefinition(self, ctx:GraphqlParser.InputObjectTypeDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#inputFieldsDefinition.
    def visitInputFieldsDefinition(self, ctx:GraphqlParser.InputFieldsDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#inputObjectTypeExtension.
    def visitInputObjectTypeExtension(self, ctx:GraphqlParser.InputObjectTypeExtensionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#directiveDefinition.
    def visitDirectiveDefinition(self, ctx:GraphqlParser.DirectiveDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#directiveLocations.
    def visitDirectiveLocations(self, ctx:GraphqlParser.DirectiveLocationsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#directiveLocation.
    def visitDirectiveLocation(self, ctx:GraphqlParser.DirectiveLocationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#executableDirectiveLocation.
    def visitExecutableDirectiveLocation(self, ctx:GraphqlParser.ExecutableDirectiveLocationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#typeSystemDirectiveLocation.
    def visitTypeSystemDirectiveLocation(self, ctx:GraphqlParser.TypeSystemDirectiveLocationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraphqlParser#name.
    def visitName(self, ctx:GraphqlParser.NameContext):
        return self.visitChildren(ctx)



del GraphqlParser
