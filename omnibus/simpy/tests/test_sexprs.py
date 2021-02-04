import ast

from .. import nodes as no  # noqa
from .. import rendering as ren
from .. import sexp


def test_sexprs():
    print()

    for s in [
        ['def', 'add2', ['x', 'y'],
         ['return', ['+', 'x', 2]]],

        ['def', 'say_hi', [],
         ['print', '~hi']]
    ]:
        print(s)

        t = sexp.xlat(s)
        print(t)

        rd = ren.render(t)
        print(rd.strip())

        ar2 = ast.parse(rd, 'exec')
        print(ar2)

        print()
