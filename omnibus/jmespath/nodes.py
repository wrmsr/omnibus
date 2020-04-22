import typing as ta

from .. import dataclasses as dc
from .. import lang


class Node(dc.Data, abstract=True, frozen=True, sealed=True):
    pass


class Operator(Node, abstract=True, frozen=True):
    pass


class Leaf(Node, abstract=True, frozen=True):
    pass


class And(Operator, frozen=True, final=True):
    left: Node
    right: Node


class Compare(Operator, frozen=True, final=True):
    class Op(lang.ValueEnum):
        EQ = '=='
        NE = '!='
        GT = '>'
        GE = '>='
        LT = '<'
        LE = '<='

    Op._by_value = {v: k for k, v in Op._by_name.items()}

    op: Op
    left: Node
    right: Node


class CreateArray(Node, frozen=True, final=True):
    items: ta.Sequence[Node]


class CreateObject(Node, frozen=True, final=True):
    fields: ta.Mapping[str, Node]


class Current(Leaf, frozen=True, final=True):
    pass


class ExpressionRef(Node, frozen=True, final=True):
    expr: Node


class FlattenArray(Leaf, frozen=True, final=True):
    pass


class FlattenObject(Leaf, frozen=True, final=True):
    pass


class FunctionCall(Node, frozen=True, final=True):
    name: str
    args: ta.Sequence[Node]


class Index(Leaf, frozen=True, final=True):
    value: int


class JsonLiteral(Leaf, frozen=True, final=True):
    text: str


class Negate(Node, frozen=True, final=True):
    item: Node


class Or(Operator, frozen=True, final=True):
    left: Node
    right: Node


class Parameter(Leaf, frozen=True, final=True):
    class Target(dc.Data, frozen=True, abstract=True, sealed=True):
        pass

    class NumberTarget(Target, frozen=True, final=True):
        value: int

    class NameTarget(Target, frozen=True, final=True):
        value: str

    target: Target


class Project(Node, frozen=True, final=True):
    child: Node


class Property(Leaf, frozen=True, final=True):
    name: str


class Selection(Node, frozen=True, final=True):
    child: Node


class Sequence(Node, frozen=True, final=True):
    items: ta.Sequence[Node]


class Slice(Leaf, frozen=True, final=True):
    start: ta.Optional[int]
    stop: ta.Optional[int]
    step: ta.Optional[int]


class String(Leaf, frozen=True, final=True):
    value: Node
