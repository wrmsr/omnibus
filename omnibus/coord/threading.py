import threading
import typing as ta

from .. import check
from .. import lang
from .types import Coordination
from .types import Event
from .types import Lease
from .types import Lock
from .types import Object
from .types import Semaphore
from .types import TimeoutException  # noqa


class ThreadingObject(Object, lang.Abstract):

    def __init__(self, name: str, coord: 'ThreadingCoordination') -> None:
        super().__init__()

        self._name = check.not_empty(name)
        self._coord = check.isinstance(coord, ThreadingCoordination)

    @property
    def name(self) -> str:
        return self._name


class ThreadingLock(ThreadingObject, Lock):

    def __init__(self, obj: threading.Lock, name: str, coord: 'ThreadingCoordination') -> None:
        super().__init__(name, coord)

        self._obj = obj

    def acquire(self, *, timeout: ta.Optional[float] = None) -> Lease:
        raise NotImplementedError


class ThreadingSemaphore(ThreadingObject, Semaphore):

    def __init__(self, obj: threading.Semaphore, name: str, coord: 'ThreadingCoordination') -> None:
        super().__init__(name, coord)

        self._obj = obj

    def acquire(self, *, timeout: ta.Optional[float] = None) -> Lease:
        raise NotImplementedError


class ThreadingEvent(ThreadingObject, Event):

    def __init__(self, obj: threading.Event, name: str, coord: 'ThreadingCoordination') -> None:
        super().__init__(name, coord)

        self._obj = obj

    def is_set(self) -> bool:
        return self._obj.is_set()

    def set(self) -> None:
        self._obj.set()

    def clear(self) -> None:
        self._obj.clear()

    def wait(self, timeout: ta.Optional[float] = None) -> None:
        raise NotImplementedError


class ThreadingCoordination(Coordination):

    def __init__(self) -> None:
        super().__init__()

        self._objects_by_name: ta.MutableMapping[str, ThreadingObject] = {}
        self._lock = threading.RLock()

    @lang.context_wrapped('_lock')
    def lock(self, name: str) -> Lock:
        try:
            return check.isinstance(self._objects_by_name[name], ThreadingLock)
        except KeyError:
            pass
        raise NotImplementedError

    @lang.context_wrapped('_lock')
    def semaphore(self, name: str, value: int) -> Semaphore:
        try:
            return check.isinstance(self._objects_by_name[name], ThreadingSemaphore)
        except KeyError:
            pass
        raise NotImplementedError

    @lang.context_wrapped('_lock')
    def event(self, name: str) -> Event:
        try:
            return check.isinstance(self._objects_by_name[name], ThreadingEvent)
        except KeyError:
            pass
        raise NotImplementedError
