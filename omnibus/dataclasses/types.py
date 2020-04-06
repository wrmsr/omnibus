import dataclasses as dc
import typing as ta

from .. import lang


T = ta.TypeVar('T')

Validator = ta.Callable[..., None]

FieldValidator = ta.Callable[[T], None]
FieldValidation = ta.Callable[[dc.Field], FieldValidator[T]]


DERIVERS_ATTR = '__dataclass_derivers__'
ORIGIN_ATTR = '__dataclass_origin__'
VALIDATORS_ATTR = '__dataclass_validators__'


class SizeMetadata(lang.Marker):
    pass


class ValidateMetadata(lang.Marker):
    pass


class CoerceMetadata(lang.Marker):
    pass


class DeriveMetadata(lang.Marker):
    pass
