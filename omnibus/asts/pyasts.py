"""
AST
  comprehension
  excepthandler
    ExceptHandler
  keyword
  mod
    Expression
    FunctionType
    Interactive
    Module
    Suite
  slice
    ExtSlice
    Index
    Slice
  type_ignore
    TypeIgnore
  withitem
"""
import ast
import typing as ta

from . import nodes as no
from .. import check
from .. import dataclasses as dc
from .. import dispatch


AstT = ta.TypeVar('AstT', bound=ast.AST)


_BIN_OP_MAP: ta.Mapping[ta.Type[ast.AST], no.BinOp] = {
    ast.Add: no.BinOps.ADD,
    ast.Sub: no.BinOps.SUB,
    ast.Mult: no.BinOps.MUL,
    ast.Div: no.BinOps.DIV,
    ast.Mod: no.BinOps.MOD,

    ast.BitAnd: no.BinOps.BIT_AND,
    ast.BitOr: no.BinOps.BIT_OR,
    ast.BitXor: no.BinOps.BIT_XOR,

    ast.LShift: no.BinOps.LSH,
    ast.RShift: no.BinOps.RSH,
}


def _get_ast_bin_op(an: ast.AST) -> no.BinOp:
    return _BIN_OP_MAP[type(an)]


_BOOL_OP_MAP: ta.Mapping[ta.Type[ast.AST], no.BoolOp] = {
    ast.And: no.BoolOps.AND,
    ast.Or: no.BoolOps.OR,
}


def _get_ast_bool_op(an: ast.AST) -> no.BoolOp:
    return _BOOL_OP_MAP[type(an)]


_CMP_OP_MAP: ta.Mapping[ta.Type[ast.AST], no.CmpOp] = {
    ast.Eq: no.CmpOps.EQ,
    ast.NotEq: no.CmpOps.NE,
    ast.Gt: no.CmpOps.GT,
    ast.GtE: no.CmpOps.GE,
    ast.Lt: no.CmpOps.LT,
    ast.LtE: no.CmpOps.LE,

    ast.Is: no.CmpOps.IS,
    ast.IsNot: no.CmpOps.IS_NOT,

    ast.In: no.CmpOps.IN,
    ast.NotIn: no.CmpOps.NOT_IN,
}


def _get_ast_cmp_op(an: ast.AST) -> no.CmpOp:
    return _CMP_OP_MAP[type(an)]


_UNARY_OP_MAP: ta.Mapping[ta.Type[ast.AST], no.UnaryOp] = {
    ast.Invert: no.UnaryOps.INVERT,

    ast.Not: no.UnaryOps.NOT,
}


def _get_ast_unary_op(an: ast.AST) -> no.UnaryOp:
    return _UNARY_OP_MAP[type(an)]


def _check_ast_fields(an: AstT, fields: ta.Iterable[str]) -> AstT:
    for f in set(type(an)._fields) - set(check.not_isinstance(fields, str)):  # noqa
        v = getattr(an, f)
        if v is not None and not (isinstance(v, ta.Iterable) and not v):
            raise ValueError(f'Node {an!r} has unhandled field {f!r} of value {v!r}')
    return an


