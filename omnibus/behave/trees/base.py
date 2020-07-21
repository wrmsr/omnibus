import abc
import random
import typing as ta

from ... import check
from ... import lang


E = ta.TypeVar('E')


class Task(ta.Generic[E], lang.Abstract):

    class Status(lang.AutoEnum):
        FRESH = ...
        RUNNING = ...
        FAILED = ...
        SUCCEEDED = ...
        CANCELLED = ...

    def __init__(
            self,
            *,
            tree: ta.Optional['BehaviorTree[E]'] = None,
            guard: ta.Optional['Task[E]'] = None,
    ) -> None:
        super().__init__()

        self._status = Task.Status.FRESH
        self._control: Task[E] = None
        self._tree: 'BehaviorTree[E]' = tree
        self._guard: Task[E] = guard

    @property
    def status(self) -> Status:
        return self._status

    @property
    def control(self) -> ta.Optional['Task[E]']:
        return self._control

    @control.setter
    def control(self, control: 'Task[E]') -> None:
        self._control = control
        self._tree = control.tree

    @property
    def tree(self) -> ta.Optional['BehaviorTree[E]']:
        return self._tree

    @property
    def guard(self) -> ta.Optional['Task[E]']:
        return self._guard

    @guard.setter
    def guard(self, guard: 'Task[E]') -> None:
        self._guard = guard

    def add_child(self, child: 'Task[E]') -> int:
        idx = self._add_child(child)
        self._tree.notify_child_added(self, idx)
        return idx

    @abc.abstractmethod
    def _add_child(self, child: 'Task[E]') -> int:
        raise NotImplementedError

    @abc.abstractproperty
    def num_children(self) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def get_child(self, idx: int) -> 'Task[E]':
        raise NotImplementedError

    @property
    def object(self) -> E:
        return check.not_none(self._tree).object

    def check_guard(self, control: 'Task[E]') -> bool:
        if self._guard is None:
            return True

        if self._guard.check_guard(control):
            return True

        self._guard.control = control.tree.guard_evaluator
        self._guard.start()
        self._guard.run()
        if self._guard.status == Task.Status.SUCCEEDED:
            return True
        elif self._guard.status == Task.Status.FAILED:
            return False
        else:
            raise TypeError(self._guard.status)

    def start(self) -> None:
        pass

    def end(self) -> None:
        pass

    @abc.abstractmethod
    def run(self) -> None:
        raise NotImplementedError

    def running(self) -> None:
        prev = self._status
        self._status = Task.Status.RUNNING
        self._tree.notify_status_updated(self, prev)
        if self._control is not None:
            self._control.child_running(self, self)

    def success(self) -> None:
        prev = self._status
        self._status = Task.Status.SUCCEEDED
        self._tree.notify_status_updated(self, prev)
        self.end()
        if self._control is not None:
            self._control.child_success(self)

    def fail(self) -> None:
        prev = self._status
        self._status = Task.Status.FAILED
        self._tree.notify_status_updated(self, prev)
        self.end()
        if self._control is not None:
            self._control.child_fail(self)

    @abc.abstractmethod
    def child_running(self, task: 'Task[E]', reporter: 'Task[E]') -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def child_success(self, task: 'Task[E]') -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def child_fail(self, task: 'Task[E]') -> None:
        raise NotImplementedError

    def cancel(self) -> None:
        self.cancel_running_children()
        prev = self._status
        self._status = Task.Status.CANCELLED
        self._tree.notify_status_updated(self, prev)
        self.end()

    def cancel_running_children(self, start_idx: int = 0) -> None:
        for i in range(start_idx, self.num_children):
            child = self.get_child(i)
            if child._status == Task.Status.RUNNING:
                child.cancel()


class BehaviorTree(Task[E]):

    def __init__(self, root: Task[E], object: E = None) -> None:
        super().__init__(
            tree=self,
            guard=BehaviorTree.GuardEvaluator(self),
        )

        self._root = root
        self._object = object
        self._guard_evaluator = BehaviorTree.GuardEvaluator(self)
        self._listeners: ta.List[BehaviorTree.Listener[E]] = []

    @property
    def object(self) -> E:
        return self._object

    @object.setter
    def object(self, object: E) -> None:
        self._object = object

    @property
    def guard_evaluator(self) -> 'BehaviorTree.GuardEvaluator[E]':
        return self._guard_evaluator

    def _add_child(self, child: Task[E]) -> None:
        check.none(self._root)
        self._root = child
        return 0

    @property
    def num_children(self) -> int:
        return 1 if self._root is not None else 0

    def get_child(self, idx: int) -> Task[E]:
        if idx == 0 and self._root is not None:
            return self._root
        else:
            raise IndexError(idx)

    def run(self) -> None:
        pass

    def step(self) -> None:
        if self._root.status == Task.Status.RUNNING:
            self._root.run()
        else:
            self._root.control = self
            self._root.start()
            if self._root.check_guard(self):
                self._root.run()
            else:
                self._root.fail()

    def child_running(self, task: Task[E], reporter: Task[E]) -> None:
        self.running()

    def child_success(self, task: Task[E]) -> None:
        self.success()

    def child_fail(self, task: Task[E]) -> None:
        self.fail()

    def add_listener(self, listener: 'Listener[E]') -> None:
        self._listeners.append(listener)

    def remove_listener(self,  listener: 'Listener[E]') -> None:
        self._listeners.remove(listener)

    def remove_listeners(self) -> None:
        self._listeners.clear()

    def notify_status_updated(self, task: Task[E], prev_status: Task.Status) -> None:
        for listener in self._listeners:
            listener.status_updated(task, prev_status)

    def notify_child_added(self,  task: Task[E],  idx: int) -> None:
        for listener in self._listeners:
            listener.child_added(task, idx)

    class GuardEvaluator(Task[E]):

        def __init__(self, tree: 'BehaviorTree[E]') -> None:
            super().__init__()

            self._tree = tree

        def _add_child(self, child: Task[E]) -> None:
            raise NotImplementedError

        @property
        def num_children(self) -> int:
            return 0

        def get_child(self, idx: int) -> Task[E]:
            return None

        def run(self) -> None:
            pass

        def child_running(self, task: Task[E], reporter: Task[E]) -> None:
            pass

        def child_success(self, task: Task[E]) -> None:
            pass

        def child_fail(self, task: Task[E]) -> None:
            pass

    class Listener(ta.Generic[E]):

        def status_updated(self, task: Task[E], prev_status: Task.Status) -> None:
            pass

        def child_added(self, task: Task[E], idx: int) -> None:
            pass


