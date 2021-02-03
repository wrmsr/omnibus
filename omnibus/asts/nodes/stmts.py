import ast  # noqa
import typing as ta

from .base import Annotated
from .base import Args
from .base import Expr
from .base import Exprs
from .base import Keyword
from .base import Node
from .base import Stmt
from .base import Stmts
from .base import Strs
from .base import TypeCommented
from .ops import BinOp


class AnnAssign(Stmt, Annotated):
    target: Expr
    value: Expr
    simple: bool


class Assert(Stmt):
    test: Expr
    msg: ta.Optional[Expr] = None


class Assign(Stmt, TypeCommented):
    targets: Exprs
    value: Expr


class AsyncFor(Stmt, TypeCommented):
    target: Expr
    iter: Expr
    body: Stmts
    or_else: Stmts = ()


class AsyncFunctionDef(Stmt, TypeCommented):
    name: str
    args: Args
    body: Stmts
    decorators: Exprs = ()
    returns: ta.Optional[Expr] = None


class WithItem(Node):
    value: Expr
    name: ta.Optional[str] = None


class AsyncWith(Stmt, TypeCommented):
    items: ta.Sequence[WithItem]
    body: Stmts


class AugAssign(Stmt):
    target: Expr
    op: BinOp
    value: Expr


class Body(Stmt):
    stmts: Stmts


class Break(Stmt):
    pass


class ClassDef(Stmt):
    name: str
    bases: Exprs
    body: Stmts
    keywords: ta.Sequence[Keyword] = ()
    decorators: Exprs = ()


class Continue(Stmt):
    pass


class Delete(Stmt):
    targets: Exprs


class For(Stmt, TypeCommented):
    target: Expr
    iter: Expr
    body: Stmts
    or_else: Stmts = ()


class FunctionDef(Stmt, TypeCommented):
    name: str
    args: Args
    body: Stmts
    decorators: Exprs = ()
    returns: ta.Optional[Expr] = None


class Global(Stmt):
    names: Strs


class If(Stmt):
    test: Expr
    body: Stmts
    or_else: Stmts = ()


class Import(Stmt):
    names: Strs


class ImportFrom(Stmt):
    module: str
    names: str
    level: ta.Optional[int] = None


class Nonlocal(Stmt):
    names: Strs


class Pass(Stmt):
    pass


class Raise(Stmt):
    exc: Expr
    cause: ta.Optional[Expr] = None


class Return(Stmt):
    value: ta.Optional[Expr] = None


class ExceptHandler(Node):
    type: Expr
    name: str
    body: Stmts


class Try(Stmt):
    body: Stmts
    handlers: ta.Sequence[ExceptHandler]
    or_elsek: Stmts = ()
    final_body: Stmts = ()


class While(Stmt):
    test: Expr
    body: Stmts
    or_else: Stmts = ()


class With(Stmt, TypeCommented):
    items: ta.Sequence[WithItem]
    body: Stmts
