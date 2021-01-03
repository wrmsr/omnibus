"""
https://github.com/python/cpython/blob/c73914a562580ae72048876cb42ed8e76e2c83f9/Lib/ast.py#L651
"""
import ast  # noqa
import enum
import typing as ta

from .. import dataclasses as dc
from .. import lang
from .. import nodal


Strs = ta.Sequence[str]
Nodes = ta.Sequence['Node']
Stmts = ta.Sequence['Stmt']
Exprs = ta.Sequence['Expr']


class BinOp(enum.Enum):
    ADD = '+'
    BIT_AND = '&'
    BIT_OR = '|'
    BIT_XOR = '^'
    DIV = '/'
    FLOOR_DIV = '//'
    L_SHIFT = '<<'
    MAT_MULT = '*'
    MOD = '%'
    MULT = '*'
    POW = '**'
    R_SHIFT = '>>'
    SUB = '-'


class BoolOp(enum.Enum):
    AND = 'and'
    OR = 'or'


class CmpOp(enum.Enum):
    EQ = '=='
    GT = '>'
    GTE = '>='
    IN = 'in'
    IS = 'is'
    IS_NOT = 'is not'
    LT = '<'
    LTE = '<='
    NOT_EQ = '!='
    NOT_IN = 'not in'


class Context(lang.AutoEnum):
    AUG_LOAD = ...
    AUG_STORE = ...
    DEL = ...
    LOAD = ...
    PARAM = ...
    STORE = ...


class UnaryOp(enum.Enum):
    INVERT = '~'
    NOT = 'not'
    ADD = '+'
    SUB = '-'


class FormatConversion(lang.ValueEnum):
    NONE = 0
    STR = 1
    REPR = 2
    ASCII = 3


class Annotation(nodal.Annotation):
    pass


class Node(nodal.Nodal['Node', Annotation], repr=False, sealed='package'):
    pass


class Stmt(Node, abstract=True):
    pass


class ExprStmt(Stmt):
    expr: 'Expr'


class Expr(Node, abstract=True):
    pass


class Annotated(dc.Data, frozen=True, abstract=True, sealed=True, reorder=True):
    annotation: ta.Optional[Expr] = None


class TypeCommented(dc.Data, frozen=True, abstract=True, sealed=True, reorder=True):
    type_comment: ta.Optional[str] = None


class Arg(Node, Annotated, TypeCommented):
    name: str


class Args(Node):
    args: ta.Sequence[Arg] = ()
    vararg: ta.Optional[Arg] = None
    kw_only_args: ta.Sequence[Arg] = ()
    kw_defaults: Exprs = ()
    kwarg: ta.Optional[Arg] = None
    defaults: Exprs = ()


class Comp(Node):
    target: 'Expr'
    iter: 'Expr'
    ifs: ta.Optional[Exprs] = None
    is_async: bool = False


class ExceptHandler(Node):
    type: Expr
    name: str
    body: Stmts


class WithItem(Node):
    value: Expr
    name: ta.Optional[str] = None


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


class AsyncWith(Stmt, TypeCommented):
    items: ta.Sequence[WithItem]
    body: Stmts


class AugAssign(Stmt):
    target: Expr
    op: BinOp
    value: Expr


class Break(Stmt):
    pass


class Kwarg(Node):
    name: str
    value: Expr


class ClassDef(Stmt):
    name: str
    bases: Exprs
    body: Stmts
    kwargs: ta.Sequence[Kwarg] = ()
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


class Attribute(Expr):
    value: Expr
    attr: str


class Await(Expr):
    value: Expr


class BinExpr(Expr):
    left: Expr
    op: BinOp
    right: Expr


class BoolExpr(Expr):
    op: BoolOp
    values: Expr


class Bytes(Expr):
    value: str


class Call(Expr):
    func: Expr
    args: Exprs = ()
    kwargs: ta.Sequence[Kwarg] = ()


class Compare(Expr):
    left: Expr
    cmps: ta.Sequence[ta.Tuple[CmpOp, Expr]]


class Constant(Expr):
    value: ta.Any
    kind: ta.Any = None


class Dict(Expr):
    items: ta.Union[ta.Tuple[str, Expr], Expr]


class DictComp(Expr):
    key: Expr
    value: Expr
    comps: ta.Sequence[Comp]


class FormattedValue(Expr):
    value: Expr
    conversion: int
    spec: ta.Optional[str] = None


class GeneratorExp(Expr):
    value: Expr
    comps: ta.Sequence[Comp]


class IfExp(Expr):
    test: Expr
    body: Expr
    or_else: Expr


class JoinedStr(Expr):
    values: Exprs


class Lambda(Expr):
    args: Args
    body: Expr


class List(Expr):
    items: Exprs


class ListComp(Expr):
    value: Expr
    comps: ta.Sequence[Comp]


class Name(Expr):
    name: str


class NamedExpr(Expr):
    target: Name
    value: Expr


class Set(Expr):
    items: Exprs


class SetComp(Expr):
    value: Expr
    comps: ta.Sequence[Comp]


class Starred(Expr):
    value: Expr


class Subscript(Expr):
    value: Expr
    slice: Expr


class Tuple(Expr):
    items: Exprs


class UnaryExpr(Expr):
    op: UnaryOp
    value: Expr


class Yield(Expr):
    value: Expr


class YieldFrom(Expr):
    value: Expr
