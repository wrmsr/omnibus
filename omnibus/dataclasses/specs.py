import dataclasses as dc
import typing as ta
import weakref

from .. import check
from .. import defs
from .. import properties
from .types import Checker
from .types import CHECKERS_ATTR
from .types import Deriver
from .types import DERIVERS_ATTR
from .types import POST_INITS_ATTR
from .types import PostInit
from .types import Validator
from .types import VALIDATORS_ATTR


Field = dc.Field


SPECS_BY_CLS = weakref.WeakKeyDictionary()


class FieldSpec:

    def __init__(self, field: Field) -> None:
        super().__init__()

        self._field = check.isinstance(field, Field)

    @property
    def name(self) -> str:
        return self._field.name

    @property
    def field(self) -> Field:
        return self._field


class DataSpec:

    def __init__(self, cls: type) -> None:
        super().__init__()

        check.arg(dc.is_dataclass(cls))
        self._cls = check.isinstance(cls, type)

    defs.repr('cls')

    @property
    def cls(self) -> type:
        return self._cls

    @properties.cached
    def params(self) -> dc._DataclassParams:
        return check.isinstance(getattr(self._cls, dc._PARAMS), dc._DataclassParams)

    @properties.cached
    def fields(self) -> ta.Sequence[Field]:
        return dc.fields(self._cls)

    @properties.cached
    def fields_by_name(self) -> ta.Mapping[str, Field]:
        return {fld.name: fld for fld in self.fields}

    def _get_merged_mro_attr_list(self, att: str) -> ta.List:
        return [v for c in reversed(self._cls.__mro__) for v in getattr(c, att, [])]

    @properties.cached
    def checkers(self) -> ta.List[Checker]:
        return self._get_merged_mro_attr_list(CHECKERS_ATTR)

    @properties.cached
    def derivers(self) -> ta.List[Deriver]:
        return self._get_merged_mro_attr_list(DERIVERS_ATTR)

    @properties.cached
    def post_inits(self) -> ta.List[PostInit]:
        return self._get_merged_mro_attr_list(POST_INITS_ATTR)

    @properties.cached
    def validators(self) -> ta.List[Validator]:
        return self._get_merged_mro_attr_list(VALIDATORS_ATTR)


def get_spec(cls: type) -> DataSpec:
    try:
        return SPECS_BY_CLS[cls]
    except KeyError:
        spec = SPECS_BY_CLS[cls] = DataSpec(cls)
        return spec
