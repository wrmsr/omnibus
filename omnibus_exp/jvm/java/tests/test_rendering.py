from .. import ast
from .. import rendering


def test_expressions():
    n = ast.Binary(
        ast.Binary.Op.ADD,
        ast.Literal(1),
        ast.Literal(2),
    )

    r = rendering.Renderer()
    r.render(n)
    print(r._writer.getvalue())
