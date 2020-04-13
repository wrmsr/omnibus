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

