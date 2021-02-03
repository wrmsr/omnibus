import dataclasses as dc

from .types import Conferrer
from .types import SUPER
from .metaclass import Data


def _confer_enum_final(att, sub, sup, bases):
    return sub['abstract'] is dc.MISSING or not sub['abstract']


ENUM_SUPER_CONFERS = {a: SUPER for a in [
    'repr',
    'reorder',
    'eq',
    'allow_setattr',
    'kwonly',
    'slots',
    'aspects',
    'confer',
]}


class Enum(
    Data,
    abstract=True,
    eq=False,
    frozen=True,
    slots=True,
    no_weakref=True,
    confer={
        'abstract': True,
        'frozen': True,
        'confer': {
            'final': Conferrer(_confer_enum_final),
            'frozen': True,
            **ENUM_SUPER_CONFERS,
        },
    },
):
    pass
