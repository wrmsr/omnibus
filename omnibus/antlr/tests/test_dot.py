import textwrap

from .. import antlr
from ... import collections as col
from ...graphs.dot import dot
from ._antlr.ChatLexer import ChatLexer  # type: ignore
from ._antlr.ChatParser import ChatParser  # type: ignore


def test_dot():
    buf = textwrap.dedent("""
    barf says: hi // comment0
    // comment1
    xarf says: /* comment2 */ xi
    """).lstrip()

    parsed = antlr.parse(buf, ChatLexer, ChatParser)
    root = parsed.chat()

    s = col.IdentitySet()
    q = [root]
    while q:
        c = q.pop()
        if c in s:
            raise ValueError
        s.add(c)
        for n in getattr(c, 'children', []):
            if n not in s:
                q.append(n)

    stmts = [dot.RawStmt('rankdir=LR;')]
    for c in s:
        stmts.append(dot.Node(f'_{id(c)}', {'label': str(type(c)), 'shape': 'box'}))
        for n in getattr(c, 'children', []):
            stmts.append(dot.Edge(f'_{id(c)}', f'_{id(n)}'))

    gv = dot.render(dot.Graph(stmts))
    print(gv)
    # dot.open_dot(gv)
