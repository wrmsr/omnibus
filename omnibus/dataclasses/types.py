import dataclasses as dc
import typing as ta

from .. import lang


T = ta.TypeVar('T')

Checker = ta.Callable[..., bool]
Deriver = ta.Callable[..., T]
PostInit = ta.Callable[[T], None]
Validator = ta.Callable[..., None]

FieldValidator = ta.Callable[[T], None]
FieldValidation = ta.Callable[[dc.Field], FieldValidator[T]]


CHECKERS_ATTR = '__dataclass_checkers__'
DERIVERS_ATTR = '__dataclass_derivers__'
POST_INITS_ATTR = '__dataclass_post_inits__'
VALIDATORS_ATTR = '__dataclass_validators__'

ORIGIN_ATTR = '__dataclass_origin__'


class CoerceMetadata(lang.Marker):
    pass


class DeriveMetadata(lang.Marker):
    pass


class DocMetadata(lang.Marker):
    pass


class SizeMetadata(lang.Marker):
    pass


class ValidateMetadata(lang.Marker):
    pass


@dc.dataclass(frozen=True)
class CheckException(Exception):
    values: ta.Dict[str, ta.Any]
    checker: Checker
