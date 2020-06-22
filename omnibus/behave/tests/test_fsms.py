import time

from . import bob
from . import elsa
from . import shared


def test_fsms():
    b = bob.Bob()
    e = elsa.Elsa()
    b._elsa = e
    e._bob = b

    for _ in range(60):
        b._state_machine.update()
        e._state_machine.update()
        shared.disp.update()
        time.sleep(0.05)
