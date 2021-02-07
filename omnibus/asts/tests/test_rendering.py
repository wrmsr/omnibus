from .. import nodes as no
from .. import rendering


def test_rendering():
    print(rendering.render(no.BinExpr(no.Constant(4), no.BinOps.ADD, no.Constant(20))))
    print(rendering.render(no.Name('abc')))
