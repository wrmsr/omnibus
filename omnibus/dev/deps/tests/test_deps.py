from .. import parsing


def test_deps():
    print(parsing.parse('abcd==4.20'))
    print(parsing.parse('abcd[a,b]==4.20'))
