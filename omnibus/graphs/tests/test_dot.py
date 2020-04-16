import textwrap

from .. import dot as dot_


def test_open_dot():
    dot_.open_dot(textwrap.dedent("""
    digraph G {
        a;
        b;
        a -> b;
    }
    """))
