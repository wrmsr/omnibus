import typing as ta

from ... import nodal


Nodes = ta.Sequence['Node']
Stmts = ta.Sequence['Stmt']
Exprs = ta.Sequence['Expr']


class Annotation(nodal.Annotation):
    pass


class Node(nodal.Nodal['Node', Annotation], sealed='package'):
    pass


class Stmt(Node, abstract=True):
    pass


class ExprStmt(Stmt):
    expr: 'Expr'


class Expr(Node, abstract=True):
    pass
