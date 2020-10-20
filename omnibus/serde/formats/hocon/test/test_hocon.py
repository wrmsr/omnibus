import os.path
import pprint

from .. import parsing
from .. import utils


def test_hocon():
    with open(os.path.join(os.path.dirname(__file__), 'examples/simple1.conf'), 'r') as f:
        res1 = parsing.parse(f.read())
    with open(os.path.join(os.path.dirname(__file__), 'examples/simple2.conf'), 'r') as f:
        res2 = parsing.parse(f.read())

    pprint.pprint(utils.unwrap_value(res1))
    pprint.pprint(utils.unwrap_value(res2))

    res3 = utils.resolve_references(res2)
    pprint.pprint(utils.unwrap_value(res3))

    with open(os.path.join(os.path.dirname(__file__), 'examples/references.conf'), 'r') as f:
        refs = parsing.parse(f.read())

    pprint.pprint(utils.unwrap_value(refs))

    rrefs = utils.resolve_references(refs)
    pprint.pprint(utils.unwrap_value(rrefs))
