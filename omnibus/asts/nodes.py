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

from .. import dataclasses as dc
from .. import lang


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


class Node(dc.Enum, abstract=True, sealed=True):
    pass


class Stmt(Node, abstract=True):
    pass


class ExprStmt(Stmt):
    expr: 'Expr'


class Expr(Node, abstract=True):
    pass


class AnnAssign(Stmt):
    pass


class Assert(Stmt):
    pass


class Assign(Stmt):
    pass


class AsyncFor(Stmt):
    pass


class AsyncFunctionDef(Stmt):
    pass


class AsyncWith(Stmt):
    pass


class AugAssign(Stmt):
    pass


class Break(Stmt):
    pass


class ClassDef(Stmt):
    pass


class Continue(Stmt):
    pass


class Delete(Stmt):
    pass


class For(Stmt):
    pass


class FunctionDef(Stmt):
    pass


class Global(Stmt):
    pass


class If(Stmt):
    pass


class Import(Stmt):
    pass


class ImportFrom(Stmt):
    pass


class Nonlocal(Stmt):
    pass


class Pass(Stmt):
    pass


class Raise(Stmt):
    pass


class Return(Stmt):
    pass


class Try(Stmt):
    pass


class While(Stmt):
    pass


class With(Stmt):
    pass


class Attribute(Expr):
    pass


class Await(Expr):
    pass


class BinExpr(Expr):
    pass


class BoolExpr(Expr):
    pass


class Bytes(Expr):
    pass


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
