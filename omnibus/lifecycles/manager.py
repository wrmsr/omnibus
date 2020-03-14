import typing as ta

from .. import check
from .. import collections as ocol
from .. import dataclasses as dc
from .. import lang
from .controller import LifecycleController
from .types import AbstractLifecycle
from .types import Lifecycle
from .types import LifecycleState
from .types import LifecycleStates



lang.warn_unstable()


T = ta.TypeVar('T')
LifecycleT = ta.TypeVar('LifecycleT', bound='Lifecycle')
LifecycleCallback = ta.Callable[[LifecycleT], None]


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

        # FIXME: reverse for stop/destroy
        controller = entry.controller
        check.state(controller.state.phase < LifecycleStates.STOPPING.phase and not controller.state.is_failed)
        while controller.state.phase < self.state.phase:
            check.state(not controller.state.is_failed)
            if controller.state is LifecycleStates.NEW:
                controller.lifecycle_construct()
            elif controller.state is LifecycleStates.CONSTRUCTED:
                controller.lifecycle_start()
            else:
                raise ValueError(controller.state)

        return entry

    def add(
            self,
            lifecycle: Lifecycle,
            dependencies: ta.Iterable[Lifecycle] = (),
    ) -> Entry:
        with self._lock:
            return self._add_internal(lifecycle, dependencies)

    @property
    def controller(self) -> 'LifecycleController[lang.Self]':
        return self.lifecycle_controller

    @property
    def state(self) -> LifecycleState:
        return self.lifecycle_controller.state

    def construct(self) -> None:
        self.lifecycle_construct()

    def _do_lifecycle_construct(self) -> None:
        for entry in self._entries_by_lifecycle.values():
            entry.controller.lifecycle_construct()

    def start(self) -> None:
        self.lifecycle_start()

    def _do_lifecycle_start(self) -> None:
        for entry in self._entries_by_lifecycle.values():
            entry.controller.lifecycle_start()

    def stop(self) -> None:
        self.lifecycle_stop()

    def _do_lifecycle_stop(self) -> None:
        for entry in self._entries_by_lifecycle.values():
            entry.controller.lifecycle_stop()

    def destroy(self) -> None:
        self.lifecycle_destroy()

    def _do_lifecycle_destroy(self) -> None:
        for entry in self._entries_by_lifecycle.values():
            entry.controller.lifecycle_destroy()
