import typing as ta

from .. import nodes as no  # noqa


T = ta.TypeVar('T')


def c(o: T) -> T:
    return o


def test_sexprs():
    add2 = ['def', 'add2', ['x', 'y'],  # noqa
            ['return', ['+', 'x', 2]]]

    say_hi = ['def', 'say_hi', [],  # noqa
              ['print', c('hi')]]
