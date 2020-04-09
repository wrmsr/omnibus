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
from ..fields import build_cls_fields
from ..fields import Fields
from ..internals import cmp_fn
from ..internals import hash_action
from ..internals import PARAMS
from ..internals import repr_fn
from ..internals import tuple_str
from ..types import ExtraParams
from ..types import METADATA_ATTR
from .context import BuildContext
from .context import FunctionBuildContext
from .init import InitBuilder
from .storage import Storage
from .validation import Validation


T = ta.TypeVar('T')
TypeT = ta.TypeVar('TypeT', bound=type, covariant=True)


class ClassProcessor(ta.Generic[TypeT]):

    def __init__(self, ctx: BuildContext[TypeT]) -> None:
        super().__init__()

        self._ctx = check.isinstance(ctx, BuildContext)

        self.check_invariants()

    @property
    def ctx(self) -> BuildContext:
        return self._ctx

    @properties.cached
    def storage(self) -> Storage:
        return Storage(self.ctx)

    @properties.cached
    def validation(self) -> Validation:
        return Validation(self.ctx)

    def check_invariants(self) -> None:
        if self.ctx.params.order and not self.ctx.params.eq:
            raise ValueError('eq must be true if order is true')

        any_frozen_base = any(getattr(b, PARAMS).frozen for b in self.ctx.spec.rmro if dc.is_dataclass(b))
        if any_frozen_base:
            if any_frozen_base and not self.ctx.params.frozen:
                raise TypeError('cannot inherit non-frozen dataclass from a frozen one')
            if not any_frozen_base and self.ctx.params.frozen:
                raise TypeError('cannot inherit frozen dataclass from a non-frozen one')

    def install_params(self) -> None:
        self.ctx.set_new_attribute(PARAMS, self.ctx.params)
        check.state(self.ctx.spec.params is self.ctx.params)

        if METADATA_ATTR in self.ctx.cls.__dict__:
            md = getattr(self.ctx.cls, METADATA_ATTR)
        else:
            md = {}
            self.ctx.set_new_attribute(METADATA_ATTR, md)
        check.state(self.ctx.spec._metadata is md)

        md[ExtraParams] = self.ctx.extra_params

    @properties.cached
    def fields(self) -> Fields:
        return build_cls_fields(self.ctx.cls, install=True)

    def install_fields(self) -> None:
        check.not_none(self.fields)

    def install_init(self) -> None:
        fctx = FunctionBuildContext(self.ctx)
        ib = InitBuilder(
            fctx,
            self.storage.create_init_builder(fctx),
            self.validation.create_init_builder(fctx),
        )
        fn = ib()
        self.ctx.set_new_attribute('__init__', fn)

    def install_repr(self) -> None:
        flds = [f for f in self.fields.instance if f.repr]
        self.ctx.set_new_attribute('__repr__', repr_fn(flds, self.ctx.spec.globals))

    def install_eq(self) -> None:
        flds = [f for f in self.fields.instance if f.compare]
        self_tuple = tuple_str('self', flds)
        other_tuple = tuple_str('other', flds)
        self.ctx.set_new_attribute(
            '__eq__',
            cmp_fn(
                '__eq__',
                '==',
                self_tuple,
                other_tuple,
                globals=self.ctx.spec.globals,
            )
        )

    def install_order(self) -> None:
        flds = [f for f in self.fields.instance if f.compare]
        self_tuple = tuple_str('self', flds)
        other_tuple = tuple_str('other', flds)
        for name, op in [
            ('__lt__', '<'),
            ('__le__', '<='),
            ('__gt__', '>'),
            ('__ge__', '>='),
        ]:
            if self.ctx.set_new_attribute(
                    name,
                    cmp_fn(
                        name,
                        op,
                        self_tuple,
                        other_tuple,
                        globals=self.ctx.spec.globals,
                    )
            ):
                raise TypeError(
                    f'Cannot overwrite attribute {name} in class {self.ctx.cls.__name__}. '
                    f'Consider using functools.total_ordering')

    def maybe_install_hash(self) -> bool:
        # Was this class defined with an explicit __hash__?  Note that if __eq__ is defined in this class, then python
        # will automatically set __hash__ to None.  This is a heuristic, as it's possible that such a __hash__ == None
        # was not auto-generated, but it close enough.
        class_hash = self.ctx.cls.__dict__.get('__hash__', dc.MISSING)
        has_explicit_hash = not (class_hash is dc.MISSING or (class_hash is None and '__eq__' in self.ctx.cls.__dict__))
        ha = hash_action[(
            bool(self.ctx.params.unsafe_hash),
            bool(self.ctx.params.eq),
            bool(self.ctx.params.frozen),
            has_explicit_hash,
        )]
        if ha:
            self.ctx.cls.__hash__ = ha(self.ctx.cls, self.fields.instance, self.ctx.spec.globals)
            return True
        else:
            return False

    def maybe_install_doc(self) -> None:
        if not getattr(self.ctx.cls, '__doc__'):
            self.ctx.cls.__doc__ = \
                self.ctx.cls.__name__ + str(inspect.signature(self.ctx.cls)).replace(' -> None', '')

    def __call__(self) -> None:
        self.install_params()

        self.install_fields()

        if self.ctx.extra_params.field_attrs:
            self.storage.install_field_attrs()

        if self.ctx.params.init:
            self.install_init()

        if self.ctx.params.repr:
            self.install_repr()

        if self.ctx.params.eq:
            self.install_eq()

        if self.ctx.params.order:
            self.install_order()

        if self.ctx.params.frozen:
            self.storage.install_frozen()

        self.maybe_install_hash()

        self.maybe_install_doc()
