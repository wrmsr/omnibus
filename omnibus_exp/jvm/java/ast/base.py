import typing as ta

from .... import dataclasses as dc
from .... import lang


class Name(dc.Pure):
    parts: ta.Sequence[str]


class Type(dc.Pure):

    class Array(dc.Pure):
        size: ta.Optional[int] = None

    name: Name
    generics: ta.Optional[ta.Sequence['Type']] = None
    arrays: ta.Optional[ta.Sequence[Array]] = None


class Access(lang.AutoEnum):
    PUBLIC = ...
    PRIVATE = ...
    PROTECTED = ...
    STATIC = ...
    FINAL = ...
    SYNCHRONIZED = ...
    VOLATILE = ...
    TRANSIENT = ...
    NATIVE = ...
    INTERFACE = ...
    ABSTRACT = ...
    SUPER = ...
    STRICT = ...


KEYWORDS = {
    'abstract',
    'assert',
    'boolean',
    'break',
    'byte',
    'case',
    'catch',
    'char',
    'class',
    'const',
    'continue',
    'default',
    'do',
    'double',
    'else',
    'enum',
    'extends',
    'final',
    'finally',
    'float',
    'for',
    'goto',
    'if',
    'implements',
    'import',
    'instanceof',
    'int',
    'interface',
    'long',
    'native',
    'new',
    'package',
    'private',
    'protected',
    'public',
    'return',
    'short',
    'static',
    'strictfp',
    'super',
    'switch',
    'synchronized',
    'this',
    'throw',
    'throws',
    'transient',
    'try',
    'void',
    'volatile',
    'while',
}


class Param(dc.Pure):
    type: Type
    name: str


class Inheritance(dc.Pure):

    class Kind(lang.AutoEnum):
        EXTENDS = ...
        IMPLEMENTS = ...

    kind: Kind
    name: Name


class Node(dc.Enum):
    pass


class Expression(Node, abstract=True):
    pass


class Statement(Node, abstract=True):
    pass


class Declaration(Node, abstract=True):
    pass
