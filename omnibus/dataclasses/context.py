import typing as ta

from .. import check
from .. import properties
from .internals import DataclassParams
from .reflect import DataSpec
from .reflect import get_cls_spec
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
    def spec(self) -> DataSpec:
        return get_cls_spec(self._cls)
