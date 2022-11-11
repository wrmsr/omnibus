import typing as ta

from .... import lang
from .base import Access
from .base import Declaration
from .base import Expression
from .base import Inheritance
from .base import Name
from .base import Param
from .base import Statement
from .base import Type


class AnnotatedDeclaration(Declaration):
    annotation: Name
    args: ta.Optional[ta.Sequence[Expression]]
    declaration: Declaration


class Constructor(Declaration):
    access: ta.Sequence[Access]
    name: str
    params: ta.Sequence[Param]
    body: Statement


class Field(Declaration):
    access: ta.Sequence[Access]
    type: Type
    name: str
    value: ta.Optional[Expression] = None


class Initialization(Declaration):
    body: Statement


class Method(Declaration):
    access: ta.Sequence[Access]
    type: Type
    name: str
    params: ta.Sequence[Param]
    body: Statement


class RawDeclaration(Declaration):
    text: str


class TypeDeclaration(Declaration):

    class Kind(lang.AutoEnum):
        CLASS = ...
        INTERFACE = ...
        ENUM = ...

    access: ta.Sequence[Access]
    kind: Kind
    name: str
    inheritance: ta.Sequence[Inheritance]
    body: ta.Sequence[Declaration]
