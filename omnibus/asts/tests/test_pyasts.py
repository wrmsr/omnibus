import ast

from .. import pyasts


def test_pyasts():
    an = ast.parse('123', 'eval')
    n = pyasts.translate(an)
    print(n)
