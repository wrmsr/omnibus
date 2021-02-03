import ast
import typing as ta

from . import nodes as no
from .. import check
from .. import dataclasses as dc
from .. import dispatch


AstT = ta.TypeVar('AstT', bound=ast.AST)


def _get_ast_bin_op(an: ast.AST) -> no.BinOp:
    if isinstance(an, ast.Add):
        return no.BinOps.ADD
    elif isinstance(an, ast.Sub):
        return no.BinOps.SUB
    elif isinstance(an, ast.Mult):
        return no.BinOps.MUL
    elif isinstance(an, ast.Div):
        return no.BinOps.DIV
    else:
        raise TypeError(an)


def _get_ast_cmp_op(an: ast.AST) -> no.CmpOp:
    if isinstance(an, ast.Eq):
        return no.CmpOps.EQ
    elif isinstance(an, ast.NotEq):
        return no.CmpOps.NE
    elif isinstance(an, ast.Gt):
        return no.CmpOps.GT
    elif isinstance(an, ast.GtE):
        return no.CmpOps.GE
    elif isinstance(an, ast.Lt):
        return no.CmpOps.LT
    elif isinstance(an, ast.LtE):
        return no.CmpOps.LE
    elif isinstance(an, ast.Is):
        return no.CmpOps.IS
    elif isinstance(an, ast.IsNot):
        return no.CmpOps.IS_NOT
    elif isinstance(an, ast.In):
        return no.CmpOps.IN
    elif isinstance(an, ast.NotIn):
        return no.CmpOps.NOT_IN
    else:
        raise TypeError(an)


