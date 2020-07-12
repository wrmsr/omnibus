"""
NOTES:
 - https://clojure.org/reference/multimethods
"""
import typing as ta

from . import specs
from .. import defs
from .. import lang


SpecT = ta.TypeVar('SpecT', bound=specs.Spec, covariant=True)


class Incomparable(Exception):

    def __init__(self, sub: specs.Spec, sup: specs.Spec) -> None:
        super().__init__(sub, sup)
        self._sub = sub
        self._sup = sup

    defs.repr('sub', 'sup')
    defs.hash_eq('sub', 'sup')

    @property
    def sub(self) -> specs.Spec:
        return self._sub

    @property
    def sup(self) -> specs.Spec:
        return self._sup


class IsSubclassVisitor(specs.SpecVisitor[bool], lang.Abstract):

    def visit_union_spec(self, spec: specs.UnionSpec) -> bool:
        return any(arg.accept(self) for arg in spec.args)


class SupVisitor(IsSubclassVisitor):

    def __init__(self, sub: specs.Spec) -> None:
        super().__init__()
        self._sub = sub

    class SubVisitor(IsSubclassVisitor, ta.Generic[SpecT], lang.Abstract):

        def __init__(self, sup: SpecT) -> None:
            super().__init__()
            self._sup = sup

        def visit_any_spec(self, sub: specs.AnySpec) -> bool:
            return isinstance(self._sup, specs.AnySpec)

    def visit_any_spec(self, sup: specs.AnySpec) -> bool:
        return True

    class NonGenericSubVisitor(SubVisitor[specs.NonGenericTypeSpec]):

        def visit_non_generic_type_spec(self, sub: specs.NonGenericTypeSpec) -> bool:
            return issubclass(sub.erased_cls, self._sup.erased_cls)

        def visit_parameterized_generic_type_spec(self, sub: specs.ParameterizedGenericTypeSpec) -> bool:
            if not issubclass(sub.erased_cls, self._sup.erased_cls):
                return False
            if not all(isinstance(a, specs.AnySpec) for a in sub.args):
                return False
            return True

    def visit_non_generic_type_spec(self, sup: specs.NonGenericTypeSpec) -> bool:
        return self._sub.accept(self.NonGenericSubVisitor(sup))

    class ParametrizedGenericSubVisitor(SubVisitor[specs.ParameterizedGenericTypeSpec]):

        def visit_non_generic_type_spec(self, sub: specs.NonGenericTypeSpec) -> bool:
            if not issubclass(sub.erased_cls, self._sup.erased_cls):
                return False
            if not all(isinstance(a, specs.AnySpec) for a in self._sup.args):
                raise Incomparable(sub, self._sup)
            return True

        def visit_parameterized_generic_type_spec(self, sub: specs.ParameterizedGenericTypeSpec) -> bool:
            if not issubclass(sub.erased_cls, self._sup.erased_cls):
                return False
            if len(sub.args) != len(self._sup.args):
                raise Incomparable(sub, self._sup)
            if not all(issubclass_(l, r) for l, r in zip(sub.args, self._sup.args)):
                return False
            return True

    def visit_parameterized_generic_type_spec(self, sup: specs.ParameterizedGenericTypeSpec) -> bool:
        return self._sub.accept(self.ParametrizedGenericSubVisitor(sup))


def issubclass_(sub: specs.Spec, sup: specs.Spec) -> bool:
    return sup.accept(SupVisitor(sub))
