"""
TODO:
 - storage:
  - can override field getters
 - policies? config policy requires custom getters
"""
import typing as ta

from ... import check
from .aspects import Doc
from .aspects import Eq
from .aspects import FieldAttrs
from .aspects import Fields
from .aspects import Frozen
from .aspects import Hash
from .aspects import Order
from .aspects import Params
from .aspects import PostInitAspect
from .aspects import Repr
from .defaulting import Defaulting
from .init import Init
from .storage import Storage
from .types import Context
from .validation import Validation


TypeT = ta.TypeVar('TypeT', bound=type, covariant=True)


DEFAULT_ASPECTS = {

    Defaulting,
    Doc,
    Eq,
    FieldAttrs,
    Fields,
    Frozen,
    Hash,
    Init,
    Order,
    Params,
    PostInitAspect,
    Repr,
    Storage,
    Validation,

}


class Driver(ta.Generic[TypeT]):

    def __init__(self, ctx: Context[TypeT]) -> None:
        super().__init__()

        self._ctx = check.isinstance(ctx, Context)

    @property
    def ctx(self) -> Context[TypeT]:
        return self._ctx

    def __call__(self) -> None:
        for phase, aspects in sorted(self.ctx.aspect_lists_by_phase.items(), key=lambda t: t[0].value):
            for aspect in aspects:
                aspect.check()
            for aspect in aspects:
                aspect.process()
