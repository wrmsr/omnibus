import dataclasses as dc
import typing as ta

from .. import lang


T = ta.TypeVar('T')

FieldValidator = ta.Callable[[T], None]
FieldValidation = ta.Callable[[dc.Field], FieldValidator[T]]


METADATA_ATTR = '__dataclass_metadata__'


class Extras(lang.Marker):
    pass


@dc.dataclass(frozen=True)
class Checker(lang.Final):
    fn: ta.Callable[..., bool]


@dc.dataclass(frozen=True)
class Deriver(lang.Final):
    attrs: ta.Union[str, ta.Iterable[str]]
    fn: ta.Callable[..., T]


@dc.dataclass(frozen=True)
class PostInit(lang.Final):
    fn: ta.Callable[[T], None]


@dc.dataclass(frozen=True)
class Validator(lang.Final):
    fn: ta.Callable[..., None]


@dc.dataclass(frozen=True)
class SelfChecker(lang.Final):
    fn: ta.Callable[[ta.Any], bool]


@dc.dataclass(frozen=True)
class SelfValidator(lang.Final):
    fn: ta.Callable[[ta.Any], None]


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
