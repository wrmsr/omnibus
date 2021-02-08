import ast
import typing as ta

from . import nodes as no
from .. import check
from .. import dispatch


AstT = ta.TypeVar('AstT', bound=ast.AST)


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

    def translate(self, an: ast.Constant) -> no.Node:  # noqa
        _check_ast_fields(an, ['value', 'kind'])
        return no.Constant(an.value, an.kind)

    def translate(self, an: ast.Expr) -> no.Node:  # noqa
        _check_ast_fields(an, ['value'])
        return no.ExprStmt(self.translate(an.value))

    def translate(self, an: ast.Module) -> no.Node:  # noqa
        _check_ast_fields(an, ['body'])
        return no.Module([self.translate(c) for c in an.body])


def translate(an: ast.AST) -> no.Node:
    return Translator().translate(an)
