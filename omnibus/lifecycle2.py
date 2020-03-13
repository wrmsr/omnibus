import typing as ta

from . import check
from . import dataclasses as dc
from . import lang


lang.warn_unstable()


T = ta.TypeVar('T')


@dc.dataclass(frozen=True)
class LifecycleState(lang.Sealed):
    name: str
    phase: int
    is_failed: bool


class LifecycleState(lang.ValueEnum):

    NEW = LifecycleState('NEW', 0, False)

    CONSTRUCTING = LifecycleState('CONSTRUCTING', 1, False)
    FAILED_CONSTRUCTING = LifecycleState('FAILED_CONSTRUCTING', 2, True)
    CONSTRUCTED = LifecycleState('CONSTRUCTED', 3, False)

    STARTING = LifecycleState('STARTING', 5, False)
    FAILED_STARTING = LifecycleState('FAILED_STARTING', 6, True)
    STARTED = LifecycleState('STARTED', 7, False)

    STOPPING = LifecycleState('STOPPING', 8, False)
    FAILED_STOPPING = LifecycleState('FAILED_STOPPING', 9, True)
    STOPPED = LifecycleState('STOPPED', 10, False)

    DESTROYING = LifecycleState('DESTROYING', 11, False)
    FAILED_DESTROYING = LifecycleState('FAILED_DESTROYING', 12, True)
    DESTROYED = LifecycleState('DESTROYED', 13, False)


class Lifecycle:

    def _construct(self) -> None:
        pass

    def _start(self) -> None:
        pass

    def _stop(self) -> None:
        pass

    def _destroy(self) -> None:
        pass


class LifecycleListener(ta.Generic[T]):

    def on_starting(self, obj: T) -> None:
        pass

    def on_started(self, obj: T) -> None:
        pass

    def on_stopping(self, obj: T) -> None:
        pass

    def on_stopped(self, obj: T) -> None:
        pass


class LifecycleController(Lifecycle):

    def __init__(
            self,
            lifecycle: Lifecycle,
            *,
            lock: lang.DefaultLockable = None,
    ) -> None:
        super().__init__()

        self._lifecycle = check.isinstance(lifecycle, Lifecycle)
        self._lock = lang.default_lock(lock, True)

        self._state = LifecycleState.NEW
        self._listeners: ta.List[LifecycleListener] = []
