import ast  # noqa
import typing as ta

from ... import lang
from .base import Args
from .base import Expr
from .base import Exprs
from .base import Keyword
from .base import Node
from .ops import BinOp
from .ops import BoolOp
from .ops import CmpOp
from .ops import UnaryOp


class Context(lang.AutoEnum):
    AUG_LOAD = ...
    AUG_STORE = ...
    DEL = ...
    LOAD = ...
    PARAM = ...
    STORE = ...


class FormatConversion(lang.ValueEnum):
    NONE = 0
    STR = 1
    REPR = 2
    ASCII = 3


class Attribute(Expr):
    value: Expr
    attr: str


class Await(Expr):
    value: Expr


class BinExpr(Expr):
    left: Expr
    op: BinOp
    right: Expr


class BoolExpr(Expr):
    op: BoolOp
    values: Expr


class Bytes(Expr):
    value: str


class Call(Expr):
    func: Expr
    args: Exprs = ()
    keywords: ta.Sequence[Keyword] = ()


class Compare(Expr):
    left: Expr
    cmps: ta.Sequence[ta.Tuple[CmpOp, Expr]]


class Constant(Expr):
    value: ta.Any
    kind: ta.Any = None


class Dict(Expr):
    items: ta.Union[ta.Tuple[str, Expr], Expr]


class Comp(Node):
    target: 'Expr'
    iter: 'Expr'
    ifs: ta.Optional[Exprs] = None
    is_async: bool = False


class DictComp(Expr):
    key: Expr
    value: Expr
    comps: ta.Sequence[Comp]


class FormattedValue(Expr):
    value: Expr
    conversion: int
    spec: ta.Optional[str] = None


class GeneratorExp(Expr):
    value: Expr
    comps: ta.Sequence[Comp]


class IfExp(Expr):
    test: Expr
    body: Expr
    or_else: Expr


class JoinedStr(Expr):
    values: Exprs


class Lambda(Expr):
    args: Args
    body: Expr


class List(Expr):
    items: Exprs


class ListComp(Expr):
    value: Expr
    comps: ta.Sequence[Comp]


class Name(Expr):
    name: str


class NamedExpr(Expr):
    target: Name
    value: Expr


class Set(Expr):
    items: Exprs


class SetComp(Expr):
    value: Expr
    comps: ta.Sequence[Comp]


class Starred(Expr):
    value: Expr


class Subscript(Expr):
    value: Expr
    slice: Expr


class Tuple(Expr):
    items: Exprs


class UnaryExpr(Expr):
    op: UnaryOp
    value: Expr


class Yield(Expr):
    value: Expr


class YieldFrom(Expr):
    value: Expr
