import contextlib
import threading
import typing as ta
import weakref

from . import lang


TLC = ta.TypeVar('TLC', bound='ThreadLocalContext')


class ThreadLocalContext(lang.Abstract):

    _LOCAL = threading.local()

    def __init__(self) -> None:
        super().__init__()

        self._exit_stack = contextlib.ExitStack()
        self._previous: 'ThreadLocalContext' = None

    @property
    def previous(self) -> ta.Optional['ThreadLocalContext']:
        return self._previous

    def __enter__(self) -> 'ThreadLocalContext':
        try:
            current_by_type = self._LOCAL.current_by_type
        except AttributeError:
            current_by_type = self._LOCAL.current_by_type = weakref.WeakKeyDictionary()
        try:
            self._previous = current_by_type[type(self)]
        except KeyError:
            self._previous = None
        current_by_type[type(self)] = self
        self._exit_stack.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> ta.Any:
        try:
            return self._exit_stack.__exit__(exc_type, exc_val, exc_tb)
        finally:
            if self.previous is None:
                del self._LOCAL.current_by_type[type(self)]
            else:
                self._LOCAL.current_by_type[type(self)] = self.previous

    @classmethod
    def current(cls: ta.Type[TLC]) -> TLC:
        try:
            return cls._LOCAL.current_by_type[cls]
        except AttributeError:
            raise KeyError


class CountDownLatch:

    def __init__(self, count: int = 1) -> None:
        super().__init__()

        self._count = count
        self._lock = threading.Condition()

    def count_down(self) -> None:
        with self._lock:
            self._count -= 1
            if self._count <= 0:
                self._lock.notify_all()

    def wait(self, timeout: int = -1) -> None:
        with self._lock.acquire(timeout=timeout):
            while self._count > 0:
                self._lock.wait()