def _get_ast_unary_op(an: ast.AST) -> no.UnaryOp:
    if isinstance(an, ast.Not):
        return no.UnaryOps.NOT
    else:
        raise TypeError(an)


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

    def _get_name_id(self, an: ast.AST, ctx: ta.Type[ast.expr_context]) -> str:
        check.isinstance(an, ast.Name)
        _check_ast_fields(an, ['id', 'ctx'])
        check.isinstance(an.ctx, ctx)
        return an.id

    def _get_attribute_fields(self, an: ast.AST, ctx: ta.Type[ast.expr_context]) -> ta.Tuple[ast.AST, str]:
        check.isinstance(an, ast.Attribute)
        _check_ast_fields(an, ['value', 'attr', 'ctx'])
        check.isinstance(an.ctx, ctx)
        return an.value, an.attr

    def translate(self, an: ast.arg) -> no.Node:  # noqa
        _check_ast_fields(an, ['arg'])
        return no.Arg(no.Ident(an.arg))

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

    def translate(self, an: ast.Assign) -> no.Node:  # noqa
        _check_ast_fields(an, ['targets', 'value'])
        t = check.single(an.targets)
        if isinstance(t, ast.Name):
            return no.SetVar(
                no.Ident(self._get_name_id(t, ast.Store)),
                self.translate(an.value),
            )
        elif isinstance(t, ast.Attribute):
            obj, att = self._get_attribute_fields(t, ast.Store)
            return no.SetAttr(
                self.translate(obj),
                no.Ident(att),
                self.translate(an.value),
            )
        else:
            raise TypeError(t)

    def translate(self, an: ast.Attribute) -> no.Node:  # noqa
        obj, att = self._get_attribute_fields(an, ast.Load)
        return no.GetAttr(self.translate(obj), no.Ident(att))

    def translate(self, an: ast.BinOp) -> no.Node:  # noqa
        _check_ast_fields(an, ['left', 'op', 'right'])
        return no.BinExpr(
            self.translate(an.left),
            _get_ast_bin_op(an.op),
            self.translate(an.right),
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

    def translate(self, an: ast.Compare) -> no.Node:  # noqa
        _check_ast_fields(an, ['left', 'ops', 'comparators'])
        op = check.single(an.ops)
        right = check.single(an.comparators)
        return no.CmpExpr(
            self.translate(an.left),
            _get_ast_cmp_op(op),
            self.translate(right),
        )

    def translate(self, an: ast.Constant) -> no.Node:  # noqa
        _check_ast_fields(an, ['value', 'kind'])
        return no.Const(an.value)

    def translate(self, an: ast.Continue) -> no.Node:  # noqa
        _check_ast_fields(an, [])
        return no.Continue()

    def translate(self, an: ast.Expr) -> no.Node:  # noqa
        _check_ast_fields(an, ['value'])
        return no.ExprStmt(self.translate(an.value))

    def translate(self, an: ast.For) -> no.Node:  # noqa
        _check_ast_fields(an, ['target', 'iter', 'body'])
        return no.ForIter(
            no.Ident(self._get_name_id(an.target, ast.Store)),
            self.translate(an.iter),
            [self.translate(e) for e in an.body]
        )

    def translate(self, an: ast.FunctionDef) -> no.Node:  # noqa
        _check_ast_fields(an, ['name', 'args', 'body'])
        return no.Fn(
            name=no.Ident(an.name),
            args=self.translate(an.args),
            body=[self.translate(b) for b in an.body],
        )

    def translate(self, an: ast.If) -> no.Node:  # noqa
        _check_ast_fields(an, ['test', 'body', 'orelse'])
        return no.If(
            self.translate(an.test),
            [self.translate(e) for e in an.body],
            [self.translate(e) for e in an.orelse] if an.orelse else None,
        )

    def translate(self, an: ast.keyword) -> no.Node:  # noqa
        _check_ast_fields(an, ['arg', 'value'])
        return no.Keyword(
            no.Ident(an.arg) if an.arg is not None else None,
            self.translate(an.value),
        )

    def translate(self, an: ast.Module) -> no.Node:  # noqa
        _check_ast_fields(an, ['body'])
        return no.Module([self.translate(c) for c in an.body])

    def translate(self, an: ast.Name) -> no.Node:  # noqa
        return no.GetVar(no.Ident(self._get_name_id(an, ast.Load)))

    def translate(self, an: ast.NameConstant) -> no.Node:  # noqa
        _check_ast_fields(an, ['value'])
        return no.Const(an.value)

    def translate(self, an: ast.Num) -> no.Node:  # noqa
        _check_ast_fields(an, ['n'])
        return no.Const(an.n)

    def translate(self, an: ast.Pass) -> no.Node:  # noqa
        _check_ast_fields(an, [])
        return no.Pass()

    def translate(self, an: ast.Raise) -> no.Node:  # noqa
        _check_ast_fields(an, ['exc'])
        return no.Raise(self.translate(check.not_none(an.exc)))

    def translate(self, an: ast.Return) -> no.Node:  # noqa
        _check_ast_fields(an, ['value'])
        return no.Return(self.translate(an.value) if an.value is not None else None)

    def translate(self, an: ast.Starred) -> no.Node:  # noqa
        _check_ast_fields(an, ['value', 'ctx'])
        check.isinstance(an.ctx, ast.Load)
        return no.Starred(self.translate(an.value))

    def translate(self, an: ast.Str) -> no.Node:  # noqa
        _check_ast_fields(an, ['s'])
        return no.Const(an.s)

    def translate(self, an: ast.Subscript) -> no.Node:  # noqa
        _check_ast_fields(an, ['value', 'slice', 'ctx'])
        check.isinstance(an.ctx, ast.Load)
        return no.GetItem(
            self.translate(an.value),
            self.translate(an.slice),
        )

    def translate(self, an: ast.UnaryOp) -> no.Node:  # noqa
        _check_ast_fields(an, ['op', 'operand'])
        return no.UnaryExpr(
            _get_ast_unary_op(an.op),
            self.translate(an.operand),
        )


def translate(an: ast.AST) -> no.Node:
    return Translator().translate(an)
