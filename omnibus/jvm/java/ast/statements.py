import typing as ta

from .base import Expression
from .base import Statement
from .base import Name
from .base import Type


class AnnotatedStatement(Statement):
    annotation: Name
    args: ta.Sequence[Expression]
    statement: Statement


class Blank(Statement):
    pass


class Block(Statement):
    body: ta.Sequence[Statement]


class Break(Statement):
    label: ta.Optional[str] = None


class Case(Statement):
    values: ta.Sequence[ta.Any]
    is_default: bool
    block: Block


class Continue(Statement):
    label: ta.Optional[str] = None


class DoWhile(Statement):
    body: Block
    condition: Expression


class Empty(Statement):
    pass


class ExpressionStatement(Statement):
    expression: Expression


class ForEach(Statement):
    type: Type
    item: str
    iterable: Expression
    body: Block


class If(Statement):
    condition: Expression
    if_true: Block
    if_false: ta.Optional[Block] = None


class Labeled(Statement):
    label: str
    statement: Statement


class RawStatement(Statement):
    text: str


class Return(Statement):
    value: ta.Optional[Expression] = None


class Switch(Statement):
    selector: Expression
    cases: ta.Sequence[Case]


class Throw(Statement):
    exception: Expression


class Variable(Statement):
    type: Type
    name: str
    value: ta.Optional[Expression] = None


class While(Statement):
    condition: Expression
    body: Block
