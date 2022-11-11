import typing as ta

from .... import lang
from .base import Expression
from .base import Name
from .base import Statement
from .base import Type


class ArrayAccess(Expression):
    array: Expression
    index: Expression


class Assignment(Expression):
    left: Expression
    right: Expression


class BigArrayLiteral(Expression):
    expressions: ta.Sequence[Expression]


class BigStringLiteral(Expression):
    value: str


class Binary(Expression):

    class Op(lang.ValueEnum):
        ADD = '+'
        SUBTRACT = '-'
        MULTIPLY = '*'
        DIVIDE = '/'
        REMAINDER = '%'
        LEFT_SHIFT = '<<'
        RIGHT_SHIFT_SIGNED = '>>'
        RIGHT_SHIFT_UNSIGNED = '>>>'
        LESS_THAN = '<'
        LESS_THAN_OR_EQUAL = '<='
        GREATER_THAN = '>'
        GREATER_THAN_OR_EQUAL = '>='
        INSTANCE_OF = 'instanceof'
        EQUALS = '=='
        NOTEQUALS = '!='
        BITWISE_AND = '&'
        BITWISE_OR = '|'
        BITWISE_XOR = '^'
        CONDITIONAL_AND = '&&'
        CONDITIONAL_OR = '||'

    op: Op
    left: Expression
    right: Expression


class Cast(Expression):
    type: Type
    value: Expression


class Conditional(Expression):
    condition: Expression
    if_true: Expression
    if_false: Expression


class Ident(Expression):
    name: Name


class Lambda(Expression):
    params: ta.Sequence[str]
    body: Statement


class Literal(Expression):
    value: ta.Any


class MemberAccess(Expression):
    instance: Expression
    member: str


class MethodInvocation(Expression):
    method: Expression
    args: ta.Sequence[Expression]


class MethodReference(Expression):
    instance: Expression
    method_name: str


class New(Expression):
    type: Type
    args: ta.Sequence[Expression]


class NewArray(Expression):
    type: Type
    items: ta.Sequence[Expression]


class RawExpression(Expression):
    text: str


class UnaryOpRepr(ta.NamedTuple):
    prefix: str
    suffix: str


class Unary(Expression):

    class Op(lang.ValueEnum):
        Plus = UnaryOpRepr('+', '')
        Minus = UnaryOpRepr('-', '')
        PreIncrement = UnaryOpRepr('++', '')
        PreDecrement = UnaryOpRepr('--', '')
        PostIncrement = UnaryOpRepr('', '++')
        PostDecrement = UnaryOpRepr('', '--')
        BitwiseComplement = UnaryOpRepr('~', '')
        LogicalComplement = UnaryOpRepr('!', '')

    op: Op
    value: Expression
