import dataclasses as dc
import functools
import types
import typing as ta

from ... import codegen as cg
from ... import properties
from .defaulting import Defaulting
from .defaulting import HasFactory
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

        def build(self) -> types.FunctionType:
            lines = []

            for phase in InitPhase.__members__.values():
                for aspect in self.fctx.aspects:
                    for attachment in aspect.attachment_lists_by_key.get(phase, []):
                        lines.extend(attachment())

            if not lines:
                lines = ['pass']

            argspec = cg.ArgSpec(
                [self.fctx.self_name],
                annotations={'return': None},
            )
            for fld in self.fctx.ctx.spec.fields.init:
                if not fld.init:
                    continue
                if fld.default is dc.MISSING and fld.default_factory is dc.MISSING:
                    argspec.args.append(fld.name)
                elif fld.default is not dc.MISSING:
                    argspec.args.append(fld.name)
                    argspec.defaults.append(fld.default)
                elif fld.default_factory is not dc.MISSING:
                    argspec.args.append(fld.name)
                    argspec.defaults.append(HasFactory)
                else:
                    raise TypeError
                if fld.type is not dc.MISSING:
                    argspec.annotations[fld.name] = fld.type

            return cg.create_fn(
                '__init__',
                argspec,
                '\n'.join(lines),
                locals=dict(self.fctx.nsb),
                globals=self.fctx.ctx.spec.globals,
            )
