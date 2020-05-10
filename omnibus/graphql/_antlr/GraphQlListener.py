# flake8: noqa
# Generated from GraphQl.g4 by ANTLR 4.8
from ..._vendor.antlr4 import *
if __name__ is not None and "." in __name__:
    from .GraphQlParser import GraphQlParser
else:
    from GraphQlParser import GraphQlParser

# This class defines a complete listener for a parse tree produced by GraphQlParser.
class GraphQlListener(ParseTreeListener):

    # Enter a parse tree produced by GraphQlParser#document.
    def enterDocument(self, ctx:GraphQlParser.DocumentContext):
        pass

    # Exit a parse tree produced by GraphQlParser#document.
    def exitDocument(self, ctx:GraphQlParser.DocumentContext):
        pass


    # Enter a parse tree produced by GraphQlParser#definition.
    def enterDefinition(self, ctx:GraphQlParser.DefinitionContext):
        pass

    # Exit a parse tree produced by GraphQlParser#definition.
    def exitDefinition(self, ctx:GraphQlParser.DefinitionContext):
        pass


    # Enter a parse tree produced by GraphQlParser#executableDefinition.
    def enterExecutableDefinition(self, ctx:GraphQlParser.ExecutableDefinitionContext):
        pass

    # Exit a parse tree produced by GraphQlParser#executableDefinition.
    def exitExecutableDefinition(self, ctx:GraphQlParser.ExecutableDefinitionContext):
        pass


    # Enter a parse tree produced by GraphQlParser#operationDefinition.
    def enterOperationDefinition(self, ctx:GraphQlParser.OperationDefinitionContext):
        pass

    # Exit a parse tree produced by GraphQlParser#operationDefinition.
    def exitOperationDefinition(self, ctx:GraphQlParser.OperationDefinitionContext):
        pass


    # Enter a parse tree produced by GraphQlParser#operationType.
    def enterOperationType(self, ctx:GraphQlParser.OperationTypeContext):
        pass

    # Exit a parse tree produced by GraphQlParser#operationType.
    def exitOperationType(self, ctx:GraphQlParser.OperationTypeContext):
        pass


    # Enter a parse tree produced by GraphQlParser#selectionSet.
    def enterSelectionSet(self, ctx:GraphQlParser.SelectionSetContext):
        pass

    # Exit a parse tree produced by GraphQlParser#selectionSet.
    def exitSelectionSet(self, ctx:GraphQlParser.SelectionSetContext):
        pass


    # Enter a parse tree produced by GraphQlParser#selection.
    def enterSelection(self, ctx:GraphQlParser.SelectionContext):
        pass

    # Exit a parse tree produced by GraphQlParser#selection.
    def exitSelection(self, ctx:GraphQlParser.SelectionContext):
        pass


    # Enter a parse tree produced by GraphQlParser#field.
    def enterField(self, ctx:GraphQlParser.FieldContext):
        pass

    # Exit a parse tree produced by GraphQlParser#field.
    def exitField(self, ctx:GraphQlParser.FieldContext):
        pass


    # Enter a parse tree produced by GraphQlParser#arguments.
    def enterArguments(self, ctx:GraphQlParser.ArgumentsContext):
        pass

    # Exit a parse tree produced by GraphQlParser#arguments.
    def exitArguments(self, ctx:GraphQlParser.ArgumentsContext):
        pass


    # Enter a parse tree produced by GraphQlParser#argument.
    def enterArgument(self, ctx:GraphQlParser.ArgumentContext):
        pass

    # Exit a parse tree produced by GraphQlParser#argument.
    def exitArgument(self, ctx:GraphQlParser.ArgumentContext):
        pass


    # Enter a parse tree produced by GraphQlParser#alias.
    def enterAlias(self, ctx:GraphQlParser.AliasContext):
        pass

    # Exit a parse tree produced by GraphQlParser#alias.
    def exitAlias(self, ctx:GraphQlParser.AliasContext):
        pass


    # Enter a parse tree produced by GraphQlParser#fragmentSpread.
    def enterFragmentSpread(self, ctx:GraphQlParser.FragmentSpreadContext):
        pass

    # Exit a parse tree produced by GraphQlParser#fragmentSpread.
    def exitFragmentSpread(self, ctx:GraphQlParser.FragmentSpreadContext):
        pass


    # Enter a parse tree produced by GraphQlParser#fragmentDefinition.
    def enterFragmentDefinition(self, ctx:GraphQlParser.FragmentDefinitionContext):
        pass

    # Exit a parse tree produced by GraphQlParser#fragmentDefinition.
    def exitFragmentDefinition(self, ctx:GraphQlParser.FragmentDefinitionContext):
        pass


    # Enter a parse tree produced by GraphQlParser#fragmentName.
    def enterFragmentName(self, ctx:GraphQlParser.FragmentNameContext):
        pass

    # Exit a parse tree produced by GraphQlParser#fragmentName.
    def exitFragmentName(self, ctx:GraphQlParser.FragmentNameContext):
        pass


    # Enter a parse tree produced by GraphQlParser#typeCondition.
    def enterTypeCondition(self, ctx:GraphQlParser.TypeConditionContext):
        pass

    # Exit a parse tree produced by GraphQlParser#typeCondition.
    def exitTypeCondition(self, ctx:GraphQlParser.TypeConditionContext):
        pass


    # Enter a parse tree produced by GraphQlParser#inlineFragment.
    def enterInlineFragment(self, ctx:GraphQlParser.InlineFragmentContext):
        pass

    # Exit a parse tree produced by GraphQlParser#inlineFragment.
    def exitInlineFragment(self, ctx:GraphQlParser.InlineFragmentContext):
        pass


    # Enter a parse tree produced by GraphQlParser#value.
    def enterValue(self, ctx:GraphQlParser.ValueContext):
        pass

    # Exit a parse tree produced by GraphQlParser#value.
    def exitValue(self, ctx:GraphQlParser.ValueContext):
        pass


    # Enter a parse tree produced by GraphQlParser#intValue.
    def enterIntValue(self, ctx:GraphQlParser.IntValueContext):
        pass

    # Exit a parse tree produced by GraphQlParser#intValue.
    def exitIntValue(self, ctx:GraphQlParser.IntValueContext):
        pass


    # Enter a parse tree produced by GraphQlParser#floatValue.
    def enterFloatValue(self, ctx:GraphQlParser.FloatValueContext):
        pass

    # Exit a parse tree produced by GraphQlParser#floatValue.
    def exitFloatValue(self, ctx:GraphQlParser.FloatValueContext):
        pass


    # Enter a parse tree produced by GraphQlParser#booleanValue.
    def enterBooleanValue(self, ctx:GraphQlParser.BooleanValueContext):
        pass

    # Exit a parse tree produced by GraphQlParser#booleanValue.
    def exitBooleanValue(self, ctx:GraphQlParser.BooleanValueContext):
        pass


    # Enter a parse tree produced by GraphQlParser#stringValue.
    def enterStringValue(self, ctx:GraphQlParser.StringValueContext):
        pass

    # Exit a parse tree produced by GraphQlParser#stringValue.
    def exitStringValue(self, ctx:GraphQlParser.StringValueContext):
        pass


    # Enter a parse tree produced by GraphQlParser#nullValue.
    def enterNullValue(self, ctx:GraphQlParser.NullValueContext):
        pass

    # Exit a parse tree produced by GraphQlParser#nullValue.
    def exitNullValue(self, ctx:GraphQlParser.NullValueContext):
        pass


    # Enter a parse tree produced by GraphQlParser#enumValue.
    def enterEnumValue(self, ctx:GraphQlParser.EnumValueContext):
        pass

    # Exit a parse tree produced by GraphQlParser#enumValue.
    def exitEnumValue(self, ctx:GraphQlParser.EnumValueContext):
        pass


    # Enter a parse tree produced by GraphQlParser#listValue.
    def enterListValue(self, ctx:GraphQlParser.ListValueContext):
        pass

    # Exit a parse tree produced by GraphQlParser#listValue.
    def exitListValue(self, ctx:GraphQlParser.ListValueContext):
        pass


    # Enter a parse tree produced by GraphQlParser#objectValue.
    def enterObjectValue(self, ctx:GraphQlParser.ObjectValueContext):
        pass

    # Exit a parse tree produced by GraphQlParser#objectValue.
    def exitObjectValue(self, ctx:GraphQlParser.ObjectValueContext):
        pass


    # Enter a parse tree produced by GraphQlParser#objectField.
    def enterObjectField(self, ctx:GraphQlParser.ObjectFieldContext):
        pass

    # Exit a parse tree produced by GraphQlParser#objectField.
    def exitObjectField(self, ctx:GraphQlParser.ObjectFieldContext):
        pass


    # Enter a parse tree produced by GraphQlParser#variable.
    def enterVariable(self, ctx:GraphQlParser.VariableContext):
        pass

    # Exit a parse tree produced by GraphQlParser#variable.
    def exitVariable(self, ctx:GraphQlParser.VariableContext):
        pass


    # Enter a parse tree produced by GraphQlParser#variableDefinitions.
    def enterVariableDefinitions(self, ctx:GraphQlParser.VariableDefinitionsContext):
        pass

    # Exit a parse tree produced by GraphQlParser#variableDefinitions.
    def exitVariableDefinitions(self, ctx:GraphQlParser.VariableDefinitionsContext):
        pass


    # Enter a parse tree produced by GraphQlParser#variableDefinition.
    def enterVariableDefinition(self, ctx:GraphQlParser.VariableDefinitionContext):
        pass

    # Exit a parse tree produced by GraphQlParser#variableDefinition.
    def exitVariableDefinition(self, ctx:GraphQlParser.VariableDefinitionContext):
        pass


    # Enter a parse tree produced by GraphQlParser#defaultValue.
    def enterDefaultValue(self, ctx:GraphQlParser.DefaultValueContext):
        pass

    # Exit a parse tree produced by GraphQlParser#defaultValue.
    def exitDefaultValue(self, ctx:GraphQlParser.DefaultValueContext):
        pass


    # Enter a parse tree produced by GraphQlParser#type_.
    def enterType_(self, ctx:GraphQlParser.Type_Context):
        pass

    # Exit a parse tree produced by GraphQlParser#type_.
    def exitType_(self, ctx:GraphQlParser.Type_Context):
        pass


    # Enter a parse tree produced by GraphQlParser#namedType.
    def enterNamedType(self, ctx:GraphQlParser.NamedTypeContext):
        pass

    # Exit a parse tree produced by GraphQlParser#namedType.
    def exitNamedType(self, ctx:GraphQlParser.NamedTypeContext):
        pass


    # Enter a parse tree produced by GraphQlParser#listType.
    def enterListType(self, ctx:GraphQlParser.ListTypeContext):
        pass

    # Exit a parse tree produced by GraphQlParser#listType.
    def exitListType(self, ctx:GraphQlParser.ListTypeContext):
        pass


    # Enter a parse tree produced by GraphQlParser#directives.
    def enterDirectives(self, ctx:GraphQlParser.DirectivesContext):
        pass

    # Exit a parse tree produced by GraphQlParser#directives.
    def exitDirectives(self, ctx:GraphQlParser.DirectivesContext):
        pass


    # Enter a parse tree produced by GraphQlParser#directive.
    def enterDirective(self, ctx:GraphQlParser.DirectiveContext):
        pass

    # Exit a parse tree produced by GraphQlParser#directive.
    def exitDirective(self, ctx:GraphQlParser.DirectiveContext):
        pass


    # Enter a parse tree produced by GraphQlParser#typeSystemDefinition.
    def enterTypeSystemDefinition(self, ctx:GraphQlParser.TypeSystemDefinitionContext):
        pass

    # Exit a parse tree produced by GraphQlParser#typeSystemDefinition.
    def exitTypeSystemDefinition(self, ctx:GraphQlParser.TypeSystemDefinitionContext):
        pass


    # Enter a parse tree produced by GraphQlParser#typeSystemExtension.
    def enterTypeSystemExtension(self, ctx:GraphQlParser.TypeSystemExtensionContext):
        pass

    # Exit a parse tree produced by GraphQlParser#typeSystemExtension.
    def exitTypeSystemExtension(self, ctx:GraphQlParser.TypeSystemExtensionContext):
        pass


    # Enter a parse tree produced by GraphQlParser#schemaDefinition.
    def enterSchemaDefinition(self, ctx:GraphQlParser.SchemaDefinitionContext):
        pass

    # Exit a parse tree produced by GraphQlParser#schemaDefinition.
    def exitSchemaDefinition(self, ctx:GraphQlParser.SchemaDefinitionContext):
        pass


    # Enter a parse tree produced by GraphQlParser#rootOperationTypeDefinition.
    def enterRootOperationTypeDefinition(self, ctx:GraphQlParser.RootOperationTypeDefinitionContext):
        pass

    # Exit a parse tree produced by GraphQlParser#rootOperationTypeDefinition.
    def exitRootOperationTypeDefinition(self, ctx:GraphQlParser.RootOperationTypeDefinitionContext):
        pass


    # Enter a parse tree produced by GraphQlParser#schemaExtension.
    def enterSchemaExtension(self, ctx:GraphQlParser.SchemaExtensionContext):
        pass

    # Exit a parse tree produced by GraphQlParser#schemaExtension.
    def exitSchemaExtension(self, ctx:GraphQlParser.SchemaExtensionContext):
        pass


    # Enter a parse tree produced by GraphQlParser#operationTypeDefinition.
    def enterOperationTypeDefinition(self, ctx:GraphQlParser.OperationTypeDefinitionContext):
        pass

    # Exit a parse tree produced by GraphQlParser#operationTypeDefinition.
    def exitOperationTypeDefinition(self, ctx:GraphQlParser.OperationTypeDefinitionContext):
        pass


    # Enter a parse tree produced by GraphQlParser#description.
    def enterDescription(self, ctx:GraphQlParser.DescriptionContext):
        pass

    # Exit a parse tree produced by GraphQlParser#description.
    def exitDescription(self, ctx:GraphQlParser.DescriptionContext):
        pass


    # Enter a parse tree produced by GraphQlParser#typeDefinition.
    def enterTypeDefinition(self, ctx:GraphQlParser.TypeDefinitionContext):
        pass

    # Exit a parse tree produced by GraphQlParser#typeDefinition.
    def exitTypeDefinition(self, ctx:GraphQlParser.TypeDefinitionContext):
        pass


    # Enter a parse tree produced by GraphQlParser#typeExtension.
    def enterTypeExtension(self, ctx:GraphQlParser.TypeExtensionContext):
        pass

    # Exit a parse tree produced by GraphQlParser#typeExtension.
    def exitTypeExtension(self, ctx:GraphQlParser.TypeExtensionContext):
        pass


    # Enter a parse tree produced by GraphQlParser#scalarTypeDefinition.
    def enterScalarTypeDefinition(self, ctx:GraphQlParser.ScalarTypeDefinitionContext):
        pass

    # Exit a parse tree produced by GraphQlParser#scalarTypeDefinition.
    def exitScalarTypeDefinition(self, ctx:GraphQlParser.ScalarTypeDefinitionContext):
        pass


    # Enter a parse tree produced by GraphQlParser#scalarTypeExtension.
    def enterScalarTypeExtension(self, ctx:GraphQlParser.ScalarTypeExtensionContext):
        pass

    # Exit a parse tree produced by GraphQlParser#scalarTypeExtension.
    def exitScalarTypeExtension(self, ctx:GraphQlParser.ScalarTypeExtensionContext):
        pass


    # Enter a parse tree produced by GraphQlParser#objectTypeDefinition.
    def enterObjectTypeDefinition(self, ctx:GraphQlParser.ObjectTypeDefinitionContext):
        pass

    # Exit a parse tree produced by GraphQlParser#objectTypeDefinition.
    def exitObjectTypeDefinition(self, ctx:GraphQlParser.ObjectTypeDefinitionContext):
        pass


    # Enter a parse tree produced by GraphQlParser#implementsInterfaces.
    def enterImplementsInterfaces(self, ctx:GraphQlParser.ImplementsInterfacesContext):
        pass

    # Exit a parse tree produced by GraphQlParser#implementsInterfaces.
    def exitImplementsInterfaces(self, ctx:GraphQlParser.ImplementsInterfacesContext):
        pass


    # Enter a parse tree produced by GraphQlParser#fieldsDefinition.
    def enterFieldsDefinition(self, ctx:GraphQlParser.FieldsDefinitionContext):
        pass

    # Exit a parse tree produced by GraphQlParser#fieldsDefinition.
    def exitFieldsDefinition(self, ctx:GraphQlParser.FieldsDefinitionContext):
        pass


    # Enter a parse tree produced by GraphQlParser#fieldDefinition.
    def enterFieldDefinition(self, ctx:GraphQlParser.FieldDefinitionContext):
        pass

    # Exit a parse tree produced by GraphQlParser#fieldDefinition.
    def exitFieldDefinition(self, ctx:GraphQlParser.FieldDefinitionContext):
        pass


    # Enter a parse tree produced by GraphQlParser#argumentsDefinition.
    def enterArgumentsDefinition(self, ctx:GraphQlParser.ArgumentsDefinitionContext):
        pass

    # Exit a parse tree produced by GraphQlParser#argumentsDefinition.
    def exitArgumentsDefinition(self, ctx:GraphQlParser.ArgumentsDefinitionContext):
        pass


    # Enter a parse tree produced by GraphQlParser#inputValueDefinition.
    def enterInputValueDefinition(self, ctx:GraphQlParser.InputValueDefinitionContext):
        pass

    # Exit a parse tree produced by GraphQlParser#inputValueDefinition.
    def exitInputValueDefinition(self, ctx:GraphQlParser.InputValueDefinitionContext):
        pass


    # Enter a parse tree produced by GraphQlParser#objectTypeExtension.
    def enterObjectTypeExtension(self, ctx:GraphQlParser.ObjectTypeExtensionContext):
        pass

    # Exit a parse tree produced by GraphQlParser#objectTypeExtension.
    def exitObjectTypeExtension(self, ctx:GraphQlParser.ObjectTypeExtensionContext):
        pass


    # Enter a parse tree produced by GraphQlParser#interfaceTypeDefinition.
    def enterInterfaceTypeDefinition(self, ctx:GraphQlParser.InterfaceTypeDefinitionContext):
        pass

    # Exit a parse tree produced by GraphQlParser#interfaceTypeDefinition.
    def exitInterfaceTypeDefinition(self, ctx:GraphQlParser.InterfaceTypeDefinitionContext):
        pass


    # Enter a parse tree produced by GraphQlParser#interfaceTypeExtension.
    def enterInterfaceTypeExtension(self, ctx:GraphQlParser.InterfaceTypeExtensionContext):
        pass

    # Exit a parse tree produced by GraphQlParser#interfaceTypeExtension.
    def exitInterfaceTypeExtension(self, ctx:GraphQlParser.InterfaceTypeExtensionContext):
        pass


    # Enter a parse tree produced by GraphQlParser#unionTypeDefinition.
    def enterUnionTypeDefinition(self, ctx:GraphQlParser.UnionTypeDefinitionContext):
        pass

    # Exit a parse tree produced by GraphQlParser#unionTypeDefinition.
    def exitUnionTypeDefinition(self, ctx:GraphQlParser.UnionTypeDefinitionContext):
        pass


    # Enter a parse tree produced by GraphQlParser#unionMemberTypes.
    def enterUnionMemberTypes(self, ctx:GraphQlParser.UnionMemberTypesContext):
        pass

    # Exit a parse tree produced by GraphQlParser#unionMemberTypes.
    def exitUnionMemberTypes(self, ctx:GraphQlParser.UnionMemberTypesContext):
        pass


    # Enter a parse tree produced by GraphQlParser#unionTypeExtension.
    def enterUnionTypeExtension(self, ctx:GraphQlParser.UnionTypeExtensionContext):
        pass

    # Exit a parse tree produced by GraphQlParser#unionTypeExtension.
    def exitUnionTypeExtension(self, ctx:GraphQlParser.UnionTypeExtensionContext):
        pass


    # Enter a parse tree produced by GraphQlParser#enumTypeDefinition.
    def enterEnumTypeDefinition(self, ctx:GraphQlParser.EnumTypeDefinitionContext):
        pass

    # Exit a parse tree produced by GraphQlParser#enumTypeDefinition.
    def exitEnumTypeDefinition(self, ctx:GraphQlParser.EnumTypeDefinitionContext):
        pass


    # Enter a parse tree produced by GraphQlParser#enumValuesDefinition.
    def enterEnumValuesDefinition(self, ctx:GraphQlParser.EnumValuesDefinitionContext):
        pass

    # Exit a parse tree produced by GraphQlParser#enumValuesDefinition.
    def exitEnumValuesDefinition(self, ctx:GraphQlParser.EnumValuesDefinitionContext):
        pass


    # Enter a parse tree produced by GraphQlParser#enumValueDefinition.
    def enterEnumValueDefinition(self, ctx:GraphQlParser.EnumValueDefinitionContext):
        pass

    # Exit a parse tree produced by GraphQlParser#enumValueDefinition.
    def exitEnumValueDefinition(self, ctx:GraphQlParser.EnumValueDefinitionContext):
        pass


    # Enter a parse tree produced by GraphQlParser#enumTypeExtension.
    def enterEnumTypeExtension(self, ctx:GraphQlParser.EnumTypeExtensionContext):
        pass

    # Exit a parse tree produced by GraphQlParser#enumTypeExtension.
    def exitEnumTypeExtension(self, ctx:GraphQlParser.EnumTypeExtensionContext):
        pass


    # Enter a parse tree produced by GraphQlParser#inputObjectTypeDefinition.
    def enterInputObjectTypeDefinition(self, ctx:GraphQlParser.InputObjectTypeDefinitionContext):
        pass

    # Exit a parse tree produced by GraphQlParser#inputObjectTypeDefinition.
    def exitInputObjectTypeDefinition(self, ctx:GraphQlParser.InputObjectTypeDefinitionContext):
        pass


    # Enter a parse tree produced by GraphQlParser#inputFieldsDefinition.
    def enterInputFieldsDefinition(self, ctx:GraphQlParser.InputFieldsDefinitionContext):
        pass

    # Exit a parse tree produced by GraphQlParser#inputFieldsDefinition.
    def exitInputFieldsDefinition(self, ctx:GraphQlParser.InputFieldsDefinitionContext):
        pass


    # Enter a parse tree produced by GraphQlParser#inputObjectTypeExtension.
    def enterInputObjectTypeExtension(self, ctx:GraphQlParser.InputObjectTypeExtensionContext):
        pass

    # Exit a parse tree produced by GraphQlParser#inputObjectTypeExtension.
    def exitInputObjectTypeExtension(self, ctx:GraphQlParser.InputObjectTypeExtensionContext):
        pass


    # Enter a parse tree produced by GraphQlParser#directiveDefinition.
    def enterDirectiveDefinition(self, ctx:GraphQlParser.DirectiveDefinitionContext):
        pass

    # Exit a parse tree produced by GraphQlParser#directiveDefinition.
    def exitDirectiveDefinition(self, ctx:GraphQlParser.DirectiveDefinitionContext):
        pass


    # Enter a parse tree produced by GraphQlParser#directiveLocations.
    def enterDirectiveLocations(self, ctx:GraphQlParser.DirectiveLocationsContext):
        pass

    # Exit a parse tree produced by GraphQlParser#directiveLocations.
    def exitDirectiveLocations(self, ctx:GraphQlParser.DirectiveLocationsContext):
        pass


    # Enter a parse tree produced by GraphQlParser#directiveLocation.
    def enterDirectiveLocation(self, ctx:GraphQlParser.DirectiveLocationContext):
        pass

    # Exit a parse tree produced by GraphQlParser#directiveLocation.
    def exitDirectiveLocation(self, ctx:GraphQlParser.DirectiveLocationContext):
        pass


    # Enter a parse tree produced by GraphQlParser#executableDirectiveLocation.
    def enterExecutableDirectiveLocation(self, ctx:GraphQlParser.ExecutableDirectiveLocationContext):
        pass

    # Exit a parse tree produced by GraphQlParser#executableDirectiveLocation.
    def exitExecutableDirectiveLocation(self, ctx:GraphQlParser.ExecutableDirectiveLocationContext):
        pass


    # Enter a parse tree produced by GraphQlParser#typeSystemDirectiveLocation.
    def enterTypeSystemDirectiveLocation(self, ctx:GraphQlParser.TypeSystemDirectiveLocationContext):
        pass

    # Exit a parse tree produced by GraphQlParser#typeSystemDirectiveLocation.
    def exitTypeSystemDirectiveLocation(self, ctx:GraphQlParser.TypeSystemDirectiveLocationContext):
        pass


    # Enter a parse tree produced by GraphQlParser#name.
    def enterName(self, ctx:GraphQlParser.NameContext):
        pass

    # Exit a parse tree produced by GraphQlParser#name.
    def exitName(self, ctx:GraphQlParser.NameContext):
        pass



del GraphQlParser
