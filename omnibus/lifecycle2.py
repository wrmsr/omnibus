import typing as ta

from . import check
from . import dataclasses as dc
from . import defs
from . import lang


lang.warn_unstable()


T = ta.TypeVar('T')
LifecycleT = ta.TypeVar('LifecycleT', bound='Lifecycle')


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


class LifecycleListener(ta.Generic[LifecycleT]):

    def on_starting(self, obj: LifecycleT) -> None:
        pass

    def on_started(self, obj: LifecycleT) -> None:
        pass

    def on_stopping(self, obj: LifecycleT) -> None:
        pass

    def on_stopped(self, obj: LifecycleT) -> None:
        pass


LifecycleCallback = ta.Callable[[T], None]


class CallbackLifecycleListener(LifecycleListener[LifecycleT], lang.Final):

    def __init__(
            self,
            *,
            on_starting: LifecycleCallback[LifecycleT] = None,
            on_started: LifecycleCallback[LifecycleT] = None,
            on_stopping: LifecycleCallback[LifecycleT] = None,
            on_stopped: LifecycleCallback[LifecycleT] = None,
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


class LifecycleController(Lifecycle, ta.Generic[LifecycleT]):

    def __init__(
            self,
            lifecycle: LifecycleT,
            *,
            lock: lang.DefaultLockable = None,
    ) -> None:
        super().__init__()

        self._lifecycle = check.isinstance(lifecycle, Lifecycle)
        self._lock = lang.default_lock(lock, True)

        self._state = LifecycleStates.NEW
        self._listeners: ta.List[LifecycleListener[LifecycleT]] = []

    defs.repr('lifecycle', 'state')

    @property
    def lifecycle(self) -> LifecycleT:
        return self._lifecycle

    @property
    def state(self) -> LifecycleState:
        return self._state

    def add_listener(self, listener: LifecycleListener[LifecycleT]) -> 'LifecycleController':
        self._listeners.append(check.isinstance(listener, LifecycleListener))
        return self

    def _advance(
            self,
            old: LifecycleState,
            new_intermediate: LifecycleState,
            new_succeeded: LifecycleState,
            new_failed: LifecycleState,
            fn: ta.Callable[[], None],
            listener_fn: ta.Callable[[LifecycleListener[LifecycleT], LifecycleT], None] = None,
    ) -> None:
        check.unique([old, new_intermediate, new_succeeded, new_failed])
        check.arg(new_intermediate.phase > old.phase)
        check.arg(new_failed.phase > new_intermediate.phase)
        check.arg(new_succeeded.phase > new_failed.phase)
        with self._lock:
            check.state(self._state is old)
            self._state = new_intermediate
            try:
                fn()
            except Exception:
                self._state = new_failed
                raise
            self._state = new_succeeded
        if listener_fn is not None:
            for listener in self._listeners:
                listener_fn(listener, self._lifecycle)

