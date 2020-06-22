import typing as ta

from .. import ast
from .base import BaseRenderer


T = ta.TypeVar('T')


class StatementRenderer(BaseRenderer):

    def render(self, node: ast.Statement) -> None:  # noqa
        raise TypeError(node)

    def render(self, node: ast.AnnotatedStatement) -> None:  # noqa
        self.write('@')
        self.render(node.annotation)
        if node.args:
            self.write('(')
            self.render_operands(node.args)
            self.write(')')
        self.write('\n')
        self.render(node.statement)

    def render(self, node: ast.Blank) -> None:  # noqa
        self.write('\n')

    def render(self, node: ast.Block) -> None:  # noqa
        self.write('{\n')
        for child in node.body:
            self.render(child)
        self.write('}')

    def render(self, node: ast.Break) -> None:  # noqa
        if node.label is not None:
            self.write(f'break {node.label};\n')
        else:
            self.write('break;\n')

    def render(self, node: ast.Case) -> None:  # noqa
        nl = False
        for obj in node.values:
            if nl:
                self.write('\n')
            else:
                nl = True
            self.write('case ')
            self.render_literal(obj)
            self.write(':')
        if node.is_default:
            if nl:
                self.write('\n')
            self.write('default:\n')
        self.render(node.block)

    def render(self, node: ast.Continue) -> None:  # noqa
        raise TypeError(node)

    def render(self, node: ast.DoWhile) -> None:  # noqa
        raise TypeError(node)

    def render(self, node: ast.Empty) -> None:  # noqa
        raise TypeError(node)

    def render(self, node: ast.ExpressionStatement) -> None:  # noqa
        raise TypeError(node)

    def render(self, node: ast.ForEach) -> None:  # noqa
        raise TypeError(node)

    def render(self, node: ast.If) -> None:  # noqa
        raise TypeError(node)

    def render(self, node: ast.Labeled) -> None:  # noqa
        raise TypeError(node)

    def render(self, node: ast.RawStatement) -> None:  # noqa
        raise TypeError(node)

    def render(self, node: ast.Return) -> None:  # noqa
        raise TypeError(node)

    def render(self, node: ast.Switch) -> None:  # noqa
        raise TypeError(node)

    def render(self, node: ast.Throw) -> None:  # noqa
        raise TypeError(node)

    def render(self, node: ast.Variable) -> None:  # noqa
        raise TypeError(node)

    def render(self, node: ast.While) -> None:  # noqa
        raise TypeError(node)
