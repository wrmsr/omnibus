import typing as ta

from .. import dataclasses as dc
from .. import lang


class Node(dc.Frozen, abstract=True, sealed=True):
    pass


class Operator(Node, abstract=True, sealed=True):
    pass


class Leaf(Node, abstract=True, sealed=True):
    pass


class And(Operator, final=True):
    left: Node
    right: Node


class Compare(Operator, final=True):
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


class CreateArray(Node, final=True):
    items: ta.Sequence[Node]


class CreateObject(Node, final=True):
    fields: ta.Mapping[str, Node]


class Current(Leaf, final=True):
    pass


class ExpressionRef(Node, final=True):
    expr: Node


class FlattenArray(Leaf, final=True):
    pass


class FlattenObject(Leaf, final=True):
    pass


class FunctionCall(Node, final=True):
    name: str
    args: ta.Sequence[Node]


class Index(Leaf, final=True):
    value: int


class JsonLiteral(Leaf, final=True):
    text: str


class Negate(Node, final=True):
    item: Node


class Or(Operator, final=True):
    left: Node
    right: Node


class Parameter(Leaf, final=True):
    class Target(dc.Enum, sealed=True):
        pass

    class NumberTarget(Target):
        value: int

    class NameTarget(Target):
        value: str

    target: Target


class Project(Node, final=True):
    child: Node


class Property(Leaf, final=True):
    name: str


class Selection(Node, final=True):
    child: Node


class Sequence(Node, final=True):
    items: ta.Sequence[Node]


class Slice(Leaf, final=True):
    start: ta.Optional[int]
    stop: ta.Optional[int]
    step: ta.Optional[int]


class String(Leaf, final=True):
    value: Node
