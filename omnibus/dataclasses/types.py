import dataclasses as dc
import typing as ta

from .. import check
from .. import lang
from .internals import DataclassParams
from .internals import FIELDS


T = ta.TypeVar('T')

FieldValidator = ta.Callable[[T], None]
FieldValidation = ta.Callable[[dc.Field], FieldValidator[T]]

NONE_TYPE = type(None)
MISSING_TYPE = type(dc.MISSING)


class SUPER(lang.Marker):
    pass


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
class ExtraFieldParams(lang.Final):
    doc: ta.Optional[str] = None
    size: ta.Optional[ta.Any] = None
    coerce: ta.Optional[ta.Union[bool, ta.Callable[[ta.Any], ta.Any]]] = None
    derive: ta.Optional[ta.Callable[..., ta.Any]] = None
    check: ta.Optional[ta.Union[bool, ta.Callable[[ta.Any], bool]]] = None
    validate: ta.Optional[ta.Union[bool, ta.Callable[[ta.Any], None]]] = None

    def __post_init__(self) -> None:
        check.isinstance(self.doc, (str, NONE_TYPE, MISSING_TYPE))
        check.isinstance(self.coerce, (bool, lang.Callable, NONE_TYPE, MISSING_TYPE))
        check.isinstance(self.derive, (lang.Callable, NONE_TYPE, MISSING_TYPE))
        check.isinstance(self.check, (bool, lang.Callable, NONE_TYPE, MISSING_TYPE))
        check.isinstance(self.validate, (bool, lang.Callable, NONE_TYPE, MISSING_TYPE))


PARAMS_CONFER_DEFAULTS = dict(
    init=True,
    repr=True,
    eq=True,
    order=False,
    unsafe_hash=False,
    frozen=False,
)


@dc.dataclass(frozen=True)
class ExtraParams(lang.Final):
    validate: ta.Optional[bool] = None
    field_attrs: bool = False
    cache_hash: bool = False
    pickle: bool = False
    reorder: bool = False
    aspects: ta.Optional[ta.Collection[ta.Any]] = None
    confer: ta.Optional[ta.Union[ta.Collection[str], ta.Mapping[str, ta.Any]]] = None

    original_params: ta.Optional[DataclassParams] = None
    original_extra_params: ta.Optional['ExtraParams'] = None

    def __post_init__(self) -> None:
        check.isinstance(self.validate, (bool, NONE_TYPE, MISSING_TYPE))
        check.isinstance(self.field_attrs, (bool, MISSING_TYPE))
        check.isinstance(self.cache_hash, (bool, MISSING_TYPE))
        check.isinstance(self.pickle, (bool, MISSING_TYPE))
        check.isinstance(self.reorder, (bool, MISSING_TYPE))
        check.isinstance(self.aspects, (ta.Collection, NONE_TYPE, MISSING_TYPE))
        check.isinstance(self.confer, (ta.Collection, ta.Mapping, NONE_TYPE, MISSING_TYPE))

        check.isinstance(self.original_params, (DataclassParams, NONE_TYPE, MISSING_TYPE))
        check.isinstance(self.original_extra_params, (ExtraParams, NONE_TYPE, MISSING_TYPE))

        if self.confer is not dc.MISSING and self.confer is not None:
            check.arg(not isinstance(self.confer, str))
            check.empty(set(self.confer) - CONFERS)


EXTRA_PARAMS_CONFER_DEFAULTS = {
    fld.name: fld.default
    for fld in getattr(ExtraParams, FIELDS).values()
    if fld.name not in {'original_params', 'original_extra_params'}
}


@dc.dataclass(frozen=True)
class MetaclassParams(lang.Final):
    slots: bool = False
    abstract: bool = False
    final: bool = False
    sealed: bool = False

    def __post_init__(self) -> None:
        check.isinstance(self.slots, (bool, MISSING_TYPE))
        check.isinstance(self.abstract, (bool, MISSING_TYPE))
        check.isinstance(self.final, (bool, MISSING_TYPE))
        check.isinstance(self.sealed, (bool, MISSING_TYPE))


METACLASS_PARAMS_CONFER_DEFAULTS = {
    fld.name: fld.default
    for fld in getattr(MetaclassParams, FIELDS).values()
}


CONFERS = set(check.unique([a for l in [
    PARAMS_CONFER_DEFAULTS,
    EXTRA_PARAMS_CONFER_DEFAULTS,
    METACLASS_PARAMS_CONFER_DEFAULTS,
] for a in l]))


@dc.dataclass(frozen=True)
class Original(ta.Generic[T], lang.Final):
    type: ta.Type[T]
