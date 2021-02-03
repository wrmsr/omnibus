import typing as ta

from .base import Def
from .base import Expr
from .base import Ident
from .base import Node
from .base import Stmt


class Arg(Node):
    name: Ident
    default: ta.Optional[Expr] = None


class Args(Node):
    args: ta.Sequence[Arg] = ()
    vararg: ta.Optional[Arg] = None
    kwonly_args: ta.Sequence[Arg] = ()
    kwarg: ta.Optional[Arg] = None


class Fn(Def):
    name: Ident
    args: Args
    body: ta.Sequence[Stmt]
