import ast

from .. import pyasts
from .. import rendering  # noqa


def test_pyasts():
    print()

    for s in [
        '123',
        '1 + 1',
        open(__file__, 'r').read(),
    ]:
        an = ast.parse(s, 'exec')
        print(an)

        n = pyasts.translate(an)
        print(n)

        # print(rendering.render(n))
        print()
