import typing as ta

from ... import dataclasses as dc
from ... import nodal


Nodes = ta.Sequence['Node']
Decls = ta.Sequence['Decl']
Stmts = ta.Sequence['Stmt']
Exprs = ta.Sequence['Expr']


class Annotation(nodal.Annotation):
    pass


class Node(nodal.Nodal['Node', Annotation], sealed='package'):
    pass


class Ident(Node):
    s: str = dc.field(check_type=str)


class Decl(Node, abstract=True):
    pass


class Stmt(Node, abstract=True):
    pass


class ExprStmt(Stmt):
    expr: 'Expr'


class Expr(Node, abstract=True):
    pass
