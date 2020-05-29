import pytest

from .. import ents as ents_  # noqa
from .. import gens as gens_  # noqa
from .. import rand as rand_  # noqa
from .. import text as text_  # noqa


@pytest.mark.xfail()
def test_tpch():
    cg = gens_.CustomerGenerator(10, 1, 20)
    for c in cg:
        print(c)
