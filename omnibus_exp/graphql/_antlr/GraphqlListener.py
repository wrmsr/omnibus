# flake8: noqa
# type: ignore
# Generated from Graphql.g4 by ANTLR 4.8
from ..._vendor.antlr4 import *
if __name__ is not None and "." in __name__:
    from .GraphqlParser import GraphqlParser
else:
    from GraphqlParser import GraphqlParser

# This class defines a complete listener for a parse tree produced by GraphqlParser.
class GraphqlListener(ParseTreeListener):

    # Enter a parse tree produced by GraphqlParser#document.
    def enterDocument(self, ctx:GraphqlParser.DocumentContext):
        pass

    # Exit a parse tree produced by GraphqlParser#document.
    def exitDocument(self, ctx:GraphqlParser.DocumentContext):
        pass


    # Enter a parse tree produced by GraphqlParser#definition.
    def enterDefinition(self, ctx:GraphqlParser.DefinitionContext):
        pass

    # Exit a parse tree produced by GraphqlParser#definition.
    def exitDefinition(self, ctx:GraphqlParser.DefinitionContext):
        pass


    # Enter a parse tree produced by GraphqlParser#executableDefinition.
    def enterExecutableDefinition(self, ctx:GraphqlParser.ExecutableDefinitionContext):
        pass

    # Exit a parse tree produced by GraphqlParser#executableDefinition.
    def exitExecutableDefinition(self, ctx:GraphqlParser.ExecutableDefinitionContext):
        pass


    # Enter a parse tree produced by GraphqlParser#operationDefinition.
    def enterOperationDefinition(self, ctx:GraphqlParser.OperationDefinitionContext):
        pass

    # Exit a parse tree produced by GraphqlParser#operationDefinition.
    def exitOperationDefinition(self, ctx:GraphqlParser.OperationDefinitionContext):
        pass


    # Enter a parse tree produced by GraphqlParser#operationType.
    def enterOperationType(self, ctx:GraphqlParser.OperationTypeContext):
        pass

    # Exit a parse tree produced by GraphqlParser#operationType.
    def exitOperationType(self, ctx:GraphqlParser.OperationTypeContext):
        pass


    # Enter a parse tree produced by GraphqlParser#selectionSet.
    def enterSelectionSet(self, ctx:GraphqlParser.SelectionSetContext):
        pass

    # Exit a parse tree produced by GraphqlParser#selectionSet.
    def exitSelectionSet(self, ctx:GraphqlParser.SelectionSetContext):
        pass


    # Enter a parse tree produced by GraphqlParser#selection.
    def enterSelection(self, ctx:GraphqlParser.SelectionContext):
        pass

    # Exit a parse tree produced by GraphqlParser#selection.
    def exitSelection(self, ctx:GraphqlParser.SelectionContext):
        pass


    # Enter a parse tree produced by GraphqlParser#field.
    def enterField(self, ctx:GraphqlParser.FieldContext):
        pass

    # Exit a parse tree produced by GraphqlParser#field.
    def exitField(self, ctx:GraphqlParser.FieldContext):
        pass


    # Enter a parse tree produced by GraphqlParser#arguments.
    def enterArguments(self, ctx:GraphqlParser.ArgumentsContext):
        pass

    # Exit a parse tree produced by GraphqlParser#arguments.
    def exitArguments(self, ctx:GraphqlParser.ArgumentsContext):
        pass


    # Enter a parse tree produced by GraphqlParser#argument.
    def enterArgument(self, ctx:GraphqlParser.ArgumentContext):
        pass

    # Exit a parse tree produced by GraphqlParser#argument.
    def exitArgument(self, ctx:GraphqlParser.ArgumentContext):
        pass


    # Enter a parse tree produced by GraphqlParser#alias.
    def enterAlias(self, ctx:GraphqlParser.AliasContext):
        pass

    # Exit a parse tree produced by GraphqlParser#alias.
    def exitAlias(self, ctx:GraphqlParser.AliasContext):
        pass


    # Enter a parse tree produced by GraphqlParser#fragmentSpread.
    def enterFragmentSpread(self, ctx:GraphqlParser.FragmentSpreadContext):
        pass

    # Exit a parse tree produced by GraphqlParser#fragmentSpread.
    def exitFragmentSpread(self, ctx:GraphqlParser.FragmentSpreadContext):
        pass


    # Enter a parse tree produced by GraphqlParser#fragmentDefinition.
    def enterFragmentDefinition(self, ctx:GraphqlParser.FragmentDefinitionContext):
        pass

    # Exit a parse tree produced by GraphqlParser#fragmentDefinition.
    def exitFragmentDefinition(self, ctx:GraphqlParser.FragmentDefinitionContext):
        pass


    # Enter a parse tree produced by GraphqlParser#fragmentName.
    def enterFragmentName(self, ctx:GraphqlParser.FragmentNameContext):
        pass

    # Exit a parse tree produced by GraphqlParser#fragmentName.
    def exitFragmentName(self, ctx:GraphqlParser.FragmentNameContext):
        pass


    # Enter a parse tree produced by GraphqlParser#typeCondition.
    def enterTypeCondition(self, ctx:GraphqlParser.TypeConditionContext):
        pass

    # Exit a parse tree produced by GraphqlParser#typeCondition.
    def exitTypeCondition(self, ctx:GraphqlParser.TypeConditionContext):
        pass


    # Enter a parse tree produced by GraphqlParser#inlineFragment.
    def enterInlineFragment(self, ctx:GraphqlParser.InlineFragmentContext):
        pass

    # Exit a parse tree produced by GraphqlParser#inlineFragment.
    def exitInlineFragment(self, ctx:GraphqlParser.InlineFragmentContext):
        pass


    # Enter a parse tree produced by GraphqlParser#value.
    def enterValue(self, ctx:GraphqlParser.ValueContext):
        pass

    # Exit a parse tree produced by GraphqlParser#value.
    def exitValue(self, ctx:GraphqlParser.ValueContext):
        pass


    # Enter a parse tree produced by GraphqlParser#intValue.
    def enterIntValue(self, ctx:GraphqlParser.IntValueContext):
        pass

    # Exit a parse tree produced by GraphqlParser#intValue.
    def exitIntValue(self, ctx:GraphqlParser.IntValueContext):
        pass


    # Enter a parse tree produced by GraphqlParser#floatValue.
    def enterFloatValue(self, ctx:GraphqlParser.FloatValueContext):
        pass

    # Exit a parse tree produced by GraphqlParser#floatValue.
    def exitFloatValue(self, ctx:GraphqlParser.FloatValueContext):
        pass


    # Enter a parse tree produced by GraphqlParser#booleanValue.
    def enterBooleanValue(self, ctx:GraphqlParser.BooleanValueContext):
        pass

    # Exit a parse tree produced by GraphqlParser#booleanValue.
    def exitBooleanValue(self, ctx:GraphqlParser.BooleanValueContext):
        pass


    # Enter a parse tree produced by GraphqlParser#stringValue.
    def enterStringValue(self, ctx:GraphqlParser.StringValueContext):
        pass

    # Exit a parse tree produced by GraphqlParser#stringValue.
    def exitStringValue(self, ctx:GraphqlParser.StringValueContext):
        pass


    # Enter a parse tree produced by GraphqlParser#nullValue.
    def enterNullValue(self, ctx:GraphqlParser.NullValueContext):
        pass

    # Exit a parse tree produced by GraphqlParser#nullValue.
    def exitNullValue(self, ctx:GraphqlParser.NullValueContext):
        pass


    # Enter a parse tree produced by GraphqlParser#enumValue.
    def enterEnumValue(self, ctx:GraphqlParser.EnumValueContext):
        pass

    # Exit a parse tree produced by GraphqlParser#enumValue.
    def exitEnumValue(self, ctx:GraphqlParser.EnumValueContext):
        pass


    # Enter a parse tree produced by GraphqlParser#listValue.
    def enterListValue(self, ctx:GraphqlParser.ListValueContext):
        pass

    # Exit a parse tree produced by GraphqlParser#listValue.
    def exitListValue(self, ctx:GraphqlParser.ListValueContext):
        pass


    # Enter a parse tree produced by GraphqlParser#objectValue.
    def enterObjectValue(self, ctx:GraphqlParser.ObjectValueContext):
        pass

    # Exit a parse tree produced by GraphqlParser#objectValue.
    def exitObjectValue(self, ctx:GraphqlParser.ObjectValueContext):
        pass


    # Enter a parse tree produced by GraphqlParser#objectField.
    def enterObjectField(self, ctx:GraphqlParser.ObjectFieldContext):
        pass

    # Exit a parse tree produced by GraphqlParser#objectField.
    def exitObjectField(self, ctx:GraphqlParser.ObjectFieldContext):
        pass


    # Enter a parse tree produced by GraphqlParser#variable.
    def enterVariable(self, ctx:GraphqlParser.VariableContext):
        pass

    # Exit a parse tree produced by GraphqlParser#variable.
    def exitVariable(self, ctx:GraphqlParser.VariableContext):
        pass


    # Enter a parse tree produced by GraphqlParser#variableDefinitions.
    def enterVariableDefinitions(self, ctx:GraphqlParser.VariableDefinitionsContext):
        pass

    # Exit a parse tree produced by GraphqlParser#variableDefinitions.
    def exitVariableDefinitions(self, ctx:GraphqlParser.VariableDefinitionsContext):
        pass


    # Enter a parse tree produced by GraphqlParser#variableDefinition.
    def enterVariableDefinition(self, ctx:GraphqlParser.VariableDefinitionContext):
        pass

    # Exit a parse tree produced by GraphqlParser#variableDefinition.
    def exitVariableDefinition(self, ctx:GraphqlParser.VariableDefinitionContext):
        pass


    # Enter a parse tree produced by GraphqlParser#defaultValue.
    def enterDefaultValue(self, ctx:GraphqlParser.DefaultValueContext):
        pass

    # Exit a parse tree produced by GraphqlParser#defaultValue.
    def exitDefaultValue(self, ctx:GraphqlParser.DefaultValueContext):
        pass


    # Enter a parse tree produced by GraphqlParser#type_.
    def enterType_(self, ctx:GraphqlParser.Type_Context):
        pass

    # Exit a parse tree produced by GraphqlParser#type_.
    def exitType_(self, ctx:GraphqlParser.Type_Context):
        pass


    # Enter a parse tree produced by GraphqlParser#namedType.
    def enterNamedType(self, ctx:GraphqlParser.NamedTypeContext):
        pass

    # Exit a parse tree produced by GraphqlParser#namedType.
    def exitNamedType(self, ctx:GraphqlParser.NamedTypeContext):
        pass


    # Enter a parse tree produced by GraphqlParser#listType.
    def enterListType(self, ctx:GraphqlParser.ListTypeContext):
        pass

    # Exit a parse tree produced by GraphqlParser#listType.
    def exitListType(self, ctx:GraphqlParser.ListTypeContext):
        pass


    # Enter a parse tree produced by GraphqlParser#directives.
    def enterDirectives(self, ctx:GraphqlParser.DirectivesContext):
        pass

    # Exit a parse tree produced by GraphqlParser#directives.
    def exitDirectives(self, ctx:GraphqlParser.DirectivesContext):
        pass


    # Enter a parse tree produced by GraphqlParser#directive.
    def enterDirective(self, ctx:GraphqlParser.DirectiveContext):
        pass

    # Exit a parse tree produced by GraphqlParser#directive.
    def exitDirective(self, ctx:GraphqlParser.DirectiveContext):
        pass


    # Enter a parse tree produced by GraphqlParser#typeSystemDefinition.
    def enterTypeSystemDefinition(self, ctx:GraphqlParser.TypeSystemDefinitionContext):
        pass

    # Exit a parse tree produced by GraphqlParser#typeSystemDefinition.
    def exitTypeSystemDefinition(self, ctx:GraphqlParser.TypeSystemDefinitionContext):
        pass


    # Enter a parse tree produced by GraphqlParser#typeSystemExtension.
    def enterTypeSystemExtension(self, ctx:GraphqlParser.TypeSystemExtensionContext):
        pass

    # Exit a parse tree produced by GraphqlParser#typeSystemExtension.
    def exitTypeSystemExtension(self, ctx:GraphqlParser.TypeSystemExtensionContext):
        pass


    # Enter a parse tree produced by GraphqlParser#schemaDefinition.
    def enterSchemaDefinition(self, ctx:GraphqlParser.SchemaDefinitionContext):
        pass

    # Exit a parse tree produced by GraphqlParser#schemaDefinition.
    def exitSchemaDefinition(self, ctx:GraphqlParser.SchemaDefinitionContext):
        pass


    # Enter a parse tree produced by GraphqlParser#rootOperationTypeDefinition.
    def enterRootOperationTypeDefinition(self, ctx:GraphqlParser.RootOperationTypeDefinitionContext):
        pass

    # Exit a parse tree produced by GraphqlParser#rootOperationTypeDefinition.
    def exitRootOperationTypeDefinition(self, ctx:GraphqlParser.RootOperationTypeDefinitionContext):
        pass


    # Enter a parse tree produced by GraphqlParser#schemaExtension.
    def enterSchemaExtension(self, ctx:GraphqlParser.SchemaExtensionContext):
        pass

    # Exit a parse tree produced by GraphqlParser#schemaExtension.
    def exitSchemaExtension(self, ctx:GraphqlParser.SchemaExtensionContext):
        pass


    # Enter a parse tree produced by GraphqlParser#operationTypeDefinition.
    def enterOperationTypeDefinition(self, ctx:GraphqlParser.OperationTypeDefinitionContext):
        pass

    # Exit a parse tree produced by GraphqlParser#operationTypeDefinition.
    def exitOperationTypeDefinition(self, ctx:GraphqlParser.OperationTypeDefinitionContext):
        pass


    # Enter a parse tree produced by GraphqlParser#description.
    def enterDescription(self, ctx:GraphqlParser.DescriptionContext):
        pass

    # Exit a parse tree produced by GraphqlParser#description.
    def exitDescription(self, ctx:GraphqlParser.DescriptionContext):
        pass


    # Enter a parse tree produced by GraphqlParser#typeDefinition.
    def enterTypeDefinition(self, ctx:GraphqlParser.TypeDefinitionContext):
        pass

    # Exit a parse tree produced by GraphqlParser#typeDefinition.
    def exitTypeDefinition(self, ctx:GraphqlParser.TypeDefinitionContext):
        pass


    # Enter a parse tree produced by GraphqlParser#typeExtension.
    def enterTypeExtension(self, ctx:GraphqlParser.TypeExtensionContext):
        pass

    # Exit a parse tree produced by GraphqlParser#typeExtension.
    def exitTypeExtension(self, ctx:GraphqlParser.TypeExtensionContext):
        pass


    # Enter a parse tree produced by GraphqlParser#scalarTypeDefinition.
    def enterScalarTypeDefinition(self, ctx:GraphqlParser.ScalarTypeDefinitionContext):
        pass

    # Exit a parse tree produced by GraphqlParser#scalarTypeDefinition.
    def exitScalarTypeDefinition(self, ctx:GraphqlParser.ScalarTypeDefinitionContext):
        pass


    # Enter a parse tree produced by GraphqlParser#scalarTypeExtension.
    def enterScalarTypeExtension(self, ctx:GraphqlParser.ScalarTypeExtensionContext):
        pass

    # Exit a parse tree produced by GraphqlParser#scalarTypeExtension.
    def exitScalarTypeExtension(self, ctx:GraphqlParser.ScalarTypeExtensionContext):
        pass


    # Enter a parse tree produced by GraphqlParser#objectTypeDefinition.
    def enterObjectTypeDefinition(self, ctx:GraphqlParser.ObjectTypeDefinitionContext):
        pass

    # Exit a parse tree produced by GraphqlParser#objectTypeDefinition.
    def exitObjectTypeDefinition(self, ctx:GraphqlParser.ObjectTypeDefinitionContext):
        pass


    # Enter a parse tree produced by GraphqlParser#implementsInterfaces.
    def enterImplementsInterfaces(self, ctx:GraphqlParser.ImplementsInterfacesContext):
        pass

    # Exit a parse tree produced by GraphqlParser#implementsInterfaces.
    def exitImplementsInterfaces(self, ctx:GraphqlParser.ImplementsInterfacesContext):
        pass


    # Enter a parse tree produced by GraphqlParser#fieldsDefinition.
    def enterFieldsDefinition(self, ctx:GraphqlParser.FieldsDefinitionContext):
        pass

    # Exit a parse tree produced by GraphqlParser#fieldsDefinition.
    def exitFieldsDefinition(self, ctx:GraphqlParser.FieldsDefinitionContext):
        pass


    # Enter a parse tree produced by GraphqlParser#fieldDefinition.
    def enterFieldDefinition(self, ctx:GraphqlParser.FieldDefinitionContext):
        pass

    # Exit a parse tree produced by GraphqlParser#fieldDefinition.
    def exitFieldDefinition(self, ctx:GraphqlParser.FieldDefinitionContext):
        pass


    # Enter a parse tree produced by GraphqlParser#argumentsDefinition.
    def enterArgumentsDefinition(self, ctx:GraphqlParser.ArgumentsDefinitionContext):
        pass

    # Exit a parse tree produced by GraphqlParser#argumentsDefinition.
    def exitArgumentsDefinition(self, ctx:GraphqlParser.ArgumentsDefinitionContext):
        pass


    # Enter a parse tree produced by GraphqlParser#inputValueDefinition.
    def enterInputValueDefinition(self, ctx:GraphqlParser.InputValueDefinitionContext):
        pass

    # Exit a parse tree produced by GraphqlParser#inputValueDefinition.
    def exitInputValueDefinition(self, ctx:GraphqlParser.InputValueDefinitionContext):
        pass


    # Enter a parse tree produced by GraphqlParser#objectTypeExtension.
    def enterObjectTypeExtension(self, ctx:GraphqlParser.ObjectTypeExtensionContext):
        pass

    # Exit a parse tree produced by GraphqlParser#objectTypeExtension.
    def exitObjectTypeExtension(self, ctx:GraphqlParser.ObjectTypeExtensionContext):
        pass


    # Enter a parse tree produced by GraphqlParser#interfaceTypeDefinition.
    def enterInterfaceTypeDefinition(self, ctx:GraphqlParser.InterfaceTypeDefinitionContext):
        pass

    # Exit a parse tree produced by GraphqlParser#interfaceTypeDefinition.
    def exitInterfaceTypeDefinition(self, ctx:GraphqlParser.InterfaceTypeDefinitionContext):
        pass


    # Enter a parse tree produced by GraphqlParser#interfaceTypeExtension.
    def enterInterfaceTypeExtension(self, ctx:GraphqlParser.InterfaceTypeExtensionContext):
        pass

    # Exit a parse tree produced by GraphqlParser#interfaceTypeExtension.
    def exitInterfaceTypeExtension(self, ctx:GraphqlParser.InterfaceTypeExtensionContext):
        pass


    # Enter a parse tree produced by GraphqlParser#unionTypeDefinition.
    def enterUnionTypeDefinition(self, ctx:GraphqlParser.UnionTypeDefinitionContext):
        pass

    # Exit a parse tree produced by GraphqlParser#unionTypeDefinition.
    def exitUnionTypeDefinition(self, ctx:GraphqlParser.UnionTypeDefinitionContext):
        pass


    # Enter a parse tree produced by GraphqlParser#unionMemberTypes.
    def enterUnionMemberTypes(self, ctx:GraphqlParser.UnionMemberTypesContext):
        pass

    # Exit a parse tree produced by GraphqlParser#unionMemberTypes.
    def exitUnionMemberTypes(self, ctx:GraphqlParser.UnionMemberTypesContext):
        pass


    # Enter a parse tree produced by GraphqlParser#unionTypeExtension.
    def enterUnionTypeExtension(self, ctx:GraphqlParser.UnionTypeExtensionContext):
        pass

    # Exit a parse tree produced by GraphqlParser#unionTypeExtension.
    def exitUnionTypeExtension(self, ctx:GraphqlParser.UnionTypeExtensionContext):
        pass


    # Enter a parse tree produced by GraphqlParser#enumTypeDefinition.
    def enterEnumTypeDefinition(self, ctx:GraphqlParser.EnumTypeDefinitionContext):
        pass

    # Exit a parse tree produced by GraphqlParser#enumTypeDefinition.
    def exitEnumTypeDefinition(self, ctx:GraphqlParser.EnumTypeDefinitionContext):
        pass


    # Enter a parse tree produced by GraphqlParser#enumValuesDefinition.
    def enterEnumValuesDefinition(self, ctx:GraphqlParser.EnumValuesDefinitionContext):
        pass

    # Exit a parse tree produced by GraphqlParser#enumValuesDefinition.
    def exitEnumValuesDefinition(self, ctx:GraphqlParser.EnumValuesDefinitionContext):
        pass


    # Enter a parse tree produced by GraphqlParser#enumValueDefinition.
    def enterEnumValueDefinition(self, ctx:GraphqlParser.EnumValueDefinitionContext):
        pass

    # Exit a parse tree produced by GraphqlParser#enumValueDefinition.
    def exitEnumValueDefinition(self, ctx:GraphqlParser.EnumValueDefinitionContext):
        pass


    # Enter a parse tree produced by GraphqlParser#enumTypeExtension.
    def enterEnumTypeExtension(self, ctx:GraphqlParser.EnumTypeExtensionContext):
        pass

    # Exit a parse tree produced by GraphqlParser#enumTypeExtension.
    def exitEnumTypeExtension(self, ctx:GraphqlParser.EnumTypeExtensionContext):
        pass


    # Enter a parse tree produced by GraphqlParser#inputObjectTypeDefinition.
    def enterInputObjectTypeDefinition(self, ctx:GraphqlParser.InputObjectTypeDefinitionContext):
        pass

    # Exit a parse tree produced by GraphqlParser#inputObjectTypeDefinition.
    def exitInputObjectTypeDefinition(self, ctx:GraphqlParser.InputObjectTypeDefinitionContext):
        pass


    # Enter a parse tree produced by GraphqlParser#inputFieldsDefinition.
    def enterInputFieldsDefinition(self, ctx:GraphqlParser.InputFieldsDefinitionContext):
        pass

    # Exit a parse tree produced by GraphqlParser#inputFieldsDefinition.
    def exitInputFieldsDefinition(self, ctx:GraphqlParser.InputFieldsDefinitionContext):
        pass


    # Enter a parse tree produced by GraphqlParser#inputObjectTypeExtension.
    def enterInputObjectTypeExtension(self, ctx:GraphqlParser.InputObjectTypeExtensionContext):
        pass

    # Exit a parse tree produced by GraphqlParser#inputObjectTypeExtension.
    def exitInputObjectTypeExtension(self, ctx:GraphqlParser.InputObjectTypeExtensionContext):
        pass


    # Enter a parse tree produced by GraphqlParser#directiveDefinition.
    def enterDirectiveDefinition(self, ctx:GraphqlParser.DirectiveDefinitionContext):
        pass

    # Exit a parse tree produced by GraphqlParser#directiveDefinition.
    def exitDirectiveDefinition(self, ctx:GraphqlParser.DirectiveDefinitionContext):
        pass


    # Enter a parse tree produced by GraphqlParser#directiveLocations.
    def enterDirectiveLocations(self, ctx:GraphqlParser.DirectiveLocationsContext):
        pass

    # Exit a parse tree produced by GraphqlParser#directiveLocations.
    def exitDirectiveLocations(self, ctx:GraphqlParser.DirectiveLocationsContext):
        pass


    # Enter a parse tree produced by GraphqlParser#directiveLocation.
    def enterDirectiveLocation(self, ctx:GraphqlParser.DirectiveLocationContext):
        pass

    # Exit a parse tree produced by GraphqlParser#directiveLocation.
    def exitDirectiveLocation(self, ctx:GraphqlParser.DirectiveLocationContext):
        pass


    # Enter a parse tree produced by GraphqlParser#executableDirectiveLocation.
    def enterExecutableDirectiveLocation(self, ctx:GraphqlParser.ExecutableDirectiveLocationContext):
        pass

    # Exit a parse tree produced by GraphqlParser#executableDirectiveLocation.
    def exitExecutableDirectiveLocation(self, ctx:GraphqlParser.ExecutableDirectiveLocationContext):
        pass


    # Enter a parse tree produced by GraphqlParser#typeSystemDirectiveLocation.
    def enterTypeSystemDirectiveLocation(self, ctx:GraphqlParser.TypeSystemDirectiveLocationContext):
        pass

    # Exit a parse tree produced by GraphqlParser#typeSystemDirectiveLocation.
    def exitTypeSystemDirectiveLocation(self, ctx:GraphqlParser.TypeSystemDirectiveLocationContext):
        pass


    # Enter a parse tree produced by GraphqlParser#name.
    def enterName(self, ctx:GraphqlParser.NameContext):
        pass

    # Exit a parse tree produced by GraphqlParser#name.
    def exitName(self, ctx:GraphqlParser.NameContext):
        pass



del GraphqlParser
