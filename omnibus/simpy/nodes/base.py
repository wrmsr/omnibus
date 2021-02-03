import typing as ta

from ... import check
from ... import nodal


Ident = str


def check_ident(i: Ident) -> Ident:
    return check.non_empty_str(i)


class Annotation(nodal.Annotation):
    pass


class Node(nodal.Nodal['Node', Annotation]):
    pass


class Expr(Node, abstract=True):
    pass


class Stmt(Node, abstract=True):
    pass


class Def(Node, abstract=True):
    pass


class Module(Node):
    defs: ta.Sequence[Def]
