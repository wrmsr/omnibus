import typing as ta

from .. import dataclasses as dc
from .. import lang
from .. import nodal


Exprs = ta.Sequence['Expr']
Stmts = ta.Sequence['Stmt']
Defs = ta.Sequence['Def']


class Annotation(nodal.Annotation):
    pass


class Node(nodal.Nodal['Node', Annotation]):
    pass


class Expr(Node, abstract=True):
    pass


class Const(Expr):
    value: ta.Any


class GetVar(Expr):
    name: str


class GetAttr(Expr):
    obj: Expr
    attr: str


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
    op: str
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
    op: str
    right: Expr


class UnaryOp(lang.ValueEnum):
    NOT = 'not'


class UnaryExpr(Expr):
    op: str
    value: Expr


class Call(Expr):
    fn: Expr
    args: Exprs


class Stmt(Node, abstract=True):
    pass


class ExprStmt(Stmt):
    expr: Expr


class SetVar(Stmt):
    name: str
    expr: Expr


class SetAttr(Stmt):
    obj: Expr
    attr: str
    value: Expr


class SetItem(Stmt):
    obj: Expr
    idx: Expr
    value: Expr


class Raise(Stmt):
    exc: Expr


class Return(Stmt):
    value: ta.Optional[Expr]


class If(Stmt):
    test: Expr
    then: Stmts
    else_: ta.Optional[Stmts] = dc.field(check=lambda l: l is None or l)


class ForLoop(Stmt):
    var: str
    iter: Expr
    body: Stmts


class Break(Stmt):
    pass


class Continue(Stmt):
    pass


class Def(Node, abstract=True):
    pass


class Fn(Def):
    name: str
    params: ta.Sequence[str] = dc.field(check=lambda s: not isinstance(s, str) and all(e and isinstance(e, str) for e in s))  # noqa
    body: Stmts


class Module(Node):
    defs: Defs
