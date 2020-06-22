import typing as ta

from .base import BaseRenderer
from .declarations import DeclarationRenderer
from .statements import StatementRenderer
from .expressions import ExpressionRenderer


T = ta.TypeVar('T')


class Renderer(
    DeclarationRenderer,
    StatementRenderer,
    ExpressionRenderer,
    BaseRenderer
):
    pass
