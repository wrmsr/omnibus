"""
TODO:
 - def __dataclass_replace__(self, ...
"""
import dataclasses as dc
import typing as ta

from ... import check
from ... import lang
from ... import properties
from ..internals import FieldType
from ..internals import get_field_type
from .storage import Storage
from .types import attach
from .types import InitPhase


pyrsistent = lang.lazy_import('pyrsistent')


class PyrsistentDescriptor:

    def __init__(
            self,
            field: dc.Field,
            vector_attr: str,
            idx: int,
            *,
            field_attrs: bool = False,
    ) -> None:
        super().__init__()

        self._field = field
        self._vector_attr = vector_attr
        self._idx = idx
        self._field_attrs = field_attrs

    def __get__(self, instance, owner):
        if instance is not None:
            vector = getattr(instance, self._vector_attr)
            try:
                return vector[self._idx]
            except IndexError:
                raise AttributeError(self._field.name)
        elif self._field_attrs is not None:
            return self._field
        else:
            return self


class PyrsistentStorage(Storage):

    @properties.cached
    def vector_attr(self) -> str:
        return '__%s_%x_vector' % (self.ctx.cls.__name__, id(self.ctx.cls))

    def check(self) -> None:
        check.not_none(pyrsistent())
        check.state(self.ctx.spec.params.frozen)

    def process(self) -> None:
        for idx, fld in enumerate(self.ctx.spec.fields.instance):
            dsc = PyrsistentDescriptor(
                fld,
                self.vector_attr,
                idx,
                field_attrs=self.ctx.spec.extra_params.field_attrs,
            )
            self.ctx.set_new_attribute(fld.name, dsc)

    @attach('init')
    class Init(Storage.Function['PyrsistentStorage']):

        @attach(InitPhase.SET_ATTRS)
        def build_set_attr_lines(self) -> ta.List[str]:
            args = []
            for f in self.fctx.ctx.spec.fields.init:
                if get_field_type(f) is FieldType.INIT:
                    continue
                if not f.init and f.default_factory is dc.MISSING:
                    continue
                args.append(f.name)
            vector_new = self.fctx.nsb.put('_vector_new', pyrsistent().pvector, add=True)
            return [self.build_setattr(self.aspect.vector_attr, f'{vector_new}(({", ".join(args)}),)')]
