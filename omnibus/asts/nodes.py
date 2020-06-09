"""
https://github.com/python/cpython/blob/c73914a562580ae72048876cb42ed8e76e2c83f9/Lib/ast.py#L651

class Comprehension(dc.Pure):

excepthandler(AST)
 ExceptHandler(excepthandler)

mod(AST)
 FunctionType(mod)
 Expr(mod)
 Suite(mod)
 Interactive(mod)
 Module(mod)

slice(AST)
 ExtSlice(slice)
 Index(slice)
 Slice(slice)

keyword(AST)

type_ignore(AST)
 TypeIgnore(type_ignore)

withitem(AST)
"""
import enum
import typing as ta

from .. import dataclasses as dc
from .. import lang


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


class Node(dc.Enum, abstract=True, sealed=True, reorder=True):
    pass


class Stmt(Node, abstract=True):
    pass


class ExprStmt(Stmt):
    expr: 'Expr'


class Expr(Node, abstract=True):
    pass


class TypeCommented(dc.Data, frozen=True, abstract=True, sealed=True, reorder=True):
    type_comment: ta.Optional[str] = None


class AnnAssign(Stmt):
    target: Expr
    annotation: ta.Optional[Expr]
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
    orelse: Stmts = ()


class AsyncFunctionDef(Stmt, TypeCommented):
    name: str
    # FIXME: args: Arguments
    body: Stmts
    decorators: Exprs = ()
    returns: ta.Optional[Expr] = None


class AsyncWith(Stmt, TypeCommented):
    # FIXME: items: ta.Sequence[WithItem]
    body: Stmts


class AugAssign(Stmt):
    target: Expr
    op: BinOp
    value: Expr


class Break(Stmt):
    pass


class ClassDef(Stmt):
    name: str
    bases: Exprs
    # FIXME: keywords: ta.Sequence[Keyword] = ()
    body: Stmts
    decorators: Exprs = ()


class Continue(Stmt):
    pass


class Delete(Stmt):
    targets: Exprs


class For(Stmt, TypeCommented):
    target: Expr
    iter: Expr
    body: Stmts
    orelse: Stmts = ()


class FunctionDef(Stmt, TypeCommented):
    name: str
    # FIXME: args: Arguments
    body: Stmts
    decorators: Exprs = ()
    returns: ta.Optional[Expr] = None


class Global(Stmt):
    names: ta.Sequence[str]


class If(Stmt):
    test: Expr
    body: Stmts
    orelse: Stmts = ()


class Import(Stmt):
    names: ta.Sequence[str]


class ImportFrom(Stmt):
    module: str
    names: str
    level: ta.Optional[int] = None


class Nonlocal(Stmt):
    names: ta.Sequence[str]


class Pass(Stmt):
    pass


class Raise(Stmt):
    exc: Expr
    cause: ta.Optional[Expr] = None


class Return(Stmt):
    value: ta.Optional[Expr] = None


class Try(Stmt):
    body: ta.Sequence[Stmt]
    # FIXME: handlers: ta.Sequence[ExceptHandler]
    orelse: Stmts = ()
    finalbody: Stmts = ()


class While(Stmt):
    test: Expr
    body: Stmts
    orelse: Stmts = ()


class With(Stmt, TypeCommented):
    items: Exprs
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
    pass


class Compare(Expr):
    pass


class Constant(Expr):
    pass


class Dict(Expr):
    pass


class DictComp(Expr):
    pass


class EllipsisExpr(Expr):
    pass


class FormattedValue(Expr):
    pass


class GeneratorExp(Expr):
    pass


class IfExp(Expr):
    pass


class JoinedStr(Expr):
    pass


class Lambda(Expr):
    pass


class List(Expr):
    pass


class ListComp(Expr):
    pass


class Name(Expr):
    pass


class NameConstant(Expr):
    pass


class NamedExpr(Expr):
    pass


class Num(Expr):
    pass


class Set(Expr):
    pass


class SetComp(Expr):
    pass


class Starred(Expr):
    pass


class Str(Expr):
    pass


class Subscript(Expr):
    pass


class Tuple(Expr):
    pass


class UnaryExpr(Expr):
    pass


class Yield(Expr):
    pass


class YieldFrom(Expr):
    pass
