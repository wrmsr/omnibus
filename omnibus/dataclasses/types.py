import dataclasses as dc
import typing as ta


T = ta.TypeVar('T')

Checker = ta.Callable[..., bool]
Deriver = ta.Callable[..., T]
PostInit = ta.Callable[[T], None]
Validator = ta.NewType('Validator', ta.Callable[..., None])

FieldValidator = ta.Callable[[T], None]
FieldValidation = ta.Callable[[dc.Field], FieldValidator[T]]


METADATA_ATTR = '__dataclass_metadata__'


@dc.dataclass(frozen=True)
class CheckException(Exception):
    values: ta.Dict[str, ta.Any]
    checker: Checker


@dc.dataclass(frozen=True)
class ExtraFieldParams:
    coerce: ta.Union[bool, ta.Callable] = None
    derive: ta.Callable = None
    doc: str = None
    size: ta.Any = None
    validate: ta.Union[bool, ta.Callable] = None


@dc.dataclass(frozen=True)
class ExtraParams:
    validate: bool = None
    field_attrs: bool = False


@dc.dataclass(frozen=True)
class MetaParams:
    slots: bool = False
    abstract: bool = False
    final: bool = False
    sealed: bool = False
    pickle: bool = False
    reorder: bool = False