class Translator(dispatch.Class):
    translate = dispatch.property()

    def translate(self, an: ast.AST) -> no.Node:  # noqa
        raise TypeError(an)

    def translate(self, an: ast.Module) -> no.Node:  # noqa
        _check_ast_fields(an, ['body'])
        return no.Module([self.translate(c) for c in an.body])

    def translate(self, an: ast.AnnAssign) -> no.Node:  # noqa
        _check_ast_fields(an, [])
        return no.AnnAssign()

    def translate(self, an: ast.alias) -> no.Node:  # noqa
        _check_ast_fields(an, ['name', 'asname'])
        return no.Alias(an.name, an.asname)

    def translate(self, an: ast.arg) -> no.Node:  # noqa
        _check_ast_fields(an, ['arg', 'annotation'])
        return no.Arg(
            no.Ident(an.arg),
            annotation=self.translate(an.annotation) if an.annotation is not None else None,
        )

    def translate(self, an: ast.arguments) -> no.Node:  # noqa
        _check_ast_fields(an, ['args', 'vararg', 'kwonlyargs', 'kw_defaults', 'kwarg', 'defaults'])

        def zip_defaults(al, dl):
            return [(a, d) for a, d in zip(al, ([None] * (len(al) - len(dl or [])) + list(dl or [])))]

        def set_defaults(al, dl):
            return [
                dc.replace(
                    check.isinstance(self.translate(a), no.Arg),
                    default=self.translate(d) if d is not None else None,
                )
                for a, d in zip_defaults(al, dl)
            ]

        return no.Args(
            set_defaults(an.args, an.defaults),
            self.translate(an.vararg) if an.vararg is not None else None,
            set_defaults(an.kwonlyargs, an.kw_defaults),
            self.translate(an.kwarg) if an.vararg is not None else None,
        )

    def translate(self, an: ast.Assert) -> no.Node:  # noqa
        _check_ast_fields(an, [])
        return no.Assert()

    def translate(self, an: ast.Assign) -> no.Node:  # noqa
        _check_ast_fields(an, ['targets', 'value'])
        return no.Assign(
            targets=[self.translate(e) for e in an.targets],
            value=self.translate(an.value),
        )

    def translate(self, an: ast.AsyncFor) -> no.Node:  # noqa
        _check_ast_fields(an, [])
        return no.AsyncFor()

    def translate(self, an: ast.AsyncFunctionDef) -> no.Node:  # noqa
        _check_ast_fields(an, [])
        return no.AsyncFunctionDef()

    def translate(self, an: ast.AsyncWith) -> no.Node:  # noqa
        _check_ast_fields(an, [])
        return no.AsyncWith()

    def translate(self, an: ast.Attribute) -> no.Node:  # noqa
        _check_ast_fields(an, ['value', 'attr', 'ctx'])
        return no.Attribute(
            value=self.translate(an.value),
            attr=an.attr,
        )

    def translate(self, an: ast.AugAssign) -> no.Node:  # noqa
        _check_ast_fields(an, [])
        return no.AugAssign()

    def translate(self, an: ast.Await) -> no.Node:  # noqa
        _check_ast_fields(an, [])
        return no.Await()

    def translate(self, an: ast.BinOp) -> no.Node:  # noqa
        _check_ast_fields(an, ['left', 'op', 'right'])
        return no.BinExpr(
            self.translate(an.left),
            _get_ast_bin_op(an.op),
            self.translate(an.right),
        )

    def translate(self, an: ast.BoolOp) -> no.Node:  # noqa
        _check_ast_fields(an, ['op', 'values'])
        left, right = an.values
        return no.BoolExpr(
            self.translate(left),
            _get_ast_bool_op(an.op),
            self.translate(right),
        )

    def translate(self, an: ast.Break) -> no.Node:  # noqa
        _check_ast_fields(an, [])
        return no.Break()

    def translate(self, an: ast.Call) -> no.Node:  # noqa
        _check_ast_fields(an, ['func', 'args', 'keywords'])
        return no.Call(
            self.translate(an.func),
            [self.translate(a) for a in an.args],
            [self.translate(k) for k in (an.keywords or [])],
        )

    def translate(self, an: ast.ClassDef) -> no.Node:  # noqa
        _check_ast_fields(an, [])
        return no.ClassDef()

    def translate(self, an: ast.Compare) -> no.Node:  # noqa
        _check_ast_fields(an, [])
        return no.Compare()

    def translate(self, an: ast.Continue) -> no.Node:  # noqa
        _check_ast_fields(an, [])
        return no.Continue()

    def translate(self, an: ast.Constant) -> no.Node:  # noqa
        _check_ast_fields(an, ['value', 'kind'])
        return no.Constant(an.value, an.kind)

    def translate(self, an: ast.Delete) -> no.Node:  # noqa
        _check_ast_fields(an, [])
        return no.Delete()

    def translate(self, an: ast.Dict) -> no.Node:  # noqa
        _check_ast_fields(an, [])
        return no.Dict()

    def translate(self, an: ast.DictComp) -> no.Node:  # noqa
        _check_ast_fields(an, [])
        return no.DictComp()

    def translate(self, an: ast.Expr) -> no.Node:  # noqa
        _check_ast_fields(an, ['value'])
        return no.ExprStmt(self.translate(an.value))

    def translate(self, an: ast.For) -> no.Node:  # noqa
        _check_ast_fields(an, ['target', 'iter', 'body', 'orelse'])
        return no.For(
            target=self.translate(an.target),
            iter=self.translate(an.iter),
            body=[self.translate(b) for b in an.body],
            or_else=[self.translate(b) for b in an.orelse] if an.orelse is not None else an.orelse,
        )

    def translate(self, an: ast.FormattedValue) -> no.Node:  # noqa
        _check_ast_fields(an, [])
        return no.FormattedValue()

    def translate(self, an: ast.FunctionDef) -> no.Node:  # noqa
        _check_ast_fields(an, ['name', 'args', 'body', 'returns'])
        return no.FunctionDef(
            name=an.name,
            args=self.translate(an.args),
            body=[self.translate(b) for b in an.body],
            returns=self.translate(an.returns) if an.returns is not None else None,
        )

    def translate(self, an: ast.GeneratorExp) -> no.Node:  # noqa
        _check_ast_fields(an, [])
        return no.GeneratorExp()

    def translate(self, an: ast.Global) -> no.Node:  # noqa
        _check_ast_fields(an, [])
        return no.Global()

    def translate(self, an: ast.If) -> no.Node:  # noqa
        _check_ast_fields(an, [])
        return no.If()

    def translate(self, an: ast.IfExp) -> no.Node:  # noqa
        _check_ast_fields(an, [])
        return no.IfExp()

    def translate(self, an: ast.Import) -> no.Node:  # noqa
        _check_ast_fields(an, ['names'])
        return no.Import([self.translate(n) for n in an.names])

    def translate(self, an: ast.ImportFrom) -> no.Node:  # noqa
        _check_ast_fields(an, ['module', 'names', 'level'])
        return no.ImportFrom(an.module, [self.translate(n) for n in an.names], an.level)

    def translate(self, an: ast.JoinedStr) -> no.Node:  # noqa
        _check_ast_fields(an, [])
        return no.JoinedStr()

    def translate(self, an: ast.Lambda) -> no.Node:  # noqa
        _check_ast_fields(an, [])
        return no.Lambda()

    def translate(self, an: ast.List) -> no.Node:  # noqa
        _check_ast_fields(an, ['elts', 'ctx'])
        return no.List([self.translate(e) for e in an.elts])

    def translate(self, an: ast.ListComp) -> no.Node:  # noqa
        _check_ast_fields(an, [])
        return no.ListComp()

    def translate(self, an: ast.Name) -> no.Node:  # noqa
        _check_ast_fields(an, ['id', 'ctx'])
        return no.Name(an.id)

    def translate(self, an: ast.NamedExpr) -> no.Node:  # noqa
        _check_ast_fields(an, [])
        return no.NamedExpr()

    def translate(self, an: ast.Nonlocal) -> no.Node:  # noqa
        _check_ast_fields(an, [])
        return no.Nonlocal()

    def translate(self, an: ast.Pass) -> no.Node:  # noqa
        _check_ast_fields(an, [])
        return no.Pass()

    def translate(self, an: ast.Raise) -> no.Node:  # noqa
        _check_ast_fields(an, [])
        return no.Raise()

    def translate(self, an: ast.Return) -> no.Node:  # noqa
        _check_ast_fields(an, [])
        return no.Return()

    def translate(self, an: ast.Set) -> no.Node:  # noqa
        _check_ast_fields(an, [])
        return no.Set()

    def translate(self, an: ast.SetComp) -> no.Node:  # noqa
        _check_ast_fields(an, [])
        return no.SetComp()

    def translate(self, an: ast.Starred) -> no.Node:  # noqa
        _check_ast_fields(an, [])
        return no.Starred()

    def translate(self, an: ast.Subscript) -> no.Node:  # noqa
        _check_ast_fields(an, [])
        return no.Subscript()

    def translate(self, an: ast.Try) -> no.Node:  # noqa
        _check_ast_fields(an, [])
        return no.Try()

    def translate(self, an: ast.Tuple) -> no.Node:  # noqa
        _check_ast_fields(an, [])
        return no.Tuple()

    def translate(self, an: ast.UnaryOp) -> no.Node:  # noqa
        _check_ast_fields(an, [])
        return no.UnaryOp()

    def translate(self, an: ast.While) -> no.Node:  # noqa
        _check_ast_fields(an, [])
        return no.While()

    def translate(self, an: ast.With) -> no.Node:  # noqa
        _check_ast_fields(an, [])
        return no.With()

    def translate(self, an: ast.Yield) -> no.Node:  # noqa
        _check_ast_fields(an, [])
        return no.Yield()

    def translate(self, an: ast.YieldFrom) -> no.Node:  # noqa
        _check_ast_fields(an, [])
        return no.YieldFrom()


def translate(an: ast.AST) -> no.Node:
    return Translator().translate(an)
