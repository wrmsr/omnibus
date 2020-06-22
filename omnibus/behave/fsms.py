"""
TODO:
 - still want dumber fsms (sqla models, buttons lol)
  - optional messaging?
"""
import typing as ta

from .. import lang
from .msgs import Telegram
from .msgs import Telegraph


E = ta.TypeVar('E')
StateT = ta.TypeVar('StateT', bound='State', covariant=True)


class State(ta.Generic[E], lang.Abstract):

    def enter(self, entity: E) -> None:
        pass

    def update(self, entity: E) -> None:
        pass

    def exit(self, entity: E) -> None:
        pass

    def on_message(self, entity: E, telegram: Telegram) -> bool:
        return False


class StateMachine(ta.Generic[E, StateT], Telegraph):

    def __init__(
            self,
            owner: ta.Optional[E] = None,
            *,
            initial: StateT = None,
            global_: StateT = None,
    ) -> None:
        super().__init__()

        self._owner = owner

        self._current = initial
        self._previous: StateT = None
        self._global = global_

    @property
    def owner(self) -> ta.Optional[E]:
        return self._owner

    @property
    def current(self) -> ta.Optional[StateT]:
        return self._current

    @property
    def previous(self) -> ta.Optional[StateT]:
        return self._previous

    @property
    def global_(self) -> ta.Optional[StateT]:
        return self._global

    def update(self) -> None:
        if self._global is not None:
            self._global.update(self._owner)
        if self._current is not None:
            self._current.update(self._owner)

    def change(self, new: StateT) -> None:
        self._previous = self._current
        self._change(new)

    def _change(self, new: StateT) -> None:
        if self._current is not None:
            self._current.exit(self._owner)
        self._current = new
        if self._current is not None:
            self._current.enter(self._owner)

    def revert(self) -> bool:
        if self._previous is None:
            return False
        self.change(self._previous)
        return True

    def is_in(self, state: StateT) -> bool:
        return self._current == state

    def handle_message(self, telegram: Telegram) -> bool:
        if self._current is not None and self._current.on_message(self._owner, telegram):
            return True
        if self._global is not None and self._global.on_message(self._owner, telegram):
            return True
        return False


class StackStateMachine(StateMachine[E, StateT]):

    def __init__(
            self,
            owner: ta.Optional[E] = None,
            *,
            initial: StateT = None,
    ) -> None:
        super().__init__(owner, initial=initial)

        self._stack: ta.List[StateT] = []

    @property
    def previous(self) -> ta.Optional[StateT]:
        return self._stack[-1] if self._stack else None

    def change(self, new: StateT, *, push: bool = True) -> None:
        if push and self._current is not None:
            self._stack.append(self._current)
        self._change(new)

    def revert(self) -> bool:
        if not self._stack:
            return False
        self.change(self._stack.pop(), push=False)
        return True
