import typing as ta

from . import check
from . import dataclasses as dc
from . import defs
from . import lang


lang.warn_unstable()


T = ta.TypeVar('T')


@dc.dataclass(frozen=True)
class LifecycleState(lang.Sealed):
    name: str
    phase: int
    is_failed: bool


class LifecycleStates(lang.ValueEnum):

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

    def lifecycle_construct(self) -> None:
        pass

    def lifecycle_start(self) -> None:
        pass

    def lifecycle_stop(self) -> None:
        pass

    def lifecycle_destroy(self) -> None:
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


LifecycleCallback = ta.Callable[[T], None]


class CallbackLifecycleListener(LifecycleListener[T], lang.Final):

    def __init__(
            self,
            *,
            on_starting: LifecycleCallback = None,
            on_started: LifecycleCallback = None,
            on_stopping: LifecycleCallback = None,
            on_stopped: LifecycleCallback = None,
    ):
        super().__init__()

        self._on_starting = check.callable(on_starting) if on_starting is not None else None
        self._on_started = check.callable(on_started) if on_starting is not None else None
        self._on_stopping = check.callable(on_stopping) if on_starting is not None else None
        self._on_stopped = check.callable(on_stopped) if on_starting is not None else None

    def on_starting(self, obj: T) -> None:
        if self._on_starting is not None:
            self._on_starting(obj)

    def on_started(self, obj: T) -> None:
        if self._on_started is not None:
            self._on_started(obj)

    def on_stopping(self, obj: T) -> None:
        if self._on_stopping is not None:
            self._on_stopping(obj)

    def on_stopped(self, obj: T) -> None:
        if self._on_stopped is not None:
            self._on_stopped(obj)


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

        self._state = LifecycleStates.NEW
        self._listeners: ta.List[LifecycleListener] = []

    defs.repr('lifecycle', 'state')

    @property
    def lifecycle(self) -> Lifecycle:
        return self._lifecycle

    @property
    def state(self) -> LifecycleState:
        return self._state

    def add_listener(self, listener: LifecycleListener) -> 'LifecycleController':
        self._listeners.append(check.isinstance(listener, LifecycleListener))
        return self

    def _advance(self) -> None:
        """
        synchronized (lock) {
            checkState(state == LifecycleState.NEW);
            state = LifecycleState.CONSTRUCTING;
            try {
                lifecycle.construct();
            }
            catch (Exception e) {
                state = LifecycleState.FAILED_CONSTRUCTING;
                throw new RuntimeException(e);
            }
            state = LifecycleState.CONSTRUCTED;
        }
        """
        with self._lock:

