import ast
import typing as ta

from . import nodes as no
from .. import check
from .. import dispatch


AstT = ta.TypeVar('AstT', bound=ast.AST)


def _get_ast_bin_op(an: ast.AST) -> str:
    if isinstance(an, ast.Add):
        return no.BinOp.ADD
    elif isinstance(an, ast.Sub):
        return no.BinOp.SUB
    elif isinstance(an, ast.Mult):
        return no.BinOp.MUL
    elif isinstance(an, ast.Div):
        return no.BinOp.DIV
    else:
        raise TypeError(an)


def _get_ast_cmp_op(an: ast.AST) -> str:
    if isinstance(an, ast.Eq):
        return no.CmpOp.EQ
    elif isinstance(an, ast.NotEq):
        return no.CmpOp.NE
    elif isinstance(an, ast.Gt):
        return no.CmpOp.GT
    elif isinstance(an, ast.GtE):
        return no.CmpOp.GE
    elif isinstance(an, ast.Lt):
        return no.CmpOp.LT
    elif isinstance(an, ast.LtE):
        return no.CmpOp.LE
    elif isinstance(an, ast.Is):
        return no.CmpOp.IS
    elif isinstance(an, ast.IsNot):
        return no.CmpOp.IS_NOT
    elif isinstance(an, ast.In):
        return no.CmpOp.IN
    elif isinstance(an, ast.NotIn):
        return no.CmpOp.NOT_IN
    else:
        raise TypeError(an)


def _get_ast_unary_op(an: ast.AST) -> str:
    if isinstance(an, ast.Not):
        return no.UnaryOp.NOT
    else:
        raise TypeError(an)


def _check_ast_fields(an: AstT, fields: ta.Iterable[str]) -> AstT:
    for f in set(type(an)._fields) - set(check.not_isinstance(fields, str)):  # noqa
        v = getattr(an, f)
        if v is not None and not (isinstance(v, ta.Iterable) and not v):
            raise ValueError(f'Node {an!r} has unhandled field {f!r} of value {v!r}')
    return an


class Translator(dispatch.Class):
    __call__ = dispatch.property()

    def __call__(self, an: ast.AST) -> no.Node:  # noqa
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

    def __call__(self, an: ast.Assign) -> no.Node:  # noqa
        _check_ast_fields(an, ['targets', 'value'])
        t = check.single(an.targets)
        if isinstance(t, ast.Name):
            return no.SetVar(
                self._get_name_id(t, ast.Store),
                self(an.value),
            )
        elif isinstance(t, ast.Attribute):
            obj, att = self._get_attribute_fields(t, ast.Store)
            return no.SetAttr(
                self(obj),
                att,
                self(an.value),
            )
        else:
            raise TypeError(t)

    def __call__(self, an: ast.Attribute) -> no.Node:  # noqa
        obj, att = self._get_attribute_fields(an, ast.Load)
        return no.GetAttr(self(obj), att)

    def __call__(self, an: ast.BinOp) -> no.Node:  # noqa
        _check_ast_fields(an, ['left', 'op', 'right'])
        return no.BinExpr(
            self(an.left),
            _get_ast_bin_op(an.op),
            self(an.right),
        )

    def __call__(self, an: ast.Break) -> no.Node:  # noqa
        _check_ast_fields(an, [])
        return no.Break()

    def __call__(self, an: ast.Call) -> no.Node:  # noqa
        _check_ast_fields(an, ['func', 'args'])
        return no.Call(
            self(an.func),
            [self(a) for a in an.args],
        )

    def __call__(self, an: ast.Compare) -> no.Node:  # noqa
        _check_ast_fields(an, ['left', 'ops', 'comparators'])
        op = check.single(an.ops)
        right = check.single(an.comparators)
        return no.CmpExpr(
            self(an.left),
            _get_ast_cmp_op(op),
            self(right),
        )

    def __call__(self, an: ast.Constant) -> no.Node:  # noqa
        _check_ast_fields(an, ['value', 'kind'])
        return no.Const(an.value)

    def __call__(self, an: ast.Continue) -> no.Node:  # noqa
        _check_ast_fields(an, [])
        return no.Continue()

    def __call__(self, an: ast.Expr) -> no.Node:  # noqa
        _check_ast_fields(an, ['value'])
        return no.ExprStmt(self(an.value))

    def __call__(self, an: ast.For) -> no.Node:  # noqa
        _check_ast_fields(an, ['target', 'iter', 'body'])
        return no.ForLoop(
            self._get_name_id(an.target, ast.Store),
            self(an.iter),
            [self(e) for e in an.body]
        )

    def __call__(self, an: ast.FunctionDef) -> no.Node:  # noqa
        _check_ast_fields(an, ['name', 'args', 'body'])
        return no.Fn(
            an.name,
            [_check_ast_fields(a, ['arg']).arg for a in an.args.args],
            [self(b) for b in an.body],
        )

    def __call__(self, an: ast.If) -> no.Node:  # noqa
        _check_ast_fields(an, ['test', 'body', 'orelse'])
        return no.If(
            self(an.test),
            [self(e) for e in an.body],
            [self(e) for e in an.orelse] if an.orelse else None,
        )

    def __call__(self, an: ast.Module) -> no.Node:  # noqa
        _check_ast_fields(an, ['body'])
        return no.Module([self(c) for c in an.body])

    def __call__(self, an: ast.Name) -> no.Node:  # noqa
        return no.GetVar(self._get_name_id(an, ast.Load))

    def __call__(self, an: ast.NameConstant) -> no.Node:  # noqa
        _check_ast_fields(an, ['value'])
        return no.Const(an.value)

    def __call__(self, an: ast.Num) -> no.Node:  # noqa
        _check_ast_fields(an, ['n'])
        return no.Const(an.n)

    def __call__(self, an: ast.Raise) -> no.Node:  # noqa
        _check_ast_fields(an, ['exc'])
        return no.Raise(self(check.not_none(an.exc)))

    def __call__(self, an: ast.Return) -> no.Node:  # noqa
        _check_ast_fields(an, ['value'])
        return no.Return(self(an.value) if an.value is not None else None)

    def __call__(self, an: ast.Str) -> no.Node:  # noqa
        _check_ast_fields(an, ['s'])
        return no.Const(an.s)

    def __call__(self, an: ast.Subscript) -> no.Node:  # noqa
        _check_ast_fields(an, ['value', 'slice', 'ctx'])
        check.isinstance(an.ctx, ast.Load)
        return no.GetItem(
            self(an.value),
            self(an.slice),
        )

    def __call__(self, an: ast.UnaryOp) -> no.Node:  # noqa
        _check_ast_fields(an, ['op', 'operand'])
        return no.UnaryExpr(
            _get_ast_unary_op(an.op),
            self(an.operand),
        )


def translate(an: ast.AST) -> no.Node:
    return Translator()(an)
