import typing as ta

from ... import check
from .base import LeafTask
from .base import Task


E = ta.TypeVar('E')


class Failure(LeafTask[E]):

    def execute(self) -> Task.Status:
        return Task.Status.FAILED


class Success(LeafTask[E]):

    def execute(self) -> Task.Status:
        return Task.Status.SUCCEEDED


class Wait(LeafTask[E]):

    def __init__(
            self,
            seconds: ta.Union[ta.Callable[[], float], float],
            clock: ta.Callable[[], float],
    ) -> None:
        super().__init__()

        self._seconds = seconds if callable(seconds) else lambda: seconds
        self._clock = check.callable(clock)

        self._start_time = 0.
        self._timeout = 0.

    def start(self) -> None:
        self._timeout = self._seconds()
        self._start_time = self._clock()

    def execute(self) -> Task.Status:
        if (self._clock() - self._start_time) < self._timeout:
            return Task.Status.RUNNING
        else:
            return Task.Status.SUCCEEDED
