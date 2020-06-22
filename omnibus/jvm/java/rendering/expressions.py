import typing as ta

from .. import ast
from .base import BaseRenderer


T = ta.TypeVar('T')


class ExpressionRenderer(BaseRenderer):

    def render(self, node: ast.Expression) -> None:  # noqa
        raise TypeError(node)

    def render(self, node: ast.ArrayAccess) -> None:  # noqa
        self.render(node.array)
        self.write('[')
        self.render(node.index)
        self.write(']')

    def render(self, node: ast.Assignment) -> None:  # noqa
        self.render(node.left)
        self.write(' = ')
        self.render(node.right)

    def render(self, node: ast.BigArrayLiteral) -> None:  # noqa
        raise NotImplementedError

    def render(self, node: ast.BigStringLiteral) -> None:  # noqa
        raise NotImplementedError

    def render(self, node: ast.Binary) -> None:  # noqa
        self.render_params(node.left)
        self.write(' ')
        self.write(node.op)
        self.write(' ')
        self.render_params(node.right)

    def render(self, node: ast.Cast) -> None:  # noqa
        self.write('(')
        self.render(node.type)
        self.write(') ')
        self.render_params(node.value)

    def render(self, node: ast.Conditional) -> None:  # noqa
        self.render_params(node.condition)
        self.write(' ? ')
        self.render_params(node.if_true)
        self.write(' : ')
        self.render_params(node.if_false)

    def render(self, node: ast.Ident) -> None:  # noqa
        raise NotImplementedError

    def render(self, node: ast.Lambda) -> None:  # noqa
        raise NotImplementedError

    def render(self, node: ast.Literal) -> None:  # noqa
        self.write(repr(node.value))

    def render(self, node: ast.MemberAccess) -> None:  # noqa
        self.render(node.instance)
        self.write('.')
        self.write(node.member)

    def render(self, node: ast.MethodInvocation) -> None:  # noqa
        self.render(node.method)
        self.write('(')
        self.render_operands(node.args)
        self.write(')')

    def render(self, node: ast.MethodReference) -> None:  # noqa
        self.render(node.instance)
        self.write('::')
        self.write(node.method_name)

    def render(self, node: ast.New) -> None:  # noqa
        self.write('new ')
        self.render(node.type)
        self.write('(')
        self.render_operands(node.args)
        self.write(')')

    def render(self, node: ast.NewArray) -> None:  # noqa
        raise NotImplementedError

    def render(self, node: ast.RawExpression) -> None:  # noqa
        raise NotImplementedError

    def render(self, node: ast.Unary) -> None:  # noqa
        raise NotImplementedError
