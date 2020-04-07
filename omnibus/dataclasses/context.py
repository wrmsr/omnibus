import sys
import typing as ta

from .. import check
from .. import properties
from .defdecls import ClsDefdecls
from .defdecls import get_cls_defdecls
from .internals import DataclassParams
from .internals import FIELDS
from .types import METADATA_ATTR
from .types import ExtraParams


TypeT = ta.TypeVar('TypeT', bound=type, covariant=True)


class BuildContext(ta.Generic[TypeT]):

    def __init__(
            self,
            cls: TypeT,
            params: DataclassParams,
            extra_params: ExtraParams = ExtraParams(),
    ) -> None:
        super().__init__()

        self._cls = check.isinstance(cls, type)
        self._params = check.isinstance(params, DataclassParams)
        self._extra_params = check.isinstance(extra_params, ExtraParams)

    @property
    def cls(self) -> TypeT:
        return self._cls

    @property
    def params(self) -> DataclassParams:
        return self._params

    @property
    def extra_params(self) -> ExtraParams:
        return self._extra_params

    @properties.cached
    def metadata(self) -> ta.Mapping[type, ta.Any]:
        return self.cls.__dict__.get(METADATA_ATTR, {})

    @properties.cached
    def defdecls(self) -> ClsDefdecls:
        return get_cls_defdecls(self.cls)

    @property
    def rmro(self) -> ta.Iterable[type]:
        return self.cls.__mro__[-1:0:-1]

    @properties.cached
    def dc_rmro(self) -> ta.List[type]:
        return [b for b in self.rmro if getattr(b, FIELDS, None)]

    @properties.cached
    def globals(self) -> ta.MutableMapping[str, ta.Any]:
        if self.cls.__module__ in sys.modules:
            return sys.modules[self.cls.__module__].__dict__
        else:
            return {}
