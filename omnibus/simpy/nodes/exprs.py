import typing as ta

from ... import dataclasses as dc
from ... import lang
from .base import check_ident
from .base import Expr
from .base import Ident
from .base import Node


class Const(Expr):
    value: ta.Any


class GetVar(Expr):
    name: Ident = dc.field(check=check_ident)


class GetAttr(Expr):
    obj: Expr
    attr: Ident = dc.field(check=check_ident)


class GetItem(Expr):
    obj: Expr
    idx: Expr


class BinOp(lang.ValueEnum):
    ADD = '+'
    SUB = '-'
    MUL = '*'
    DIV = '/'


class BinExpr(Expr):
    left: Expr
    op: str = dc.field(check=bool)
    right: Expr


class CmpOp(lang.ValueEnum):
    EQ = '=='
    NE = '!='
    GT = '>'
    GE = '>='
    LT = '<'
    LE = '<='

    IS = 'is'
    IS_NOT = 'is_not'

    IN = 'in'
    NOT_IN = 'not_in'


class CmpExpr(Expr):
    left: Expr
    op: str = dc.field(check=bool)
    right: Expr


class UnaryOp(lang.ValueEnum):
    NOT = 'not'


class UnaryExpr(Expr):
    op: str = dc.field(check=bool)
    value: Expr


class Keyword(Node):
    name: ta.Optional[Ident]
    value: Expr


class Call(Expr):
    fn: Expr
    args: ta.Sequence[Expr]
    keywords: ta.Sequence[Keyword] = ()


class Starred(Expr):
    value: Expr
