from .. import nodes as no
from .. import rendering


def test_rendering():
    n = no.BinExpr(no.Constant(4), no.BinOp.ADD, no.Constant(20))
    print(rendering.render(n))
