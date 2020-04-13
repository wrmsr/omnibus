import dataclasses as dc
import inspect
import typing as ta

from ... import check
from ... import lang
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
AspectT = ta.TypeVar('AspectT', bound='Aspect', covariant=True)


class Aspect(lang.Abstract):

    def __init__(self, ctx: BuildContext[TypeT]) -> None:
        super().__init__()

        self._ctx = check.isinstance(ctx, BuildContext)

    @property
    def ctx(self) -> BuildContext:
        return self._ctx

    def install(self) -> None:
        pass

    class Init(ta.Generic[AspectT]):

        def __init__(self, owner: AspectT) -> None:
            super().__init__()

            self._owner = owner

        @property
        def owner(self) -> AspectT:
            return self._owner


class Repr(Aspect):

    def install(self) -> None:
        if not self.ctx.params.repr:
            return

        flds = [f for f in self.ctx.spec.fields.instance if f.repr]
        self.ctx.set_new_attribute('__repr__', repr_fn(flds, self.ctx.spec.globals))


class Eq(Aspect):

    def install(self) -> None:
        if not self.ctx.params.eq:
            return

        flds = [f for f in self.ctx.spec.fields.instance if f.compare]
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


class Order(Aspect):

    def install(self) -> None:
        if not self.ctx.params.order:
            return

        flds = [f for f in self.ctx.spec.fields.instance if f.compare]
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


class Hash(Aspect):

    def install(self) -> None:
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
            self.ctx.cls.__hash__ = ha(self.ctx.cls, self.ctx.spec.fields.instance, self.ctx.spec.globals)


class Doc(Aspect):

    def install(self) -> None:
        if not getattr(self.ctx.cls, '__doc__'):
            self.ctx.cls.__doc__ = \
                self.ctx.cls.__name__ + str(inspect.signature(self.ctx.cls)).replace(' -> None', '')
