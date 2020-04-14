import dataclasses as dc
import typing as ta

from ... import codegen as cg
from ... import lang
from ... import properties
from .defaulting import Defaulting
from .defaulting import HasFactory
from .types import Aspect
from .types import attach


T = ta.TypeVar('T')
TypeT = ta.TypeVar('TypeT', bound=type, covariant=True)


class Init(Aspect, lang.Abstract):
    pass


class StandardInit(Init):

    def process(self) -> None:
        if not self.ctx.spec.params.init:
            return

        fctx = self.ctx.function(['init'])
        init = fctx.get_aspect(StandardInit.Init)
        fn = init.build('__init__')
        self.ctx.set_new_attribute('__init__', fn)

    @attach('init')
    class Init(Aspect.Function['StandardInit']):

        @properties.cached
        def defaulting(self) -> Defaulting.Init:
            return self.fctx.get_aspect(Defaulting.Init)

        @properties.cached
        def argspec(self) -> cg.ArgSpec:
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

            return argspec
