import typing as ta

from . import check
from . import dataclasses as dc
from . import defs
from . import lang


lang.warn_unstable()


T = ta.TypeVar('T')
LifecycleT = ta.TypeVar('LifecycleT', bound='Lifecycle')
LifecycleCallback = ta.Callable[[LifecycleT], None]


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


class CallbackLifecycle(Lifecycle, lang.Final, ta.Generic[LifecycleT]):

    def __init__(
            self,
            *,
            construct: LifecycleCallback[LifecycleT] = None,
            start: LifecycleCallback[LifecycleT] = None,
            stop: LifecycleCallback[LifecycleT] = None,
            destroy: LifecycleCallback[LifecycleT] = None,
    ):
        super().__init__()

        self._construct = check.callable(construct) if construct is not None else None
        self._start = check.callable(start) if construct is not None else None
        self._stop = check.callable(stop) if construct is not None else None
        self._destroy = check.callable(destroy) if construct is not None else None

    def lifecycle_construct(self) -> None:
        if self._construct is not None:
            self._construct()

    def lifecycle_start(self) -> None:
        if self._start is not None:
            self._start()

    def lifecycle_stop(self) -> None:
        if self._stop is not None:
            self._stop()

    def lifecycle_destroy(self) -> None:
        if self._destroy is not None:
            self._destroy()


class AbstractLifecycle(Lifecycle, lang.Abstract):

    def __init__(self: lang.Self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._lifecycle_delegate = CallbackLifecycle(
            construct=self._do_lifecycle_construct,
            start=self._do_lifecycle_start,
            stop=self._do_lifecycle_stop,
            destroy=self._do_lifecycle_destroy,
        )
        self._lifecycle_controller: LifecycleController[lang.Self] = LifecycleController(self)

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


class LifecycleListener(ta.Generic[LifecycleT]):

    def on_starting(self, obj: LifecycleT) -> None:
        pass

    def on_started(self, obj: LifecycleT) -> None:
        pass

    def on_stopping(self, obj: LifecycleT) -> None:
        pass

    def on_stopped(self, obj: LifecycleT) -> None:
        pass


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
            old: ta.Set[LifecycleState],
            new_intermediate: LifecycleState,
            new_failed: LifecycleState,
            new_succeeded: LifecycleState,
            lifecycle_fn: ta.Callable[[], None],
            pre_listener_fn: ta.Callable[[LifecycleListener[LifecycleT]], ta.Callable[[LifecycleT], None]] = None,
            post_listener_fn: ta.Callable[[LifecycleListener[LifecycleT]], ta.Callable[[LifecycleT], None]] = None,
    ) -> None:
        check.unique(list(old) + [new_intermediate, new_succeeded, new_failed])
        check.arg(all(new_intermediate.phase > o.phase for o in old))
        check.arg(new_failed.phase > new_intermediate.phase)
        check.arg(new_succeeded.phase > new_failed.phase)
        with self._lock:
            if pre_listener_fn is not None:
                for listener in self._listeners:
                    pre_listener_fn(listener)(self._lifecycle)
            check.state(self._state in old)
            self._state = new_intermediate
            try:
                lifecycle_fn()
            except Exception:
                self._state = new_failed
                raise
            self._state = new_succeeded
            if post_listener_fn is not None:
                for listener in self._listeners:
                    post_listener_fn(listener)(self._lifecycle)

    def lifecycle_construct(self) -> None:
        self._advance(
            {LifecycleStates.NEW},
            LifecycleStates.CONSTRUCTING,
            LifecycleStates.FAILED_CONSTRUCTING,
            LifecycleStates.CONSTRUCTED,
            self._lifecycle.lifecycle_construct,
        )

    def lifecycle_start(self) -> None:
        self._advance(
            {LifecycleStates.CONSTRUCTED},
            LifecycleStates.STARTING,
            LifecycleStates.FAILED_STARTING,
            LifecycleStates.STARTED,
            self._lifecycle.lifecycle_start,
            lambda l: l.on_starting,
            lambda l: l.on_started,
        )

    def lifecycle_stop(self) -> None:
        self._advance(
            {LifecycleStates.STARTED},
            LifecycleStates.STOPPING,
            LifecycleStates.FAILED_STOPPING,
            LifecycleStates.STOPPED,
            self._lifecycle.lifecycle_stop,
            lambda l: l.on_stopping,
            lambda l: l.on_stopped,
        )

    def lifecycle_destroy(self) -> None:
        self._advance(
            {
                LifecycleStates.NEW,

                LifecycleStates.CONSTRUCTING,
                LifecycleStates.FAILED_CONSTRUCTING,
                LifecycleStates.CONSTRUCTED,

                LifecycleStates.STARTING,
                LifecycleStates.FAILED_STARTING,
                LifecycleStates.STARTED,

                LifecycleStates.STOPPING,
                LifecycleStates.FAILED_STOPPING,
                LifecycleStates.STOPPED,
            },
            LifecycleStates.DESTROYING,
            LifecycleStates.FAILED_DESTROYING,
            LifecycleStates.DESTROYED,
            self._lifecycle.lifecycle_destroy,
        )
