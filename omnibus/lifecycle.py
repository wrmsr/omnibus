import logging
import sys
import threading
import typing as ta

from . import lang
from . import check


lang.warn_unstable()


Self = ta.TypeVar('Self')
LifecycleListener = ta.Callable[['Lifecycle', 'Lifecycle.State'], None]


log = logging.getLogger(__name__)


class Lifecycle(lang.ExitStacked):

    class State(lang.AutoEnum):
        NEW = ...
        STARTING = ...
        STARTED = ...
        STOPPING = ...
        STOPPED = ...

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self._lifecycle_state = Lifecycle.State.NEW
        self._lifecycle_lock = threading.RLock()
        self._lifecycle_listeners: ta.List[LifecycleListener] = []

    @property
    def lifecycle_state(self) -> 'Lifecycle.State':
        return self._lifecycle_state

    def add_lifecycle_listener(self, listener: LifecycleListener) -> Self:
        self._lifecycle_listeners.append(listener)
        return self

    def _call_lifecycle_listeners(self) -> None:
        for listener in self._lifecycle_listeners:
            try:
                listener(self, self._lifecycle_state)
            except Exception:
                log.exception('Error in lifecycle listener')

    @property
    def is_started(self) -> bool:
        return self._lifecycle_state == Lifecycle.State.STARTED

    @lang.context_wrapped('_lifecycle_lock')
    def __enter__(self: Self) -> Self:
        check.state(self._lifecycle_state == Lifecycle.State.NEW)
        self._lifecycle_state = Lifecycle.State.STARTING
        self._call_lifecycle_listeners()

        super().__enter__()
        try:
            self._start()
        except Exception:
            et, e, tb = sys.exc_info()
            super().__exit__(et, e, tb)
            raise

        self._lifecycle_state = Lifecycle.State.STARTED
        self._call_lifecycle_listeners()
        return self

    def _start(self) -> None:
        pass

    @lang.context_wrapped('_lifecycle_lock')
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        check.state(self._lifecycle_state == Lifecycle.State.STARTED)
        self._lifecycle_state = Lifecycle.State.STOPPING
        self._call_lifecycle_listeners()

        self._stop()
        super().__exit__(exc_type, exc_val, exc_tb)

        self._lifecycle_state = Lifecycle.State.STOPPED
        self._call_lifecycle_listeners()

    def _stop(self) -> None:
        pass
