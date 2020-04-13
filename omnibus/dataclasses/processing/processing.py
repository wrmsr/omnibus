"""
TODO:
 - storage:
  - can override field getters
 - policies? config policy requires custom getters
"""
import dataclasses as dc
import inspect
import typing as ta

from ... import check
from ... import properties
from ..internals import cmp_fn
from ..internals import hash_action
from ..internals import PARAMS
from ..internals import repr_fn
from ..internals import tuple_str
from ..types import ExtraParams
from ..types import METADATA_ATTR
from .defaulting import Defaulting
from .fields import build_cls_fields
from .storage import Storage
from .types import Aspect
from .types import Context
from .validation import Validation


TypeT = ta.TypeVar('TypeT', bound=type, covariant=True)


class ClassProcessor(ta.Generic[TypeT]):

    def __init__(self, ctx: Context[TypeT]) -> None:
        super().__init__()

        self._ctx = check.isinstance(ctx, Context)

    @property
    def ctx(self) -> Context[TypeT]:
        return self._ctx

    def _install_fields(self) -> None:
        build_cls_fields(self.ctx.cls, install=True)

    def _install_init(self) -> None:
        fctx = FunctionBuildContext(self.ctx)
        ib = InitBuilder(
            fctx,
            self.defaulting.create_init_builder(fctx),
            self.storage.create_init_builder(fctx),
            self.validation.create_init_builder(fctx),
        )
        fn = ib()
        self.ctx.set_new_attribute('__init__', fn)

    def __call__(self) -> None:
        self._install_params()

        self._install_fields()

        if self.ctx.params.init:
            self._install_init()

        self.storage.process()

        self.validation.process()
