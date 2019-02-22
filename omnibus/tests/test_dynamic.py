from .. import dynamic as dyn


def test_dyn():
    with dyn.dyn(x=5):
        assert dyn.dyn.x == 5
        with dyn.dyn(y=10):
            assert dyn.dyn.x == 5 and dyn.dyn.y == 10
            with dyn.dyn(x=6):
                assert dyn.dyn.x == 6 and dyn.dyn.y == 10
                with dyn.dyn(y=11):
                    assert dyn.dyn.x == 6 and dyn.dyn.y == 11
                assert dyn.dyn.x == 6 and dyn.dyn.y == 10
            assert dyn.dyn.x == 5 and dyn.dyn.y == 10
        assert dyn.dyn.x == 5

    try:
        dyn.dyn.x
    except AttributeError:
        pass
    else:
        assert False

    def _g1():
        while True:
            yield dyn.dyn.x
    g1 = _g1()

    with dyn.dyn(x=99):
        assert next(g1) == 99

    def _g2(x):
        while True:
            with dyn.dyn(x=x):
                yield next(g1)

    # g2a = _g2('a')
    # g2b = _g2('b')

    # FIXME
    # assert next(g2a) == 'a'
    # assert next(g2b) == 'b'
    # with dyn.dyn(x=100):
    #     assert next(g1) == 100
    #     assert next(g2a) == 'a'
    #     assert next(g2b) == 'b'

    try:
        next(g1)
    except AttributeError:
        pass
    else:
        assert False


def test_var():
    v = dyn.Var()
    with v(4):
        assert v() == 4


def test_cm():
    v = dyn.Var(420)

    @dyn.contextmanager
    def cm():
        with v(421):
            yield

    assert v() == 420
    with cm():
        assert v() == 421
    assert v() == 420

    @dyn.contextmanager
    def cm2():
        with cm():
            yield

    assert v() == 420
    with cm2():
        assert v() == 421
    assert v() == 420
