import abc
import logging
import time
import typing as ta

from .. import dataclasses as dc


log = logging.getLogger(__name__)


BaseSchedulerEntryT = ta.TypeVar('BaseSchedulerEntryT', bound='BaseScheduler.Entry', covariant=True)


class Schedulable(abc.ABC):

    @abc.abstractmethod
    def run(self, ttl: float) -> None:
        raise NotImplementedError


class Scheduler(Schedulable):

    @abc.abstractmethod
    def add(self, schedulable: Schedulable, frequency: int, *, phase: int = None) -> None:
        raise NotImplementedError


class BaseScheduler(ta.Generic[BaseSchedulerEntryT], Schedulable):

    class Entry(dc.Data, frozen=True):
        schedulable: Schedulable
        frequency: int
        phase: int

    def __init__(self, dry_run_frames: int = 0) -> None:
        super().__init__()

        self._schedulable: ta.List[BaseSchedulerEntryT] = []
        self._phase_counters: ta.List[int] = []
        self._dry_run_frames = dry_run_frames
        self._frame = 0

    def _calculate_phase(self, frequency: int) -> int:
        self._phase_counters = [0] * frequency

        for frame in range(self._dry_run_frames):
            slot = frame % frequency
            for entry in self._schedulable:
                if (frame - entry.phase) % entry.frequency == 0:
                    self._phase_counters[slot] += 1

        min_value = 2 ** 32
        min_value_at = -1
        for i in range(frequency):
            if self._phase_counters[i] < min_value:
                min_value = self._phase_counters[i]
                min_value_at = i
        return min_value_at


class PriorityScheduler(BaseScheduler['PriorityScheduler.Entry']):

    class Entry(BaseScheduler.Entry):
        priority: float

    def __init__(self, dry_run_frames: int = 0) -> None:
        super().__init__(dry_run_frames)

    def run(self, ttl: float) -> None:
        ttl = float(ttl)
        self._frame += 1

        runnable = []
        total_priority = 0.
        for entry in self._schedulable:
            if (self._frame + entry.phase) % entry.frequency == 0:
                runnable.append(entry)
                total_priority += entry.priority

        last_time = time.time()
        for entry in runnable:
            now = time.time()
            ttl -= now - last_time
            available_time = (ttl * entry.priority / total_priority)

            entry.schedulable.run(available_time)
            last_time = now

    def add(
            self,
            schedulable: Schedulable,
            frequency: int,
            *,
            phase: int = None,
            priority: float = 1.,
    ) -> None:
        self._schedulable.append(
            self.Entry(
                schedulable,
                frequency,
                phase if phase is not None else self._calculate_phase(frequency),
                priority,
            ))


class LoadBalancingScheduler(BaseScheduler[BaseScheduler.Entry]):

    def run(self, ttl: float) -> None:
        ttl = float(ttl)
        self._frame += 1

        runnable = []
        for entry in self._schedulable:
            if (self._frame + entry.phase) % entry.frequency == 0:
                runnable.append(entry)

        last_time = time.time()
        for entry in runnable:
            now = time.time()
            ttl -= now - last_time
            available_time = ttl / (len(runnable) - 1)

            entry.schedulable.run(available_time)
            last_time = now

    def add(
            self,
            schedulable: Schedulable,
            frequency: int,
            *,
            phase: int = None,
    ) -> None:
        self._schedulable.append(
            self.Entry(
                schedulable,
                frequency,
                phase if phase is not None else self._calculate_phase(frequency),
            ))
