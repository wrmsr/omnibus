from .. import parsing


def test_deps():
    parsing.parse('abcd==4.20')
