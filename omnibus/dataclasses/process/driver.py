import typing as ta

from ... import check
from .bootstrap import Fields
from .bootstrap import FixVarAnnotations
from .bootstrap import Params
from .bootstrap import Slots
from .defaulting import Defaulting
from .init import StandardInit
from .simple import Doc
from .simple import Eq
from .simple import Frozen
from .simple import Hash
from .simple import Order
from .simple import Pickle
from .simple import Placeholders
from .simple import PostInitAspect
from .simple import Repr
from .storage import StandardStorage
from .types import Aspect
from .types import Aspectable
from .types import Context
from .validation import StandardValidation


TypeT = ta.TypeVar('TypeT', bound=type, covariant=True)


DEFAULT_ASPECTS = {

    Defaulting,
    Doc,
    Eq,
    Fields,
    FixVarAnnotations,
    Frozen,
    Hash,
    Order,
    Params,
    Pickle,
    Placeholders,
    PostInitAspect,
    Repr,
    Slots,
    StandardInit,
    StandardStorage,
    StandardValidation,

}


def replace_aspects(
        replacements_by_cls: ta.Mapping[ta.Type[Aspect], Aspectable],
        aspects: ta.Iterable[Aspectable] = DEFAULT_ASPECTS,  # noqa
) -> ta.Sequence[Aspectable]:
    da = []
    for a in aspects:
        for rc, rv in replacements_by_cls.items():
            if (isinstance(a, type) and issubclass(a, rc)) or (isinstance(a, Aspect) and issubclass(type(a), rc)):
                a = rv
        da.append(a)
    return da


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
