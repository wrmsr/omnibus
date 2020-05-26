import abc
import enum
import types
import typing as ta
import weakref

from .. import caches
from .. import check
from .. import defs
from .. import lang
from .. import properties


class IsSubclassVisitor(rfl.SpecVisitor[bool]):

    def __init__(self, sub: rfl.Spec) -> None:
        super().__init__()

        self._sub = sub

    def visit_any_spec(self, sup: rfl.AnySpec) -> bool:
        return True

    class NonGenericVisitor(rfl.SpecVisitor[bool]):

        def __init__(self, sup: rfl.NonGenericTypeSpec) -> None:
            super().__init__()

            self._sup = sup

        def visit_any_spec(self, sub: rfl.AnySpec) -> bool:
            return True

        def visit_non_generic_type_spec(self, sub: rfl.NonGenericTypeSpec) -> bool:
            return issubclass(sub.erased_cls, self._sup.erased_cls)

        def visit_union_spec(self, sub: rfl.UnionSpec) -> bool:
            return any(arg.accept(self) for arg in sub.args)

    def visit_non_generic_type_spec(self, sup: rfl.NonGenericTypeSpec) -> bool:
        return self._sub.accept(self.NonGenericVisitor(sup))

    def visit_union_spec(self, sup: rfl.UnionSpec) -> bool:
        return any(arg.accept(self) for arg in sup.args)


