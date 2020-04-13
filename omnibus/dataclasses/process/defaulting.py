import dataclasses as dc
import typing as ta

from ... import check
from ... import collections as ocol
from ... import lang
from ... import properties
from ..types import Deriver
from ..types import ExtraFieldParams
from .types import Aspect
from .types import attach
from .utils import get_flat_fn_args


class _HasFactory(lang.Final):

    def __repr__(self) -> str:
        return '<factory>'


HasFactory = _HasFactory()


class Defaulting(Aspect):

    def check(self) -> None:
        # Make sure we don't have fields without defaults following fields with defaults.  This actually would be caught
        # when exec-ing the function source code, but catching it here gives a better error message, and future-proofs
        # us in case we build up the function using ast.
        seen_default = False
        for f in self.ctx.spec.fields.init:
            # Only consider fields in the __init__ call.
            if f.init:
                if not (f.default is dc.MISSING and f.default_factory is dc.MISSING):
                    seen_default = True
                elif seen_default:
                    raise TypeError(f'non-default argument {f.name!r} follows default argument')

    class DeriverNode(ta.NamedTuple):
        fn: ta.Callable
        ias: ta.FrozenSet[str]
        oas: ta.FrozenSet[str]

    @properties.cached
    def deriver_nodes(self) -> ta.Sequence[DeriverNode]:
        nodes: ta.List[Defaulting.DeriverNode] = []

        field_derivers_by_field = {
            f: efp.derive
            for f in self.ctx.spec.fields
            if ExtraFieldParams in f.metadata
            for efp in [f.metadata[ExtraFieldParams]]
            if efp.derive is not None
        }
        for f, fd in field_derivers_by_field.items():
            ias = get_flat_fn_args(fd)
            for ia in ias:
                check.in_(ia, self.ctx.spec.fields)
            nodes.append(self.DeriverNode(fd, frozenset(ias), frozenset([f.name])))

        extra_derivers = self.ctx.spec.rmro_extras_by_cls[Deriver]
        for ed in extra_derivers:
            ias = get_flat_fn_args(ed.fn)
            for ia in ias:
                check.in_(ia, self.ctx.spec.fields)
            if isinstance(ed.attrs, str):
                oas = [ed.attrs]
            elif isinstance(ed.attrs, ta.Iterable):
                oas = ed.attrs
            else:
                raise TypeError(ed)
            for oa in oas:
                check.isinstance(oa, str)
                check.in_(oa, self.ctx.spec.fields)
            nodes.append(self.DeriverNode(ed.fn, frozenset(ias), frozenset(oas)))

        return tuple(nodes)

    @properties.cached
    def deriver_supersteps(self):
        if not self.deriver_nodes:
            return

        nodes_by_oa = {}
        for n in self.deriver_nodes:
            for oa in n.oas:
                if oa in nodes_by_oa:
                    raise AttributeError('Duplicate deriver output', n, nodes_by_oa[oa])
                nodes_by_oa[oa] = n

        # TODO: ** hijack default factory machinery **
        return list(ocol.toposort({oa: set(n.ias) for oa, n in nodes_by_oa.items()}))

    @attach('init')
    class Init(Aspect.Function['Defaulting']):

        @properties.cached
        def default_names_by_field_name(self) -> ta.Mapping[str, str]:
            return {
                f.name: self.fctx.nsb.put(f'_{f.name}_default', f.default)
                for f in self.fctx.ctx.spec.fields.init
                if f.default is not dc.MISSING
            }

        @properties.cached
        def default_factory_names_by_field_name(self) -> ta.Mapping[str, str]:
            return {
                f.name: self.fctx.nsb.put(f'_{f.name}_default_factory', f.default_factory)
                for f in self.fctx.ctx.spec.fields.init
                if f.default_factory is not dc.MISSING
            }

        @properties.cached
        def has_factory_name(self) -> str:
            return self.fctx.nsb.put('has_factory', HasFactory, add=True)
