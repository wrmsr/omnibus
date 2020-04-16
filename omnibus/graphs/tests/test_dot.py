import textwrap

import pytest

from .. import dot as dot_


@pytest.mark.skip()
def test_open_dot():
    src = textwrap.dedent("""
    digraph G {
        a;
        b;
        a -> b;
    }
    """)
    dot_.open_dot(src)
