"""
NOTES:
 - https://clojure.org/reference/multimethods
"""
import dataclasses as dc
import itertools
import typing as ta

from . import specs
from .. import collections as ocol
from .. import defs
from .. import lang


SpecT = ta.TypeVar('SpecT', bound=specs.Spec, covariant=True)
MatchGen = ta.Generator['Match', None, None]


class Match(lang.Final):

    def __init__(
            self,
            sub: specs.Spec,
            sup: specs.Spec,
            *,
            vars: ta.Mapping[ta.TypeVar, 'Match'] = ocol.frozendict(),
    ) -> None:
        super().__init__()

        if vars:
            if not isinstance(sup, specs.ParameterizedGenericTypeSpec):
                raise TypeError(sup)

        self._sub = sub
        self._sup = sup
        self._vars = vars

        self._bind: ta.Optional[specs.TypeLike] = None

    defs.basic('sub', 'sup', 'vars')

    @property
    def sub(self) -> specs.Spec:
        return self._sub

    @property
    def sup(self) -> specs.Spec:
        return self._sup

    @property
    def vars(self) -> ta.Mapping[ta.TypeVar, 'Match']:
        return self._vars

    @property
    def bind(self) -> specs.TypeLike:
        if self._bind is None:
            if self.vars:
                # FIXME: WRONG
                bspec = ta.cast(specs.ParameterizedGenericTypeSpec, self.sup)
                # FIXME: recursively replace params - recursive .bind?
                bind = bspec.cls[tuple(self.vars[p].sub.cls for p in bspec.cls_args if isinstance(p, ta.TypeVar))]
            else:
                bind = self.sub.cls
            self._bind = bind
        return self._bind


@dc.dataclass(frozen=True)
class Incomparable(Exception):
    sub: specs.Spec
    sup: specs.Spec


class IsSubclassVisitor(specs.SpecVisitor[MatchGen], lang.Abstract):
    pass


class SupVisitor(IsSubclassVisitor):

    def __init__(self, sub: specs.Spec) -> None:
        super().__init__()
        self._sub = sub

    class SubVisitor(IsSubclassVisitor, ta.Generic[SpecT], lang.Abstract):

        def __init__(self, sup: SpecT) -> None:
            super().__init__()
            self._sup = sup

    def visit_any_spec(self, sup: specs.AnySpec) -> MatchGen:
        yield Match(self._sub, sup)

    def visit_var_spec(self, sup: specs.VarSpec) -> MatchGen:
        if sup.bound is not None:
            raise NotImplementedError
        yield Match(self._sub, sup)

    def visit_union_spec(self, sup: specs.UnionSpec) -> MatchGen:
        for arg in sup.args:
            yield from _issubclass(self._sub, arg)

    def visit_any_union_spec(self, sup: specs.AnyUnionSpec) -> MatchGen:
        if not isinstance(self._sub, (specs.UnionSpec, specs.AnyUnionSpec)):
            return
        yield Match(self._sub, sup)

    class TypeSubVisitor(SubVisitor[SpecT], lang.Abstract):

        def visit_any_spec(self, sub: specs.AnySpec) -> MatchGen:
            if not isinstance(self._sup, specs.AnySpec):
                return
            yield Match(sub, self._sup)

        def visit_union_spec(self, sub: specs.UnionSpec) -> MatchGen:
            for arg in sub.args:
                if not issubclass_(arg, self._sup):
                    return
            yield Match(sub, self._sup)

        def visit_any_union_spec(self, sub: specs.AnyUnionSpec) -> MatchGen:
            return
            yield

    class NonGenericSubVisitor(TypeSubVisitor[specs.NonGenericTypeSpec]):

        def visit_non_generic_type_spec(self, sub: specs.NonGenericTypeSpec) -> MatchGen:
            if not issubclass(sub.erased_cls, self._sup.erased_cls):
                return
            yield Match(sub, self._sup)

        def visit_parameterized_generic_type_spec(self, sub: specs.ParameterizedGenericTypeSpec) -> MatchGen:
            if not issubclass(sub.erased_cls, self._sup.erased_cls):
                return
            # if not all(isinstance(a, specs.AnySpec) for a in sub.args):
            #     return
            yield Match(sub, self._sup)

    def visit_non_generic_type_spec(self, sup: specs.NonGenericTypeSpec) -> MatchGen:
        yield from self._sub.accept(self.NonGenericSubVisitor(sup))

    class ParametrizedGenericSubVisitor(TypeSubVisitor[specs.ParameterizedGenericTypeSpec]):

        def visit_non_generic_type_spec(self, sub: specs.NonGenericTypeSpec) -> MatchGen:
            if not issubclass(sub.erased_cls, self._sup.erased_cls):
                return
            if not all(isinstance(a, specs.AnySpec) for a in self._sup.args):
                raise Incomparable(sub, self._sup)
            yield Match(sub, self._sup)

        def visit_parameterized_generic_type_spec(self, sub: specs.ParameterizedGenericTypeSpec) -> MatchGen:
            if not issubclass(sub.erased_cls, self._sup.erased_cls):
                return
            if len(sub.args) != len(self._sup.args):
                raise Incomparable(sub, self._sup)
            mls = [list(_issubclass(l, r)) for l, r in zip(sub.args, self._sup.args)]
            for ml in itertools.product(*mls):
                vls = {}
                for a, m in zip(self._sup.args, ml):
                    if not isinstance(a, specs.VarSpec):
                        continue
                    vls.setdefault(a.cls, []).append(m)
                vs = {}
                for ac, vl in vls.items():
                    if len(vl) < 2:
                        [vs[ac]] = vl
                        continue
                    raise NotImplementedError
                yield Match(sub, self._sup, vars=ocol.frozendict(vs))

    def visit_parameterized_generic_type_spec(self, sup: specs.ParameterizedGenericTypeSpec) -> MatchGen:
        yield from self._sub.accept(self.ParametrizedGenericSubVisitor(sup))


def _issubclass(sub: specs.Spec, sup: specs.Spec) -> MatchGen:
    return sup.accept(SupVisitor(sub))


def issubclass_(sub: specs.Spec, sup: specs.Spec) -> bool:
    try:
        match = next(_issubclass(sub, sup))  # noqa
    except StopIteration:
        return False
    else:
        return True
