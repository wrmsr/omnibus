/*
A Protocol Buffers 3 grammar for ANTLR v4.

Derived and adapted from:
https://developers.google.com/protocol-buffers/docs/reference/proto3-spec

@author Marco Willemart
*/
grammar Protobuf3;


proto
    : syntax (syntaxExtra)* EOF
    ;

syntax
    : SYNTAX '=' (PROTO3_DOUBLE | PROTO3_SINGLE) ';'
    ;

syntaxExtra
    : importStatement
    | packageStatement
    | option
    | topLevelDef
    | emptyStatement
    ;

importStatement
    : IMPORT (WEAK | PUBLIC)? StrLit ';'
    ;

packageStatement
    : PACKAGE fullIdent ';'
    ;

option
    : OPTION optionName '=' (constant | optionBody)  ';'
    ;

optionName
    : (Ident | '(' fullIdent ')' ) ('.' (Ident | reservedWord))*
    ;

optionBody
    : '{' (optionBodyVariable)* '}'
    ;

optionBodyVariable
    : optionName ':' constant
    ;

topLevelDef
    : message
    | enumDefinition
    | extend
    | service
    ;

message
    : MESSAGE messageName messageBody
    ;

messageBody
    : '{' (messageBodyContent)* '}'
    ;

messageBodyContent
    : field
    | enumDefinition
    | message
    | extend
    | option
    | oneof
    | mapField
    | reserved
    | emptyStatement
    ;

enumDefinition
    : ENUM enumName enumBody
    ;

enumBody
    :  '{' (option | enumField |emptyStatement)* '}'
    ;

enumField
    : Ident '=' '-'? IntLit ('[' enumValueOption (','  enumValueOption)* ']')? ';'
    ;

enumValueOption
    : optionName '=' constant
    ;

extend
    : EXTEND messageType '{' (field | emptyStatement) '}'
    ;

service
    : SERVICE serviceName '{' (option | rpc | emptyStatement)* '}'
    ;

rpc
    : RPC rpcName '(' STREAM? messageType ')'
      RETURNS '(' STREAM? messageType ')'
      (('{' (option | emptyStatement)* '}') | ';')
    ;

reserved
    : RESERVED (ranges | fieldNames) ';'
    ;

ranges
    : rangeRule (',' rangeRule)*
    ;

rangeRule
    : IntLit
    | IntLit TO IntLit
    ;

fieldNames
    : StrLit (',' StrLit)*
    ;

typeRule
    : simpleType
    | messageOrEnumType
    ;

simpleType
    : DOUBLE
    | FLOAT
    | INT32
    | INT64
    | UINT32
    | UINT64
    | SINT32
    | SINT64
    | FIXED32
    | FIXED64
    | SFIXED32
    | SFIXED64
    | BOOL
    | STRING
    | BYTES
    ;

fieldNumber
    : IntLit
    ;

field
    : REPEATED? typeRule fieldName '=' fieldNumber ('[' fieldOptions ']')? ';'
    ;

fieldOptions
    : fieldOption (','  fieldOption)*
    ;

fieldOption
    : optionName '=' constant
    ;

oneof
    : ONEOF oneofName '{' (oneofField | emptyStatement)* '}'
    ;

oneofField
    : typeRule fieldName '=' fieldNumber ('[' fieldOptions ']')? ';'
    ;

mapField
    : MAP '<' keyType ',' typeRule '>' mapName '=' fieldNumber ('[' fieldOptions ']')? ';'
    ;

keyType
    : INT32
    | INT64
    | UINT32
    | UINT64
    | SINT32
    | SINT64
    | FIXED32
    | FIXED64
    | SFIXED32
    | SFIXED64
    | BOOL
    | STRING
    ;

reservedWord
    : EXTEND
    | MESSAGE
    | OPTION
    | PACKAGE
    | RPC
    | SERVICE
    | STREAM
    | STRING
    | SYNTAX
    | WEAK
    ;

BOOL: 'bool';
BYTES: 'bytes';
DOUBLE: 'double';
ENUM: 'enum';
EXTEND: 'extend';
FIXED32: 'fixed32';
FIXED64: 'fixed64';
FLOAT: 'float';
IMPORT: 'import';
INT32: 'int32';
INT64: 'int64';
MAP: 'map';
MESSAGE: 'message';
ONEOF: 'oneof';
OPTION: 'option';
PACKAGE: 'package';
PROTO3_DOUBLE: '"proto3"';
PROTO3_SINGLE: '\'proto3\'';
PUBLIC: 'public';
REPEATED: 'repeated';
RESERVED: 'reserved';
RETURNS: 'returns';
RPC: 'rpc';
SERVICE: 'service';
SFIXED32: 'sfixed32';
SFIXED64: 'sfixed64';
SINT32: 'sint32';
SINT64: 'sint64';
STREAM: 'stream';
STRING: 'string';
SYNTAX: 'syntax';
TO: 'to';
UINT32: 'uint32';
UINT64: 'uint64';
WEAK: 'weak';

fragment Letter
    : [A-Za-z_]
    ;

fragment DecimalDigit
    : [0-9]
    ;

fragment OctalDigit
    : [0-7]
    ;

fragment HexDigit
    : [0-9A-Fa-f]
    ;

Ident
    : Letter (Letter | DecimalDigit)*
    ;

fullIdent
    : Ident ('.' Ident)*
    ;

messageName
    : Ident
    ;

enumName
    : Ident
    ;

messageOrEnumName
    : Ident
    ;

fieldName
    : Ident
    | reservedWord
    ;

oneofName
    : Ident
    ;

mapName
    : Ident
    ;

serviceName
    : Ident
    ;

rpcName
    : Ident
    ;

messageType
    : '.'? (Ident '.')* messageName
    ;

messageOrEnumType
    : '.'? ( (Ident | reservedWord) '.')* messageOrEnumName
    ;

IntLit
    : DecimalLit
    | OctalLit
    | HexLit
    ;

fragment DecimalLit
    : [1-9] DecimalDigit*
    ;

fragment OctalLit
    : '0' OctalDigit*
    ;

fragment HexLit
    : '0' ('x' | 'X') HexDigit+
    ;

FloatLit
    : (Decimals '.' Decimals? Exponent? | Decimals Exponent | '.' Decimals Exponent?)
    | 'inf'
    | 'nan'
    ;

fragment Decimals
    : DecimalDigit+
    ;

fragment Exponent
    : ('e' | 'E') ('+' | '-')? Decimals
    ;

BoolLit
    : 'true'
    | 'false'
    ;

StrLit
    : '\'' CharValue* '\''
    | '"' CharValue* '"'
    ;

fragment CharValue
    : HexEscape
    | OctEscape
    | CharEscape
    | ~[\u0000\n\\]
    ;

fragment HexEscape
    : '\\' ('x' | 'X') HexDigit HexDigit
    ;

fragment OctEscape
    : '\\' OctalDigit OctalDigit OctalDigit
    ;

fragment CharEscape
    : '\\' [abfnrtv\\'"]
    ;

Quote
    : '\''
    | '"'
    ;

emptyStatement
    :   ';'
    ;

constant
    : fullIdent
    | ('-' | '+')? IntLit
    | ('-' | '+')? FloatLit
    | StrLit
    | BoolLit
    ;

WS
    : [ \t\r\n\u000C]+ -> channel(2)
    ;

COMMENT
    : '/*' .*? '*/' -> channel(2)
    ;

LINE_COMMENT
    : '//' ~[\r\n]* -> channel(2)
    ;
