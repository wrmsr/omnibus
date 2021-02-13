import ast

from .. import pyasts


def test_pyasts():
    print()

    for s in [
        '123',
        '1 + 1',
    ]:
        an = ast.parse(s, 'eval')
        print(an)

        n = pyasts.translate(an)
        print(n)

        print()
