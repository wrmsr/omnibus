import typing as ta

from ... import check
from ... import dataclasses as dc
from ... import nodal


class Annotation(nodal.Annotation):
    pass


class Node(nodal.Nodal['Node', Annotation]):
    pass


class Ident(Node):
    s: str = dc.field(check=check.non_empty_str)


class Expr(Node, abstract=True):
    pass


class Stmt(Node, abstract=True):
    pass


class Def(Node, abstract=True):
    pass


class Module(Node):
    defs: ta.Sequence[Def]
