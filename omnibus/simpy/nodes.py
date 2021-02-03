import typing as ta

from .. import check
from .. import dataclasses as dc
from .. import lang
from .. import nodal


Exprs = ta.Sequence['Expr']
Stmts = ta.Sequence['Stmt']
Defs = ta.Sequence['Def']
Ident = str


def check_ident(i: Ident) -> Ident:
    return check.non_empty_str(i)


class Annotation(nodal.Annotation):
    pass


class Node(nodal.Nodal['Node', Annotation]):
    pass


class Expr(Node, abstract=True):
    pass


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


class Kwarg(Node):
    name: ta.Optional[Ident]
    value: Expr


class Call(Expr):
    fn: Expr
    args: Exprs
    kwargs: ta.Sequence[Kwarg] = ()


class Star(Expr):
    value: Expr


class Stmt(Node, abstract=True):
    pass


class ExprStmt(Stmt):
    expr: Expr


class SetVar(Stmt):
    name: Ident = dc.field(check=check_ident)
    expr: Expr


class SetAttr(Stmt):
    obj: Expr
    attr: Ident = dc.field(check=check_ident)
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
    var: Ident = dc.field(check=check_ident)
    iter: Expr
    body: Stmts


class Break(Stmt):
    pass


class Continue(Stmt):
    pass


class Pass(Stmt):
    pass


class Def(Node, abstract=True):
    pass


class Arg(Node):
    name: Ident = dc.field(check=check_ident)
    default: ta.Optional[Expr] = None


class Args(Node):
    args: ta.Sequence[Arg] = ()
    vararg: ta.Optional[Arg] = None
    kwarg: ta.Optional[Arg] = None


class Fn(Def):
    name: Ident = dc.field(check=check_ident)
    args: Args
    body: Stmts


class Module(Node):
    defs: Defs
