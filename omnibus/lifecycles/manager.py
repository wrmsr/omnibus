import logging
import types
import typing as ta

from .. import check
from .. import collections as ocol
from .. import dataclasses as dc
from .. import lang
from .abstract import AbstractLifecycle
from .controller import LifecycleController
from .types import Lifecycle
from .types import LifecycleState
from .types import LifecycleStateException
from .types import LifecycleStates


log = logging.getLogger(__name__)


class LifecycleManager(AbstractLifecycle):

    @dc.dataclass(frozen=True)
    class Entry:
        controller: LifecycleController
        dependencies: ta.Set['LifecycleManager.Entry'] = dc.field(default_factory=ocol.IdentitySet)
        dependents: ta.Set['LifecycleManager.Entry'] = dc.field(default_factory=ocol.IdentitySet)

    def __init__(
            self,
            *,
            lock: lang.DefaultLockable = None,
    ) -> None:
        super().__init__()

        self._lock = lang.default_lock(lock, True)

        self._entries_by_lifecycle: ta.MutableMapping[Lifecycle, LifecycleManager.Entry] = ocol.IdentityKeyDict()

    @property
    def controller(self) -> 'LifecycleController[lang.Self]':
        return self.lifecycle_controller

    @property
    def state(self) -> LifecycleState:
        return self.lifecycle_controller.state

    @staticmethod
    def _get_controller(lifecycle: Lifecycle) -> LifecycleController:
        if isinstance(lifecycle, LifecycleController):
            return lifecycle
        elif isinstance(lifecycle, AbstractLifecycle):
            return lifecycle.lifecycle_controller
        elif isinstance(lifecycle, Lifecycle):
            return LifecycleController(lifecycle)
        else:
            raise TypeError(lifecycle)

    def _add_internal(self, lifecycle: Lifecycle, dependencies: ta.Iterable[Lifecycle]) -> Entry:
        check.state(self.state.phase < LifecycleStates.STOPPING.phase and not self.state.is_failed)

        check.isinstance(lifecycle, Lifecycle)
        try:
            entry = self._entries_by_lifecycle[lifecycle]
        except KeyError:
            controller = self._get_controller(lifecycle)
            entry = self._entries_by_lifecycle[lifecycle] = LifecycleManager.Entry(controller)

        for dep in dependencies:
            check.isinstance(dep, Lifecycle)
            dep_entry = self._add_internal(dep, [])
            entry.dependencies.add(dep_entry)
            dep_entry.dependents.add(entry)

        return entry

    def add(
            self,
            lifecycle: Lifecycle,
            dependencies: ta.Iterable[Lifecycle] = (),
    ) -> Entry:
        with self._lock:
            return self._add_internal(lifecycle, dependencies)

    def construct(self) -> None:
        self.lifecycle_construct()

    def _do_lifecycle_construct(self) -> None:
        def rec(entry: LifecycleManager.Entry) -> None:
            for dep in entry.dependencies:
                rec(dep)
            if entry.controller.state.is_failed:
                raise LifecycleStateException(entry.controller)
            if entry.controller.state.phase < LifecycleStates.CONSTRUCTED.phase:
                entry.controller.lifecycle_construct()
        for entry in self._entries_by_lifecycle.values():
            rec(entry)

    def start(self) -> None:
        self.lifecycle_start()

    def _do_lifecycle_start(self) -> None:
        def rec(entry: LifecycleManager.Entry) -> None:
            for dep in entry.dependencies:
                rec(dep)
            if entry.controller.state.is_failed:
                raise LifecycleStateException(entry.controller)
            if entry.controller.state.phase < LifecycleStates.CONSTRUCTED.phase:
                entry.controller.lifecycle_construct()
            if entry.controller.state.phase < LifecycleStates.STARTED.phase:
                entry.controller.lifecycle_start()
        for entry in self._entries_by_lifecycle.values():
            rec(entry)

    def stop(self) -> None:
        self.lifecycle_stop()

    def _do_lifecycle_stop(self) -> None:
        def rec(entry: LifecycleManager.Entry) -> None:
            for dep in entry.dependents:
                rec(dep)
            if entry.controller.state.is_failed:
                raise LifecycleStateException(entry.controller)
            if entry.controller.state is LifecycleStates.STARTED:
                entry.controller.lifecycle_stop()
        for entry in self._entries_by_lifecycle.values():
            rec(entry)

    def destroy(self) -> None:
        self.lifecycle_destroy()

    def _do_lifecycle_destroy(self) -> None:
        def rec(entry: LifecycleManager.Entry) -> None:
            for dep in entry.dependents:
                rec(dep)
            if entry.controller.state.phase < LifecycleStates.DESTROYED.phase:
                entry.controller.lifecycle_destroy()
        for entry in self._entries_by_lifecycle.values():
            rec(entry)


class LifecycleContextManager:

    def __init__(self, **kwargs) -> None:
        super().__init__()

        self._manager = LifecycleManager(**kwargs)

    @property
    def manager(self) -> LifecycleManager:
        return self._manager

    def add(
            self: lang.Self,
            lifecycle: Lifecycle,
            dependencies: ta.Iterable[Lifecycle] = (),
    ) -> lang.Self:
        self._manager.add(lifecycle, dependencies)
        return self

    def __enter__(self: lang.Self) -> lang.Self:
        try:
            self._manager.construct()
            self._manager.start()
        except Exception:
            self._manager.destroy()
            raise
        return self

    def __exit__(
            self,
            exc_type: ta.Optional[ta.Type[Exception]],
            exc_val: ta.Optional[Exception],
            exc_tb: ta.Optional[types.TracebackType],
    ) -> ta.Optional[bool]:
        try:
            if self._manager.state is LifecycleStates.STARTED:
                self._manager.stop()
        except Exception:
            log.exception('Error stopping')
            self._manager.destroy()
            raise
        else:
            self._manager.destroy()
        return None


def context_manager(
        *lifecycles: Lifecycle,
        lock: lang.DefaultLockable = None,
) -> LifecycleContextManager:
    lcm = LifecycleContextManager(lock=lock)
    for lc in lifecycles:
        lcm.add(lc)
    return lcm


class ContextManageableLifecycle(AbstractLifecycle, lang.Abstract):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._lifecycle_context_manager = LifecycleContextManager()
        self._lifecycle_context_manager.add(self)

    def __enter__(self: lang.Self) -> lang.Self:
        self._lifecycle_context_manager.__enter__()
        return self

    def __exit__(
            self,
            exc_type: ta.Optional[ta.Type[Exception]],
            exc_val: ta.Optional[Exception],
            exc_tb: ta.Optional[types.TracebackType]
    ) -> ta.Optional[bool]:
        return self._lifecycle_context_manager.__exit__(exc_type, exc_val, exc_tb)
