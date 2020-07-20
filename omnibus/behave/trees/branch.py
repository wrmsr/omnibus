import abc
import typing as ta

from ... import lang
from .base import BranchTask
from .base import E
from .base import SingleRunningChildBranch
from .base import Task


class DynamicGuardSelector(BranchTask[E]):

    def __init__(self, children: ta.Sequence[Task[E]] = None) -> None:
        super().__init__(children)

        self._running_child: Task[E] = None

    def child_running(self, task: 'Task[E]', reporter: 'Task[E]') -> None:
        self._running_child = task
        self.running()

    def child_success(self, task: 'Task[E]') -> None:
        self._running_child = None
        self.success()

    def child_fail(self, task: 'Task[E]') -> None:
        self._running_child = None
        self.fail()

    def run(self) -> None:
        child_to_run = None
        for child in self._children:
            if child.check_guard(self):
                child_to_run = child
                break

        if self._running_child is not None and self._running_child is not child_to_run:
            self._running_child.cancel()
            self._running_child = None

        if child_to_run is None:
            self.fail()
        else:
            if self._running_child is None:
                self._running_child = child_to_run
                self._running_child.control = self
                self._running_child.start()
            self._running_child.run()


class Parallel(BranchTask[E]):

    def __init__(
            self,
            children: ta.Sequence[Task[E]] = None,
            *,
            orchestrator: 'Parallel.Orchestrator' = None,
            policy: 'Parallel.Policy' = None,
    ) -> None:
        super().__init__(children)

        self._orchestrator = orchestrator if orchestrator is not None else Parallel.ResumeOrchestrator()
        self._policy = policy if policy is not None else Parallel.SequencePolicy()

        self._no_running_tasks = True
        self._last_result: ta.Optional[bool] = None
        self._current_child_idx = 0

    def run(self) -> None:
        self._orchestrator.execute(self)

    def child_running(self, task: 'Task[E]', reporter: 'Task[E]') -> None:
        self._no_running_tasks = False

    def child_success(self, task: 'Task[E]') -> None:
        self._last_result = self._policy.on_child_success(self)

    def child_fail(self, task: 'Task[E]') -> None:
        self._last_result = self._policy.on_child_fail(self)

    class Orchestrator(lang.Abstract):

        @abc.abstractmethod
        def execute(self, parallel: 'Parallel[E]') -> None:
            raise NotImplementedError

    class ResumeOrchestrator(Orchestrator):

        def execute(self, parallel: 'Parallel[E]') -> None:
            parallel._no_running_tasks = True
            parallel._last_result = None

            for i in range(len(parallel._children)):
                parallel._current_child_idx = i
                child = parallel._children[i]

                if child.status == Task.Status.RUNNING:
                    child.run()
                else:
                    child.control = parallel
                    child.start()
                    if child.check_guard(parallel):
                        child.run()
                    else:
                        child.fail()

                if parallel._last_result is None:
                    parallel.cancel_running_children(
                        parallel._current_child_idx + 1 if parallel._no_running_tasks else 0)
                    if parallel._last_result:
                        parallel.success()
                    else:
                        parallel.fail()
                    return

                parallel.running()

    class JoinOrchestrator(Orchestrator):

        def execute(self, parallel: 'Parallel[E]') -> None:
            parallel._no_running_tasks = True
            parallel._last_result = None

            for i in range(len(parallel._children)):
                parallel._current_child_idx = i
                child = parallel._children[i]

                if child.status == Task.Status.RUNNING:
                    child.run()
                elif child.status in (Task.Status.SUCCEEDED, Task.Status.FAILED):
                    pass
                else:
                    child.control = parallel
                    child.start()
                    if child.check_guard(parallel):
                        child.run()
                    else:
                        child.fail()

                if parallel._last_result is not None:
                    parallel.cancel_running_children(
                        parallel._current_child_idx + 1 if parallel._no_running_tasks else 0)
                    if parallel._last_result:
                        parallel.success()
                    else:
                        parallel.fail()
                    return

            parallel.running()

    class Policy(lang.Abstract):

        @abc.abstractmethod
        def on_child_success(self, parallel: 'Parallel[E]') -> ta.Optional[bool]:
            raise NotImplementedError

        @abc.abstractmethod
        def on_child_fail(self, parallel: 'Parallel[E]') -> ta.Optional[bool]:
            raise NotImplementedError

    class SequencePolicy(Policy):

        def on_child_success(self, parallel: 'Parallel[E]') -> ta.Optional[bool]:
            if isinstance(parallel._orchestrator, Parallel.JoinOrchestrator):
                if parallel._no_running_tasks and parallel._children[-1].status == Task.Status.SUCCEEDED:
                    return True
                else:
                    return None
            else:
                if parallel._no_running_tasks and parallel._current_child_idx == (len(parallel._children) - 1):
                    return True
                else:
                    return None

        def on_child_fail(self, parallel: 'Parallel[E]') -> ta.Optional[bool]:
            return False

    class SelectorPolicy(Policy):

        def on_child_success(self, parallel: 'Parallel[E]') -> ta.Optional[bool]:
            return True

        def on_child_fail(self, parallel: 'Parallel[E]') -> ta.Optional[bool]:
            if parallel._no_running_tasks and parallel._current_child_idx == (len(parallel._children) - 1):
                return False
            else:
                return None


class Selector(SingleRunningChildBranch[E]):

    def child_success(self, task: 'Task[E]') -> None:
        super().child_success(task)
        self.success()

    def child_fail(self, task: 'Task[E]') -> None:
        super().child_fail(task)
        self._current_child_idx += 1
        if self._current_child_idx < len(self._children):
            self.run()
        else:
            self.fail()


class Sequence(SingleRunningChildBranch[E]):

    def child_success(self, task: 'Task[E]') -> None:
        super().child_success(task)
        self._current_child_idx += 1
        if self._current_child_idx < len(self._children):
            self.run()
        else:
            self.success()

    def child_fail(self, task: 'Task[E]') -> None:
        super().child_fail(task)
        self.fail()


class RandomSelector(Selector[E]):

    def start(self) -> None:
        super().start()
        if self._random_children is None:
            self._random_children = list(self._children)


class RandomSequence(Sequence[E]):

    def start(self) -> None:
        super().start()
        if self._random_children is None:
            self._random_children = list(self._children)
