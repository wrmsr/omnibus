import dataclasses as dc
import inspect

from ..internals import cmp_fn
from ..internals import frozen_get_del_attr
from ..internals import hash_action
from ..internals import PARAMS
from ..internals import repr_fn
from ..internals import tuple_str
from .types import Aspect


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

    def check(self) -> None:
        if self.ctx.params.order and not self.ctx.params.eq:
            raise ValueError('eq must be true if order is true')

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


class Frozen(Aspect):

    def check(self) -> None:
        any_frozen_base = any(getattr(b, PARAMS).frozen for b in self.ctx.spec.rmro if dc.is_dataclass(b))
        if any_frozen_base:
            if any_frozen_base and not self.ctx.params.frozen:
                raise TypeError('cannot inherit non-frozen dataclass from a frozen one')
            if not any_frozen_base and self.ctx.params.frozen:
                raise TypeError('cannot inherit frozen dataclass from a non-frozen one')

    def install(self) -> None:
        for fn in frozen_get_del_attr(
                self.ctx.cls,
                self.ctx.spec.fields.instance,
                self.ctx.spec.globals
        ):
            if self.ctx.set_new_attribute(fn.__name__, fn):
                raise TypeError(f'Cannot overwrite attribute {fn.__name__} in class {self.ctx.cls.__name__}')