class BranchTask(Task[E], lang.Abstract):

    def __init__(self, children: ta.Sequence[Task[E]] = None) -> None:
        super().__init__()

        self._children = list(children or [])

    def _add_child(self, child: Task[E]) -> int:
        self._children.append(child)
        return len(self._children) - 1

    @property
    def num_children(self) -> int:
        return len(self._children)

    def get_child(self, idx: int) -> Task[E]:
        return self._children[idx]


class Decorator(Task[E], lang.Abstract):

    def __init__(self, child: Task[E] = None) -> None:
        super().__init__()

        self._child = child

    def _add_child(self, child: Task[E]) -> int:
        check.none(self._child)
        self._child = child
        return 0

    @property
    def num_children(self) -> int:
        return 1 if self._child is not None else 0

    def get_child(self, idx: int) -> Task[E]:
        if idx == 0 and self._child is not None:
            return self._child
        else:
            raise IndexError(idx)

    def run(self) -> None:
        if self._child.status == Task.Status.RUNNING:
            self._child.run()
        else:
            self._child.control = self
            self._child.start()
            if self._child.check_guard(self):
                self._child.run()
            else:
                self._child.fail()

    def child_running(self, task: Task[E], reporter: Task[E]) -> None:
        self.running()

    def child_fail(self, task: Task[E]) -> None:
        self.fail()

    def child_success(self, task: Task[E]) -> None:
        self.success()


class LeafTask(Task[E], lang.Abstract):

    @abc.abstractmethod
    def execute(self) -> Task.Status:
        raise NotImplementedError

    def run(self) -> None:
        result = check.not_none(self.execute())
        if result == Task.Status.SUCCEEDED:
            self.success()
        elif result == Task.Status.FAILED:
            self.fail()
        elif result == Task.Status.RUNNING:
            self.running()
        else:
            raise TypeError(result)

    def _add_child(self, child: Task[E]) -> int:
        raise TypeError

    @property
    def num_children(self) -> int:
        return 0

    def get_child(self, idx: int) -> Task[E]:
        raise IndexError(idx)

    def child_running(self, task: Task[E], reporter: Task[E]) -> None:
        pass

    def child_fail(self, task: Task[E]) -> None:
        pass

    def child_success(self, task: Task[E]) -> None:
        pass


class LoopDecorator(Decorator[E], lang.Abstract):

    def __init__(self, child: Task[E] = None) -> None:
        super().__init__(child)

        self._loop = False

    @property
    def condition(self) -> bool:
        return self._loop

    def run(self) -> None:
        self._loop = True
        while self.condition:
            if self._child.status == Task.Status.RUNNING:
                self._child.run()
            else:
                self._child.control = self
                self._child.start()
                if self._child.check_guard(self):
                    self._child.run()
                else:
                    self._child.fail()

    def child_running(self, task: Task[E], reporter: Task[E]) -> None:
        super().child_running(task, reporter)
        self._loop = False


class SingleRunningChildBranch(BranchTask[E], lang.Abstract):

    def __init__(self, children: ta.Sequence[Task[E]] = None) -> None:
        super().__init__(children)

        self._running_child: ta.Optional[Task[E]] = None
        self._current_child_idx: int = 0
        self._random_children: ta.Optional[ta.List[Task[E]]] = None

    def child_running(self, task: Task[E], reporter: Task[E]) -> None:
        self._running_child = task
        self.running()

    def child_success(self, task: Task[E]) -> None:
        self._running_child = None

    def child_fail(self, task: Task[E]) -> None:
        self._running_child = None

    def run(self) -> None:
        if self._running_child is not None:
            self._running_child.run()
        else:
            if self._current_child_idx < len(self._children):
                if self._random_children is not None:
                    last = len(self._children) - 1
                    if self._current_child_idx < last:
                        other_child_idx = random.randint(0, last)
                        tmp = self._random_children[self._current_child_idx]
                        self._random_children[self._current_child_idx] = self._random_children[other_child_idx]
                        self._random_children[other_child_idx] = tmp
                    self._running_child = self._random_children[self._current_child_idx]
                else:
                    self._running_child = self._children[self._current_child_idx]
                self._running_child.control = self
                self._running_child.start()
                if not self._running_child.check_guard(self):
                    self._running_child.fail()
                else:
                    self._running_child.run()

    def start(self) -> None:
        self._current_child_idx = 0
        self._running_child = None

    def cancel_running_children(self, start_idx: int = 0) -> None:
        super().cancel_running_children(start_idx)
        self._running_child = None
