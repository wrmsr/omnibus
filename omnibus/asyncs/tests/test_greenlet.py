from ...dev.testing import helpers


@helpers.skip_if_cant_import('greenlet')
def test_greenlet():
    import greenlet

    def test1():
        gr2.switch()
        gr2.switch()
        nonlocal done
        done += 1

    def test2():
        def f():
            gr1.switch()
        f()
        nonlocal done
        done += 1
        gr1.switch()

    done = 0
    gr1 = greenlet.greenlet(test1)
    gr2 = greenlet.greenlet(test2)
    gr1.switch()
    assert done == 2
