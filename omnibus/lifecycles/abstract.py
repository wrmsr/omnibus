from .. import lang
from .controller import LifecycleController
from .controller import LifecycleState
from .types import CallbackLifecycle
from .types import Lifecycle


class AbstractLifecycle(Lifecycle, lang.Abstract):

    def __init__(self: lang.Self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._lifecycle_delegate = CallbackLifecycle(
            construct=self._do_lifecycle_construct,
            start=self._do_lifecycle_start,
            stop=self._do_lifecycle_stop,
            destroy=self._do_lifecycle_destroy,
        )
        self._lifecycle_controller: LifecycleController[lang.Self] = LifecycleController(self._lifecycle_delegate)

    @property
    def lifecycle_controller(self) -> 'LifecycleController[lang.Self]':
        return self._lifecycle_controller

    @property
    def lifecycle_state(self) -> LifecycleState:
        return self._lifecycle_controller.state

    def lifecycle_construct(self) -> None:
        self._lifecycle_controller.lifecycle_construct()

    def _do_lifecycle_construct(self) -> None:
        pass

    def lifecycle_start(self) -> None:
        self._lifecycle_controller.lifecycle_start()

    def _do_lifecycle_start(self) -> None:
        pass

    def lifecycle_stop(self) -> None:
        self._lifecycle_controller.lifecycle_stop()

    def _do_lifecycle_stop(self) -> None:
        pass

    def lifecycle_destroy(self) -> None:
        self._lifecycle_controller.lifecycle_destroy()

    def _do_lifecycle_destroy(self) -> None:
        pass
