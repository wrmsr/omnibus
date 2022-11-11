import random

from . import shared
from .. import fsms
from .. import msgs
from ... import lang


class ElsaState(fsms.State['Elsa'], lang.Sealed, lang.Abstract):
    pass


class DoHouseWorkElsaState(ElsaState):

    def update(self, entity: 'Elsa') -> None:
        msg = ['mopping', 'washing', 'bedmaking'][random.randint(0, 2)]
        print(msg)


class VisitBathroomElsaState(ElsaState):

    def enter(self, entity: 'Elsa') -> None:
        print('visiting bathroom')

    def update(self, entity: 'Elsa') -> None:
        print('using bathroom')
        entity._state_machine.revert()

    def exit(self, entity: 'Elsa') -> None:
        print('done in bathroom')


class CookStewElsaState(ElsaState):

    def enter(self, entity: 'Elsa') -> None:
        if not entity._is_cooking:
            print('starting to cook')
            shared.disp.dispatch(entity, entity, shared.StewReadyMessage(), delay=1.5)
            entity._is_cooking = True

    def update(self, entity: 'Elsa') -> None:
        print('cooking stew')

    def exit(self, entity: 'Elsa') -> None:
        print('serving food')

    def on_message(self, entity: 'Elsa', telegram: msgs.Telegram) -> bool:
        if isinstance(telegram.message, shared.StewReadyMessage):
            print('stew is ready')
            shared.disp.dispatch(entity, entity._bob, shared.StewReadyMessage())
            entity._is_cooking = False
            entity._state_machine.change(DoHouseWorkElsaState())
            return True

        return False


class GlobalElsaState(ElsaState):

    def update(self, entity: 'Elsa') -> None:
        if random.random() < .1 and not isinstance(entity._state_machine.current, VisitBathroomElsaState):
            entity._state_machine.change(VisitBathroomElsaState())

    def on_message(self, entity: 'Elsa', telegram: msgs.Telegram) -> bool:
        if isinstance(telegram.message, shared.HomeMessage):
            print('got home, making stew')
            entity._state_machine.change(CookStewElsaState())
            return True

        return False


class Elsa(msgs.Telegraph):

    def __init__(self) -> None:
        super().__init__()

        self._bob = None

        self._state_machine: fsms.StateMachine[Elsa, ElsaState] = fsms.StateMachine(
            self,
            initial=DoHouseWorkElsaState(),
            global_=GlobalElsaState(),
        )

        self._is_cooking = False

    def handle_message(self, telegram: msgs.Telegram) -> bool:
        self._state_machine.handle_message(telegram)
