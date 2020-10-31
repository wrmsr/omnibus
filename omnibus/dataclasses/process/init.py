import dataclasses as dc
import typing as ta

from ... import code
from ... import lang
from ... import properties
from ..types import ExtraFieldParams
from .storage import Storage
from .defaulting import HasFactory
from .types import Aspect
from .types import attach


T = ta.TypeVar('T')
TypeT = ta.TypeVar('TypeT', bound=type, covariant=True)


class Init(Aspect, lang.Abstract):

    @property
    def deps(self) -> ta.Collection[ta.Type[Aspect]]:
        return [Storage]

    def process(self) -> None:
        raise TypeError


def append_argspec_args(argspec: code.ArgSpec, fields: ta.Iterable[dc.Field]) -> code.ArgSpec:
    args = []
    defaults = []
    kwonlyargs = []
    kwonlydefaults = {}
    annotations = {}

    for fld in fields:
        if not fld.init:
            continue

        efp = fld.metadata.get(ExtraFieldParams)
        if efp is not None and efp.kwonly:
            if fld.default is dc.MISSING and fld.default_factory is dc.MISSING:
                kwonlyargs.append(fld.name)
            elif fld.default is not dc.MISSING:
                kwonlyargs.append(fld.name)
                kwonlydefaults[fld.name] = fld.default
            elif fld.default_factory is not dc.MISSING:
                kwonlyargs.append(fld.name)
                kwonlydefaults[fld.name] = HasFactory
            else:
                raise TypeError
        elif fld.default is dc.MISSING and fld.default_factory is dc.MISSING and (efp is None or efp.derive is dc.MISSING):  # noqa
            args.append(fld.name)
        elif fld.default is not dc.MISSING:
            args.append(fld.name)
            defaults.append(fld.default)
        elif fld.default_factory is not dc.MISSING or (efp is not None and efp.derive is not dc.MISSING):
            args.append(fld.name)
            defaults.append(HasFactory)
        else:
            raise TypeError

        if fld.type is not dc.MISSING:
            annotations[fld.name] = fld.type

    return dc.replace(
        argspec,
        args=list(argspec.args) + args,
        defaults=list(argspec.defaults) + defaults,
        kwonlyargs=kwonlyargs,
        kwonlydefaults=kwonlydefaults,
        annotations={**argspec.annotations, **annotations},
    )


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
        def argspec(self) -> code.ArgSpec:
            argspec = code.ArgSpec(
                [self.fctx.self_name],
                annotations={'return': None},
            )
            return append_argspec_args(argspec, self.fctx.ctx.spec.fields.init)
