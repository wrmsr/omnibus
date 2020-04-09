import typing as ta

from ... import check
from ... import codegen
from ... import properties
from ..internals import DataclassParams
from ..reflect import DataSpec
from ..reflect import get_cls_spec
from ..types import ExtraParams


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

    def set_new_attribute(self, name: str, value: ta.Any) -> bool:
        if name in self.cls.__dict__:
            return True
        setattr(self.cls, name, value)
        return False


class FunctionBuildContext:

    def __init__(self, ctx: BuildContext) -> None:
        super().__init__()

        self._ctx = check.isinstance(ctx, BuildContext)

        self._nsb = codegen.NamespaceBuilder(codegen.name_generator(unavailable_names=ctx.spec.fields.by_name))

    @property
    def ctx(self) -> BuildContext:
        return self._ctx

    @property
    def nsb(self) -> codegen.NamespaceBuilder:
        return self._nsb

    @properties.cached
    def self_name(self) -> str:
        return self._nsb.put('self', None)
