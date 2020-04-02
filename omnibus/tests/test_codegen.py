import datetime
import inspect

from .. import codegen as cg


def test_codegen():
    def run(fn):
        nsb = cg.NamespaceBuilder()
        cg.render_arg_spec(cg.ArgSpec.from_inspect(inspect.getfullargspec(fn)), nsb)

    run(lambda: None)
    run(lambda a: None)
    run(lambda a=0: None)
    run(lambda a, b: None)
    run(lambda a, b=0: None)
    run(lambda a=0, b=0: None)
    run(lambda a, b, *c: None)
    run(lambda a, b, *, c: None)
    run(lambda a, b, *, c=0: None)
    run(lambda a, b, *, c=0, **k: None)


def test_namegen():
    ng = cg.name_generator()
    assert ng() == '_0'
    assert ng() == '_1'

    nsb = cg.NamespaceBuilder()
    now = datetime.datetime.now()
    assert nsb.put(0) == '_0'
    assert nsb.put(now) == '_1'
    assert dict(nsb) == {'_0': 0, '_1': now}

    g = cg.Codegen()
    g('hi\n')
    with g.indent():
        g('there\n')

    print()
    print(str(g))
