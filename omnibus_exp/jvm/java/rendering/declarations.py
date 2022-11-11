import typing as ta

from .. import ast
from .base import BaseRenderer


T = ta.TypeVar('T')


class DeclarationRenderer(BaseRenderer):

    def render(self, node: ast.Declaration) -> None:  # noqa
        raise TypeError(node)

    def render(self, node: ast.AnnotatedDeclaration) -> None:  # noqa
        self.write('@')
        self.render(node.annotation)
        if node.args:
            self.write('(')
            self.render_operands(node.args)
            self.write(')')
        self.write('\n')
        self.render(node.declaration)

    def render(self, node: ast.Constructor) -> None:  # noqa
        raise TypeError(node)

    def render(self, node: ast.Field) -> None:  # noqa
        self.render_prefixes(node.access)
        self.render(node.type)
        self.write(f' {node.name}')
        self.write(';\n')

    def render(self, node: ast.Initialization) -> None:  # noqa
        raise TypeError(node)

    def render(self, node: ast.Method) -> None:  # noqa
        raise TypeError(node)

    def render(self, node: ast.RawDeclaration) -> None:  # noqa
        raise TypeError(node)

    def render(self, node: ast.TypeDeclaration) -> None:  # noqa
        raise TypeError(node)
