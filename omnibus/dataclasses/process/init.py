import dataclasses as dc
import functools
import types
import typing as ta

from ... import codegen as cg
from ... import properties
from ..internals import create_fn
from .defaulting import Defaulting
from .types import Aspect
from .types import attach
from .types import Context
from .types import InitPhase


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
        def type_names_by_field_name(self) -> ta.Mapping[str, str]:
            return {
                f.name: self.fctx.nsb.put(f'_{f.name}_type', f.type)
                for f in self.fctx.ctx.spec.fields.init
                if f.type is not dc.MISSING
            }

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
