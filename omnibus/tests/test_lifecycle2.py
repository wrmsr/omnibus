from .. import lifecycle2


def test_lifecycle2():
    class L(lifecycle2.Lifecycle):
        pass

    l = L()

    c = lifecycle2.LifecycleController(l)

    c.lifecycle_construct()
    c.lifecycle_start()
    c.lifecycle_stop()
    c.lifecycle_destroy()
