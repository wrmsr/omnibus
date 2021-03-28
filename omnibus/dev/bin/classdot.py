"""
TODO:
 - https://stackoverflow.com/questions/19308847/graphviz-vertical-ordering
  - (same expected mro past top ~= same expected ver pos, order by name)
"""
import typing as ta

from ...graphs.dot import dot


def gen_class_dot(roots: ta.Iterable[type]) -> dot.Graph:
    roots = set(roots)
    root_tup = tuple(roots)

    stmts = []
    stmts.append(dot.RawStmt('rankdir=LR;'))

    todo = set(roots)
    seen = set()
    while todo:
        cur = todo.pop()
        seen.add(cur)
        stmts.append(dot.Node(str(id(cur)), {'label': '.'.join([cur.__module__, cur.__qualname__])}))
        for base in cur.__bases__:
            if issubclass(base, root_tup):
                stmts.append(dot.Edge(str(id(base)), str(id(cur))))
        for sub in cur.__subclasses__():
            if issubclass(sub, root_tup):
                if sub not in seen:
                    todo.add(sub)

    return dot.Graph(stmts)


def _main():
    import sys

    from ... import lang

    roots = []
    for spec in sys.argv[1:]:
        cls = lang.import_module_attr(spec)
        roots.append(cls)

    if not roots:
        return

    scd = gen_class_dot(roots)
    dot.open_dot(dot.render(scd))


if __name__ == '__main__':
    _main()
