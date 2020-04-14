import dataclasses as dc
import functools
import types
import typing as ta

from ... import check
from ... import codegen as cg
from ... import lang
from ... import lang
from ... import properties
from ... import properties
from ..internals import FieldType
from ..internals import get_field_type
from .defaulting import Defaulting
from .defaulting import HasFactory
from .types import Aspect
from .types import Aspect
from .types import attach
from .types import attach
from .types import Context
from .types import InitPhase
from .types import InitPhase
from .init import Init
from .storage import Storage


T = ta.TypeVar('T')
TypeT = ta.TypeVar('TypeT', bound=type, covariant=True)


class DictDescriptor:

    def __init__(
            self,
            field: dc.Field,
            dict_attr: str,
            *,
            frozen: bool = False,
            attr_fields: bool = False,
    ) -> None:
        super().__init__()

        self._field = field
        self._dict_attr = dict_attr
        self._frozen = frozen
        self._attr_fields = attr_fields

    def __get__(self, instance, owner):
        if instance is not None:
            dct = getattr(instance, self._dict_attr)
            try:
                return dct[self._field.name]
            except KeyError:
                raise AttributeError(self._field.name)
        elif self._attr_fields is not None:
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
                attr_fields=self.ctx.spec.params.attr_fields,
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

        attachments = [
            functools.partial(attachment, aspect)
            for aspect in self.ctx.aspects
            for attachment in aspect.attachment_lists_by_key.get('init', [])
        ]

        fctx = Context.Function(self.ctx, attachments)
        init = fctx.get_aspect(DictInit.Init)
        fn = init.build()
        self.ctx.set_new_attribute('__init__', fn)

    @attach('init')
    class Init(Aspect.Function['DictInit']):

        @properties.cached
        def storage(self) -> DictStorage:
            return check.isinstance(self.fctx.get_aspect(Storage), DictStorage)

        @properties.cached
        def argspec(self) -> cg.ArgSpec:
            return cg.ArgSpec(
                [self.fctx.self_name, 'dct'],
                annotations={'return': None, 'dct': ta.Mapping[str, ta.Any]},
            )

        def build(self) -> types.FunctionType:
            lines = []

            for phase in InitPhase.__members__.values():
                for aspect in self.fctx.aspects:
                    for attachment in aspect.attachment_lists_by_key.get(phase, []):
                        lines.extend(attachment())

            if not lines:
                lines = ['pass']

            return cg.create_fn(
                '__init__',
                self.argspec,
                '\n'.join(lines),
                locals=dict(self.fctx.nsb),
                globals=self.fctx.ctx.spec.globals,
            )
