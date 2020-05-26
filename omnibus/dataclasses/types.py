import dataclasses as dc
import typing as ta

from .. import check
from .. import lang
from .internals import DataclassParams
from .internals import FIELDS


T = ta.TypeVar('T')

FieldValidator = ta.Callable[[T], None]
FieldValidation = ta.Callable[[dc.Field], FieldValidator[T]]


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
    aspects: ta.Optional[ta.Sequence[ta.Any]] = None
    confer: ta.Union[None, ta.Sequence[str], ta.Mapping[str, ta.Any]] = None

    original_params: ta.Optional[DataclassParams] = None
    original_extra_params: ta.Optional['ExtraParams'] = None

    def __post_init__(self) -> None:
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
    inner: bool = False


METACLASS_PARAMS_CONFER_DEFAULTS = {
    fld.name: fld.default
    for fld in getattr(MetaclassParams, FIELDS).values()
}


CONFERS = set(check.unique([a for l in [
    PARAMS_CONFER_DEFAULTS,
    EXTRA_PARAMS_CONFER_DEFAULTS,
    METACLASS_PARAMS_CONFER_DEFAULTS,
] for a in l]))
