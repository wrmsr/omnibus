"""
Responsibilities:
 - signature, typeanns
 - defaults, defaut_factories, derivers
 - coercions
 - validations
 - field assignment
 - post-inits
"""
import dataclasses as dc
import functools
import types
import typing as ta

from ... import properties
from ..internals import create_fn
from ..internals import FieldType
from ..internals import get_field_type
from .defaulting import Defaulting
from .storage import Storage
from .types import Aspect
from .types import attach
from .types import InitPhase
from .types import Context


T = ta.TypeVar('T')
TypeT = ta.TypeVar('TypeT', bound=type, covariant=True)


class Init(Aspect):

    def process(self) -> None:
        if not self.ctx.spec.params.init:
            return

        attachments = [
            functools.partial(attachment, aspect)
            for aspect in self.ctx.aspects
            for attachment in aspect.attachment_lists_by_key.get('init', [])
        ]

        fctx = Context.Function(self.ctx, attachments)
        init = fctx.get_aspect(Init.Init)
        fn = init.build()
        self.ctx.set_new_attribute('__init__', fn)

    @attach('init')
    class Init(Aspect.Function['Init']):

        @properties.cached
        def defaulting(self) -> Defaulting.Init:
            return self.fctx.get_aspect(Defaulting.Init)

        @properties.cached
        def storage(self) -> Storage.Init:
            return self.fctx.get_aspect(Storage.Init)

        @properties.cached
        def type_names_by_field_name(self) -> ta.Mapping[str, str]:
            return {
                f.name: self.fctx.nsb.put(f'_{f.name}_type', f.type)
                for f in self.fctx.ctx.spec.fields.init
                if f.type is not dc.MISSING
            }

        @attach(InitPhase.SET_ATTRS)
        def build_set_attr_lines(self) -> ta.List[str]:
            dct = {}
            for f in self.fctx.ctx.spec.fields.init:
                if get_field_type(f) is FieldType.INIT:
                    continue
                elif f.default_factory is not dc.MISSING:
                    default_factory_name = self.defaulting.default_factory_names_by_field_name[f.name]
                    if f.init:
                        value = f'{default_factory_name}() if {f.name} is {self.defaulting.has_factory_name} else {f.name}'  # noqa
                    else:
                        value = f'{default_factory_name}()'
                elif f.init:
                    value = f.name
                else:
                    continue
                dct[f.name] = value
            return self.storage.build_set_attr_lines(dct, self.fctx.self_name)

        def _build_init_param(self, fld: dc.Field) -> str:
            if fld.default is dc.MISSING and fld.default_factory is dc.MISSING:
                default = ''
            elif fld.default is not dc.MISSING:
                default = ' = ' + self.defaulting.default_names_by_field_name[fld.name]
            elif fld.default_factory is not dc.MISSING:
                default = ' = ' + self.defaulting.has_factory_name
            else:
                raise TypeError
            return f'{fld.name}: {self.type_names_by_field_name[fld.name]}{default}'

        def build(self) -> types.FunctionType:
            lines = []

            for phase in InitPhase.__members__.values():
                for aspect in self.fctx.aspects:
                    for attachment in aspect.attachment_lists_by_key.get(phase, []):
                        lines.extend(attachment())

            if not lines:
                lines = ['pass']

            return create_fn(
                '__init__',
                [self.fctx.self_name] + [self._build_init_param(f) for f in self.fctx.ctx.spec.fields.init if f.init],
                lines,
                locals=dict(self.fctx.nsb),
                globals=self.fctx.ctx.spec.globals,
                return_type=None,
            )
