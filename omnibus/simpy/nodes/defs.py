import typing as ta

from ... import dataclasses as dc
from .base import check_ident
from .base import Def
from .base import Expr
from .base import Ident
from .base import Node
from .base import Stmt


class Arg(Node):
    name: Ident = dc.field(check=check_ident)
    default: ta.Optional[Expr] = None


class Args(Node):
    args: ta.Sequence[Arg] = ()
    vararg: ta.Optional[Arg] = None
    kwonly_args: ta.Sequence[Arg] = ()
    kwarg: ta.Optional[Arg] = None


class Fn(Def):
    name: Ident = dc.field(check=check_ident)
    args: Args
    body: ta.Sequence[Stmt]
