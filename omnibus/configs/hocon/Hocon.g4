grammar Hocon;


COMMENT
   : ('#'|'//') ~( '\r' | '\n' )* -> skip
   ;

NUMBER
   : '-'? INT '.' [0-9] + EXP? | '-'? INT EXP | '-'? INT
   ;

STRING
   : '"' (ESC | ~ ["\\])* '"'
   | '\'' (ESC | ~ ['\\])* '\''
   ;

PATH_ELEMENT
   : (ALPHANUM|'-'|'_')+
   ;

REFERENCE
   : '${' PATH_ELEMENT ('.' PATH_ELEMENT)* '}'
   ;

KV : [=:]
   ;

WS
   : [ \t\n\r] + -> skip
   ;

fragment ESC
   : '\\' (["\\/bfnrt] | UNICODE)
   ;


fragment UNICODE
   : 'u' HEX HEX HEX HEX
   ;

fragment ALPHANUM
   : ('0' .. '9') | ('a'..'z') | ('A' .. 'Z')
   ;

fragment HEX
   : [0-9a-fA-F]
   ;

fragment INT
   : '0' | [1-9] [0-9]*
   ;

// no leading zeros

fragment EXP
   : [Ee] [+\-]? INT
   ;

// \- since - means "range" inside [...]

//======================================================================================

path
   : PATH_ELEMENT ('.' PATH_ELEMENT)*
   ;

key
   : path
   | STRING
   ;

hocon
   : obj*
   | array*
   | prop*
   ;

obj
   : objectBegin prop (','? prop)* objectEnd
   | objectBegin objectEnd
   ;

prop
   : objectData
   | arrayData
   | stringData
   | referenceData
   | numberData
   ;

rawstring
   : (PATH_ELEMENT|'-')+
   ;

stringValue
   : STRING stringValue*       #v_string
   | rawstring stringValue*    #v_rawstring
   | REFERENCE stringValue*    #v_reference
   ;

// object data

objectBegin
   : '{'
   ;

objectEnd
   : '}'
   ;

objectData
   : key KV? obj
   ;

arrayData
   : key KV array
   ;

stringData
   : key KV stringValue
   ;

referenceData
   : key KV REFERENCE
   ;

numberData
   : key KV NUMBER
   ;

// array data

arrayBegin
   : '['
   ;

arrayEnd
   : ']'
   ;

array
   : arrayBegin arrayValue (','? arrayValue)* arrayEnd
   | arrayBegin arrayEnd
   ;

arrayString: stringValue;
arrayReference: REFERENCE;
arrayNumber: NUMBER;
arrayObj: obj;
arrayArray: array;

arrayValue
   : arrayString
   | arrayReference
   | arrayNumber
   | arrayObj
   | arrayArray
   ;