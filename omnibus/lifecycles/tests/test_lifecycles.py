from .. import controller as controller_
from .. import manager as manager_
from .. import types as types_


def test_lifecycle():
    class L(types_.Lifecycle):

        def lifecycle_construct(self) -> None:
            super().lifecycle_construct()

        def lifecycle_start(self) -> None:
            super().lifecycle_start()

        def lifecycle_stop(self) -> None:
            super().lifecycle_stop()

        def lifecycle_destroy(self) -> None:
            super().lifecycle_destroy()

    l = L()

    c = controller_.LifecycleController(l)

    c.lifecycle_construct()
    c.lifecycle_start()
    c.lifecycle_stop()
    c.lifecycle_destroy()


def test_abstract_lifecycle():
    class L(types_.AbstractLifecycle):

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


def test_lifecycle_manager():
    class L(types_.AbstractLifecycle):

        def _do_lifecycle_construct(self) -> None:
            super()._do_lifecycle_construct()

        def _do_lifecycle_start(self) -> None:
            super()._do_lifecycle_start()

        def _do_lifecycle_stop(self) -> None:
            super()._do_lifecycle_stop()

        def _do_lifecycle_destroy(self) -> None:
            super()._do_lifecycle_destroy()

    l0 = L()
    l1 = L()

    lm = manager_.LifecycleManager()
    lm.add(l0)
    lm.add(l1, [l0])

    lm.construct()
    assert l0.lifecycle_state is types_.LifecycleStates.CONSTRUCTED
    assert l1.lifecycle_state is types_.LifecycleStates.CONSTRUCTED

    lm.start()

    lm.stop()

    lm.destroy()
