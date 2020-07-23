import dataclasses as dc
import typing as ta

from ... import check
from ... import code
from ... import properties
from ..internals import FieldType
from ..internals import get_field_type
from .init import append_argspec_args
from .init import Init
from .storage import Storage
from .types import Aspect
from .types import attach


class TupleDescriptor:

    def __init__(
            self,
            field: dc.Field,
            idx: int,
            *,
            field_attrs: bool = False,
    ) -> None:
        super().__init__()

        self._field = field
        self._idx = idx
        self._field_attrs = field_attrs

    def __get__(self, instance, owner=None):
        if instance is not None:
            try:
                return instance[self._idx]
            except IndexError:
                raise AttributeError(self._field.name)
        elif self._field_attrs is not None:
            return self._field
        else:
            return self


class TupleStorage(Storage):

    def check(self) -> None:
        check.state(issubclass(self.ctx.cls, tuple))
        check.state(self.ctx.spec.params.frozen)
        check.state(not self.ctx.spec.extra_params.allow_setattr)

    def process(self) -> None:
        for idx, fld in enumerate(self.ctx.spec.fields.instance):
            dsc = TupleDescriptor(
                fld,
                idx,
                field_attrs=self.ctx.spec.extra_params.field_attrs,
            )
            self.ctx.set_new_attribute(fld.name, dsc)

    @attach('init')
    class Init(Storage.Function['TupleStorage']):

        @properties.cached
        def cls_name(self) -> str:
            return self.fctx.nsb.put(None, '_cls')

        @attach(Aspect.Function.Phase.SET_ATTRS)
        def build_set_attr_lines(self) -> ta.List[str]:
            args = []
            for f in self.fctx.ctx.spec.fields.init:
                if get_field_type(f) is FieldType.INIT:
                    continue
                if not f.init and f.default_factory is dc.MISSING:
                    continue
                args.append(f.name)
            tuple_new = self.fctx.nsb.put(tuple.__new__, '_tuple_new')
            return [f'{self.fctx.self_name} = {tuple_new}({self.cls_name}, ({", ".join(args)}),)']


class TupleInit(Init):

    def process(self) -> None:
        if not self.ctx.spec.params.init:
            return

        fctx = self.ctx.function(['init'])
        init = fctx.get_aspect(TupleInit.Init)
        fn = init.build('__new__')
        self.ctx.set_new_attribute('__new__', fn)

    @attach('init')
    class Init(Aspect.Function['TupleInit']):

        @properties.cached
        def storage(self) -> TupleStorage.Init:
            return self.fctx.get_aspect(TupleStorage.Init)

        @properties.cached
        def argspec(self) -> code.ArgSpec:
            argspec = code.ArgSpec(
                [self.storage.cls_name],
                annotations={'return': self.fctx.nsb.put(self.fctx.ctx.cls)},
            )
            return append_argspec_args(argspec, self.fctx.ctx.spec.fields.init)

        @attach(Aspect.Function.Phase.RETURN)
        def build_return_lines(self) -> ta.List[str]:
            return [f'return {self.fctx.self_name}']
