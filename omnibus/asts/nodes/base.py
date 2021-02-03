"""
https://github.com/python/cpython/blob/c73914a562580ae72048876cb42ed8e76e2c83f9/Lib/ast.py#L651
"""
import ast  # noqa
import typing as ta

from ... import dataclasses as dc
from ... import nodal


Strs = ta.Sequence[str]
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


class Annotated(dc.Data, frozen=True, abstract=True, sealed='package', reorder=True):
    annotation: ta.Optional[Expr] = None


class TypeCommented(dc.Data, frozen=True, abstract=True, sealed='package', reorder=True):
    type_comment: ta.Optional[str] = None


class Arg(Node, Annotated, TypeCommented):
    name: str
    default: ta.Optional[Expr] = None


class Args(Node):
    args: ta.Sequence[Arg] = ()
    vararg: ta.Optional[Arg] = None
    kw_only_args: ta.Sequence[Arg] = ()
    kwarg: ta.Optional[Arg] = None


class Keyword(Node):
    name: ta.Optional[str]
    value: Expr
