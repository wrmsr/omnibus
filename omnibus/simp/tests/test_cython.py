"""
TODO:
 - regex first, run through tokenizer next to skip strs (prob have to reconcile w/ regex, tok prob discards cmnts)
 - move all to omnibus.pyasts - + Analysis
 - ** need to disable cy hooks when importing to gen cy hooks lol **
"""
import ast
import bisect
import glob
import os.path

import yaml

from .. import rendering as ren
from ... import check
from ... import lang  # noqa
from ... import pyasts
from ...serde import mapping as sm
from ..pyasts import translate


_HC_PREFIX = '# @simp.'


def test_gen():
    for filnam in glob.glob('**/*.py', recursive=True):
        with open(filnam, 'r') as f:
            buf = f.read()

        lines = buf.splitlines()
        hcs = {i for i, l in enumerate(lines) if l.strip().startswith(_HC_PREFIX)}
        if not hcs:
            continue

        first_nodes_by_lineno = {}
        root = ast.parse(buf, 'exec')

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

        basic = pyasts.analyze(root)

        for hc, hc_node in hc_nodes.items():
            fn = check.isinstance(hc_node, ast.FunctionDef)
            print(fn.name)
            print(fn)
            print()

            ps = []
            c = fn
            while True:
                p = basic.parents_by_node[c]
                if not p:
                    break
                ps.append(p)
                c = p
            print(ps)
            print()

            ns = []
            check.isinstance(ps[-1], ast.Module)
            for p in ps[:-1]:
                if isinstance(p, ast.ClassDef):
                    ns.append(p.name)
                else:
                    raise TypeError(p)

            mqfn = '.'.join([*ns, fn.name])
            print(mqfn)
            print()

            # 'omnibus/lang/descriptors.py'
            n, _, ext = filnam.rpartition('.')
            check.state(ext == 'py')
            mod = lang.import_module(n.replace(os.path.sep, '.'))
            print(mod)
            print()

            o = mod
            for p in mqfn.split('.'):
                o = getattr(o, p)
            print(o)
            print()

            # for p in ps:
            #     if isinstance(p, ast.Class)

            nr = translate(fn)
            print(yaml.dump(sm.serialize(nr)))
            print()

            print(ren.render(nr))
            print()

            print()
