import typing as ta

from . import specs
from .. import lang


SpecT = ta.TypeVar('SpecT', bound=specs.Spec, covariant=True)


class BaseIsSubclassVisitor(specs.SpecVisitor[bool]):

    def visit_any_spec(self, spec: specs.AnySpec) -> bool:
        return True

    def visit_union_spec(self, spec: specs.UnionSpec) -> bool:
        return any(arg.accept(self) for arg in spec.args)


class IsSubclassVisitor(BaseIsSubclassVisitor):

    def __init__(self, sub: specs.Spec) -> None:
        super().__init__()
        self._sub = sub

    class SubVisitor(BaseIsSubclassVisitor, ta.Generic[SpecT], lang.Abstract):

        def __init__(self, sup: SpecT) -> None:
            super().__init__()
            self._sup = sup

    class NonGenericSubVisitor(SubVisitor[specs.NonGenericTypeSpec]):

        def visit_non_generic_type_spec(self, sub: specs.NonGenericTypeSpec) -> bool:
            return issubclass(sub.erased_cls, self._sup.erased_cls)

    def visit_non_generic_type_spec(self, sup: specs.NonGenericTypeSpec) -> bool:
        return self._sub.accept(self.NonGenericSubVisitor(sup))

    class ParametrizedGenericSubVisitor(SubVisitor[specs.ParameterizedGenericTypeSpec]):

        def visit_non_generic_type_spec(self, sub: specs.NonGenericTypeSpec) -> bool:
            if not issubclass(sub.cls, self._sup.erased_cls):
                return False
            if not all(isinstance(a, specs.AnySpec) for a in self._sup.args):
                return False
            return True

        def visit_parameterized_generic_type_spec(self, sub: specs.ParameterizedGenericTypeSpec) -> bool:
            if not issubclass(sub.erased_cls, self._sup.erased_cls):
                return False
            raise NotImplementedError

    def visit_parameterized_generic_type_spec(self, sup: specs.ParameterizedGenericTypeSpec) -> bool:
        return self._sub.accept(self.ParametrizedGenericSubVisitor(sup))


def issubclass_(sub: specs.Spec, sup: specs.Spec) -> bool:
    return sup.accept(IsSubclassVisitor(sub))
