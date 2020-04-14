import datetime
import inspect

import pytest

from .. import codegen as cg


def test_codegen():
    def run(fn):
        nsb = cg.NamespaceBuilderLkkk()
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
    assert ng('self') == '_self0'

    nsb = cg.NamespaceBuilder()
    now = datetime.datetime.now()
    assert nsb.add(0) == '_0'
    assert nsb.add(now) == '_1'
    assert dict(nsb) == {'_0': 0, '_1': now}

    g = cg.Codegen()
    g('hi\n')
    with g.indent():
        g('there\n')

    print()
    print(str(g))


def test_createfn():
    fn = cg.create_fn('fn', cg.ArgSpec(['x', 'y']), 'return x + y')
    assert fn(1, 2) == 3

    fn = cg.create_fn('fn', cg.ArgSpec(['x', 'y']), 'raise ValueError')
    with pytest.raises(ValueError):
        assert fn(1, 2) == 3
