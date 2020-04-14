import dataclasses as dc
import typing as ta

from ... import check
from ... import codegen as cg
from ... import properties
from ..internals import FieldType
from ..internals import get_field_type
from .defaulting import Defaulting
from .init import Init
from .storage import Storage
from .types import Aspect
from .types import attach
from .types import InitPhase


class DictDescriptor:

    def __init__(
            self,
            field: dc.Field,
            dict_attr: str,
            *,
            frozen: bool = False,
            field_attrs: bool = False,
    ) -> None:
        super().__init__()

        self._field = field
        self._dict_attr = dict_attr
        self._frozen = frozen
        self._field_attrs = field_attrs

    def __get__(self, instance, owner):
        if instance is not None:
            dct = getattr(instance, self._dict_attr)
            try:
                return dct[self._field.name]
            except KeyError:
                raise AttributeError(self._field.name)
        elif self._field_attrs is not None:
            return self._field
        else:
            return self

    def __set__(self, instance, value):
        if self._frozen:
            raise dc.FrozenInstanceError(f'cannot assign to field {self._field.name!r}')
        getattr(instance, self._dict_attr)[self._field.name] = value

    def __delete__(self, instance):
        if self._frozen:
            raise dc.FrozenInstanceError(f'cannot delete field {self._field.name!r}')
        del getattr(instance, self._dict_attr)[self._field.name]


class DictStorage(Storage):

    @properties.cached
    def dict_attr(self) -> str:
        return '__%s_%x_dict' % (self.ctx.cls.__name__, id(self.ctx.cls))

    def process(self) -> None:
        for fld in self.ctx.spec.fields.instance:
            dsc = DictDescriptor(
                fld,
                self.dict_attr,
                frozen=self.ctx.spec.params.frozen,
                field_attrs=self.ctx.spec.extra_params.field_attrs,
            )
            self.ctx.set_new_attribute(fld.name, dsc)

    @attach('init')
    class Init(Aspect.Function['DictStorage']):

        @attach(InitPhase.SET_ATTRS)
        def build_set_attr_lines(self) -> ta.List[str]:
            ret = [f'{self.fctx.self_name}.{self.aspect.dict_attr} = {{}}']
            for f in self.fctx.ctx.spec.fields.init:
                if get_field_type(f) is FieldType.INIT:
                    continue
                if not f.init and f.default_factory is dc.MISSING:
                    continue
                ret.append(f'{self.fctx.self_name}.{self.aspect.dict_attr}[{f.name!r}] = {f.name}')
            return ret


class DictInit(Init):

    def process(self) -> None:
        if not self.ctx.spec.params.init:
            return

        fctx = self.ctx.function(['init'])
        init = fctx.get_aspect(DictInit.Init)
        fn = init.build('__init__')
        self.ctx.set_new_attribute('__init__', fn)

    @attach('init')
    class Init(Aspect.Function['DictInit']):

        @properties.cached
        def defaulting(self) -> Defaulting:
            return check.isinstance(self.fctx.get_aspect(Defaulting), Defaulting)

        @properties.cached
        def dict_name(self) -> str:
            return self.fctx.nsb.put('_dict', None, add=True)

        @properties.cached
        def argspec(self) -> cg.ArgSpec:
            return cg.ArgSpec(
                [self.fctx.self_name, self.dict_name],
                annotations={'return': None, self.dict_name: ta.Mapping[str, ta.Any]},
            )

        @attach(InitPhase.BOOTSTRAP)
        def build_bootstrap_lines(self) -> ta.List[str]:
            ret = []
            for fld in self.fctx.ctx.spec.fields.init:
                if not fld.init:
                    continue
                if fld.default is dc.MISSING and fld.default_factory is dc.MISSING:
                    ret.append(f'{fld.name} = {self.dict_name}[{fld.name!r}]')
                elif fld.default is not dc.MISSING:
                    ret.append(f'{fld.name} = {self.dict_name}get({fld.name!r}, {self.default_names_by_field_name[fld.name]}')  # noqa
                elif fld.default_factory is not dc.MISSING:
                    ret.append(f'{fld.name} = {self.dict_name}get({fld.name!r}, {self.defaulting.has_factory_name}')
                else:
                    raise TypeError
            return ret
