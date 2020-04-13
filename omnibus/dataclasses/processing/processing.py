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
from .context import BuildContext
from .context import FunctionBuildContext
from .defaulting import Defaulting
from .fields import build_cls_fields
from .init import InitBuilder
from .storage import Storage
from .validation import Validation


TypeT = ta.TypeVar('TypeT', bound=type, covariant=True)


class ClassProcessor(ta.Generic[TypeT]):

    def __init__(self, ctx: BuildContext[TypeT]) -> None:
        super().__init__()

        self._ctx = check.isinstance(ctx, BuildContext)

    @property
    def ctx(self) -> BuildContext:
        return self._ctx

    @properties.cached
    def defaulting(self) -> Defaulting:
        return Defaulting(self.ctx)

    @properties.cached
    def storage(self) -> Storage:
        return Storage(self.ctx)

    @properties.cached
    def validation(self) -> Validation:
        return Validation(self.ctx)

    def _install_params(self) -> None:
        self.ctx.set_new_attribute(PARAMS, self.ctx.params)
        check.state(self.ctx.spec.params is self.ctx.params)

        if METADATA_ATTR in self.ctx.cls.__dict__:
            md = getattr(self.ctx.cls, METADATA_ATTR)
        else:
            md = {}
            self.ctx.set_new_attribute(METADATA_ATTR, md)
        check.state(self.ctx.spec._metadata is md)

        md[ExtraParams] = self.ctx.extra_params

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
