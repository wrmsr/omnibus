import random
import typing as ta

from .base import E
from .base import Task
from .base import Decorator
from .base import LoopDecorator


class AlwaysFail(Decorator[E]):

    def child_success(self, task: 'Task[E]') -> None:
        self.child_fail(task)


class AlwaysSucceed(Decorator[E]):

    def child_fail(self, task: 'Task[E]') -> None:
        self.child_success(task)


class Include(Decorator[E]):

    def __init__(self):
        raise NotImplementedError

    def start(self) -> None:
        raise NotImplementedError


class Invert(Decorator[E]):

    def child_success(self, task: 'Task[E]') -> None:
        super().child_fail(task)

    def child_fail(self, task: 'Task[E]') -> None:
        super().child_success(task)


class Random(Decorator[E]):

    def __init__(self, chance: float = 0.5, child: Task[E] = None) -> None:
        super().__init__(child)

        self._chance = chance

    def run(self) -> None:
        if self._child is not None:
            super().run()
        else:
            self.decide()

    def child_fail(self, task: 'Task[E]') -> None:
        self.decide()

    def child_success(self, task: 'Task[E]') -> None:
        self.decide()

    def decide(self) -> None:
        if random.random() >= self._chance:
            self.success()
        else:
            self.fail()


class Repeat(LoopDecorator[E]):

    def __init__(self, times: int = 2, child: Task[E] = None) -> None:
        super().__init__(child)

        self._times = times
        self._count = 0

    @property
    def condition(self) -> bool:
        return self._loop and bool(self._count)

    def start(self) -> None:
        self._count = self._times

    def child_fail(self, task: 'Task[E]') -> None:
        self.child_success(task)

    def child_success(self, task: 'Task[E]') -> None:
        if self._count:
            self._count -= 1
        if not self._count:
            super().child_success(task)
            self._loop = False
        else:
            self._loop = True


class Semaphore(ta.Protocol):

    def acquire(self, num: int = 1) -> bool:
        ...

    def release(self, num: int = 1) -> bool:
        ...


class SemaphoreGuard(Decorator[E]):

    def __init__(self, semaphore: Semaphore, child: Task[E] = None) -> None:
        super().__init__(child)

        self._semaphore = semaphore
        self._acquired = False

    def start(self) -> None:
        self._acquired = self._semaphore.acquire()
        super().start()

    def run(self) -> None:
        if self._acquired:
            super().run()
        else:
            self.fail()

    def end(self) -> None:
        if self._acquired:
            self._semaphore.release()
            self._acquired = False
        super().end()


class UntilFail(LoopDecorator[E]):

    def child_success(self, task: 'Task[E]') -> None:
        self._loop = True

    def child_fail(self, task: 'Task[E]') -> None:
        self.success()
        self._loop = False


class UntilSuccess(LoopDecorator[E]):

    def child_success(self, task: 'Task[E]') -> None:
        self.success()
        self._loop = False

    def child_fail(self, task: 'Task[E]') -> None:
        self._loop = True
