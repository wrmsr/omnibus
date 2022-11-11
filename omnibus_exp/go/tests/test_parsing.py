import os.path

from ..parsing import parse


def test_parse():
    with open(os.path.join(os.path.dirname(__file__), 'examples/example.go'), 'r') as f:
        buf = f.read()
    parse(buf)
