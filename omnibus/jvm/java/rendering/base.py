import typing as ta

from .. import ast
from .... import code
from .... import dispatch


T = ta.TypeVar('T')


class BaseRenderer(dispatch.Class):

    def __init__(
            self,
            *,
            writer: ta.Optional[code.IndentWriter] = None,
    ) -> None:
        super().__init__()

        self._writer = writer if writer is not None else code.IndentWriter()

    def write(self, s: str) -> None:
        self._writer.write(s)

    def delimited_iter(self, items: ta.Iterable[T], delimiter: str, fn: ta.Callable[[T], None]) -> None:
        for i, e in enumerate(items):
            if i:
                self.write(delimiter)
            fn(e)

    render = dispatch.property()

    def render(self, obj: object) -> None:  # noqa
        raise TypeError(obj)

    def render(self, name: ast.Name) -> None:  # noqa
        self.write('.'.join(name.parts))

    def render(self, type: ast.Type) -> None:  # noqa
        self.render(type.name)
        if type.generics:
            self.write('<')
            self.delimited_iter(type.generics, ', ', self.render)
            self.write('>')
        for a in type.arrays:
            self.write('[')
            self.render(a)
            self.write(']')

    def render(self, access: ast.Access) -> None:  # noqa
        self.write(access.name.lower())

    def render_operands(self, operands: ta.Iterable[ta.Any]) -> None:
        self.delimited_iter(operands, ', ', self.render_params)

    def render_params(self, obj: ta.Any) -> None:
        self.write('(')
        self.render(obj)
        self.write(')')

    def render_prefixes(self, accesses: ta.Iterable[ta.Any]) -> None:
        if accesses:
            self.delimited_iter(accesses, ' ', self.render)
            self.write(' ')

    render_literal = dispatch.property()

    def render_literal(self, obj: object) -> None:  # noqa
        raise TypeError(obj)

    def render_literal(self, obj: str) -> None:  # noqa
        return self.write(f'"{obj}')
