from .. import lifecycle2


def test_lifecycle():
    class L(lifecycle2.Lifecycle):

        def lifecycle_construct(self) -> None:
            super().lifecycle_construct()

        def lifecycle_start(self) -> None:
            super().lifecycle_start()

        def lifecycle_stop(self) -> None:
            super().lifecycle_stop()

        def lifecycle_destroy(self) -> None:
            super().lifecycle_destroy()

    l = L()

    c = lifecycle2.LifecycleController(l)

    c.lifecycle_construct()
    c.lifecycle_start()
    c.lifecycle_stop()
    c.lifecycle_destroy()


def test_abstract_lifecycle():
    class L(lifecycle2.AbstractLifecycle):

        def _do_lifecycle_construct(self) -> None:
            super()._do_lifecycle_construct()

        def _do_lifecycle_start(self) -> None:
            super()._do_lifecycle_start()

        def _do_lifecycle_stop(self) -> None:
            super()._do_lifecycle_stop()

        def _do_lifecycle_destroy(self) -> None:
            super()._do_lifecycle_destroy()

    l = L()

    l.lifecycle_construct()
    l.lifecycle_start()
    l.lifecycle_stop()
    l.lifecycle_destroy()
