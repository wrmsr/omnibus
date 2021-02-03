import typing as ta

from ... import dataclasses as dc
from .base import Expr
from .base import Ident
from .base import Node


class Const(Expr):
    value: ta.Any


class GetVar(Expr):
    name: Ident


class GetAttr(Expr):
    obj: Expr
    attr: Ident


class GetItem(Expr):
    obj: Expr
    idx: Expr


class Op(Node, abstract=True):
    glyph: str


class BinOp(dc.ValueEnum, Op):
    pass


class BinOps(BinOp.Values):
    ADD = BinOp('+')
    SUB = BinOp('-')
    MUL = BinOp('*')
    DIV = BinOp('/')


class BinExpr(Expr):
    left: Expr
    op: BinOp
    right: Expr


class CmpOp(dc.ValueEnum, Op):
    pass


class CmpOps(CmpOp.Values):
    EQ = CmpOp('==')
    NE = CmpOp('!=')
    GT = CmpOp('>')
    GE = CmpOp('>=')
    LT = CmpOp('<')
    LE = CmpOp('<=')

    IS = CmpOp('is')
    IS_NOT = CmpOp('is_not')

    IN = CmpOp('in')
    NOT_IN = CmpOp('not_in')


class CmpExpr(Expr):
    left: Expr
    op: CmpOp
    right: Expr


class UnaryOp(dc.ValueEnum, Op):
    pass


class UnaryOps(UnaryOp.Values):
    NOT = UnaryOp('not')


class UnaryExpr(Expr):
    op: UnaryOp
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
