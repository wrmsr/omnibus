import ast
import bisect
import glob
import typing as ta

from .. import rendering as ren
from ... import check
from ..asts import translate


_HC_PREFIX = '# @simpy.'


def _build_parents(root: ast.AST) -> ta.Mapping[ta.Any, ast.AST]:
    dct = {}
    todo = [root]
    seen = set()
    last = None
    while todo:
        cur = todo.pop()
        if not isinstance(cur, (ast.expr_context, ast.operator, ast.cmpop, ast.unaryop)):
            check.not_in(cur, seen)
            seen.add(cur)
        if last is not None:
            dct[cur] = last
        for nxt in ast.iter_child_nodes(cur):
            if isinstance(nxt, ast.AST):
                todo.append(nxt)
        last = cur
    return dct


def test_gen():
    for fn in glob.glob('**/*.py', recursive=True):
        with open(fn, 'r') as f:
            buf = f.read()

        lines = buf.splitlines()
        hcs = {i for i, l in enumerate(lines) if l.strip().startswith(_HC_PREFIX)}
        if not hcs:
            continue

        first_nodes_by_lineno = {}
        root = ast.parse(buf, 'exec')

        parents = _build_parents(root)  # noqa

        for cur in ast.walk(root):
            if (
                    isinstance(cur, ast.AST) and
                    hasattr(cur, 'lineno') and
                    cur.lineno and
                    cur.lineno not in first_nodes_by_lineno
            ):
                first_nodes_by_lineno[cur.lineno] = cur

        hc_nodes = {}
        linenos = sorted(first_nodes_by_lineno)
        for hc in hcs:
            i = bisect.bisect(linenos, hc)
            # TODO: while(isinstance(hcn, ast.Decorator)): ...
            hc_nodes[hc] = first_nodes_by_lineno[linenos[i]]

        for hc, hc_node in hc_nodes.items():
            fn = check.isinstance(hc_node, ast.FunctionDef)
            print(fn.name)
            print(fn)
            nr = translate(fn)
            print(nr)
            print(ren.render(nr))
            print()
