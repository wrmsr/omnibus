import typing as ta

from ... import check
from .aspects import Doc
from .aspects import Eq
from .aspects import Fields
from .aspects import Hash
from .aspects import Order
from .aspects import Params
from .aspects import Pickle
from .aspects import PostInitAspect
from .aspects import Repr
from .defaulting import Defaulting
from .init import StandardInit
from .storage import StandardStorage
from .types import Context
from .validation import StandardValidation


TypeT = ta.TypeVar('TypeT', bound=type, covariant=True)


DEFAULT_ASPECTS = {

    Defaulting,
    Doc,
    Eq,
    Fields,
    Hash,
    Order,
    Params,
    Pickle,
    PostInitAspect,
    Repr,
    StandardInit,
    StandardStorage,
    StandardValidation,

}


class Driver(ta.Generic[TypeT]):

    def __init__(self, ctx: Context[TypeT]) -> None:
        super().__init__()

        self._ctx = check.isinstance(ctx, Context)

    @property
    def ctx(self) -> Context[TypeT]:
        return self._ctx

    def __call__(self) -> None:
        for aspects in self.ctx.aspect_plan:
            for aspect in aspects:
                aspect.check()
            for aspect in aspects:
                aspect.process()
