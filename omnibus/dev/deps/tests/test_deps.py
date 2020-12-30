from .. import parsing


def test_deps():
    def f(s):
        n = parsing.parse(s)
        print(n)
        print(parsing.render(n))

    f('abcd==4.20')
    f('abcd[a,b]==4.20')
    # f("PyHive[hive]==0.6.3; python_version < '3.9'")
