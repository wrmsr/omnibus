import ast

from . import nodes as no
from .. import dispatch


class Translator(dispatch.Class):
    translate = dispatch.property()

    def translate(self, an: ast.AST) -> no.Node:  # noqa
        raise TypeError(an)
