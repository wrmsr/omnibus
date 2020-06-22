from . import shared
from .. import fsms
from .. import msgs
from ... import lang


class Location(lang.AutoEnum):
    SHACK = ...
    GOLD_MINE = ...
    BANK = ...
    SALOON = ...


class BobState(fsms.State['Bob'], lang.Sealed, lang.Abstract):
    pass


class EnterMineAndDigBobState(BobState):

    def enter(self, entity: 'Bob') -> None:
        if entity._location != Location.GOLD_MINE:
            print('walking to mine')
            entity._location = Location.GOLD_MINE

    def update(self, entity: 'Bob') -> None:
        print('mining')

        entity._gold_carried += 1
        entity._fatigue += 1

        if entity._gold_carried >= Bob.MAX_NUGGETS:
            entity._state_machine.change(VisitBankBobState())

        if entity._thirst >= Bob.THIRST_LEVEL:
            entity._state_machine.change(QuenchThirstBobState())

    def exit(self, entity: 'Bob') -> None:
        print('leaving mine')


class GoHomeAndSleepBobState(BobState):

    def enter(self, entity: 'Bob') -> None:
        if entity._location != Location.SHACK:
            print('walking home')
            entity._location = Location.SHACK
            shared.disp.dispatch(entity, entity._elsa, shared.HomeMessage())

    def update(self, entity: 'Bob') -> None:
        if entity._fatigue < Bob.TIREDNESS_THRESHOLD:
            print('rested')
            entity._state_machine.change(EnterMineAndDigBobState())

        else:
            entity._fatigue -= 1
            print('resting')

    def on_message(self, entity: 'Bob', telegram: msgs.Telegram) -> bool:
        if isinstance(telegram.message, shared.StewReadyMessage):
            print('going to eat')
            entity._state_machine.change(EatStewBobState())
            return True

        return False


class QuenchThirstBobState(BobState):

    def enter(self, entity: 'Bob') -> None:
        if entity._location != Location.SALOON:
            print('going to saloon')
            entity._location = Location.SALOON

    def update(self, entity: 'Bob') -> None:
        print('drinking')
        entity._money_in_bank -= 2
        entity._thirst = 0
        entity._state_machine.change(EnterMineAndDigBobState())

    def exit(self, entity: 'Bob') -> None:
        print('leaving saloon')


class VisitBankBobState(BobState):

    def enter(self, entity: 'Bob') -> None:
        if entity._location != Location.BANK:
            print('going to bank')
            entity._location = Location.BANK

    def update(self, entity: 'Bob') -> None:
        print('depositing')
        entity._money_in_bank += entity._gold_carried
        entity._gold_carried = 0
        print(f'money in bank: {entity._money_in_bank}')

        if entity._money_in_bank >= Bob.COMFORT_LEVEL:
            print('comfortable')
            entity._state_machine.change(GoHomeAndSleepBobState())
        else:
            entity._state_machine.change(EnterMineAndDigBobState())

    def exit(self, entity: 'Bob') -> None:
        print('leaving bank')


class EatStewBobState(BobState):

    def enter(self, entity: 'Bob') -> None:
        print('beginning to eat stew')

    def update(self, entity: 'Bob') -> None:
        print('eating stew')
        entity._state_machine.revert()

    def exit(self, entity: 'Bob') -> None:
        print('done eating stew')


class Bob(msgs.Telegraph):

    COMFORT_LEVEL = 5
    MAX_NUGGETS = 3
    THIRST_LEVEL = 5
    TIREDNESS_THRESHOLD = 5

    def __init__(self) -> None:
        super().__init__()

        self._elsa = None

        self._location = Location.SHACK
        self._gold_carried = 0
        self._money_in_bank = 0
        self._thirst = 0
        self._fatigue = 0

        self._state_machine: fsms.StateMachine[Bob, BobState] = fsms.StateMachine(
            self,
            initial=GoHomeAndSleepBobState(),
        )

        self._is_cooking = False

    def handle_message(self, telegram: msgs.Telegram) -> bool:
        self._state_machine.handle_message(telegram)
