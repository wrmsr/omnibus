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


class Invert(Decorator[E]):

    def child_success(self, task: 'Task[E]') -> None:
        super().child_fail(task)

    def child_fail(self, task: 'Task[E]') -> None:
        super().child_success(task)


class Random(Decorator[E]):

    def __init__(self, child: Task[E] = None, chance: float = 0.5) -> None:
        raise NotImplementedError


class Repeat(Decorator[E]):

    def __init__(self, child: Task[E] = None) -> None:
        raise NotImplementedError


class SemaphoreGuard(Decorator[E]):

    def __init__(self, child: Task[E] = None) -> None:
        raise NotImplementedError


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
