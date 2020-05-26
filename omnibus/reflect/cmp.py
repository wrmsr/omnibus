from . import specs


class IsSubclassVisitor(specs.SpecVisitor[bool]):

    def __init__(self, sub: specs.Spec) -> None:
        super().__init__()

        self._sub = sub

    def visit_any_spec(self, sup: specs.AnySpec) -> bool:
        return True

    class NonGenericVisitor(specs.SpecVisitor[bool]):

        def __init__(self, sup: specs.NonGenericTypeSpec) -> None:
            super().__init__()

            self._sup = sup

        def visit_any_spec(self, sub: specs.AnySpec) -> bool:
            return True

        def visit_non_generic_type_spec(self, sub: specs.NonGenericTypeSpec) -> bool:
            return issubclass(sub.erased_cls, self._sup.erased_cls)

        def visit_union_spec(self, sub: specs.UnionSpec) -> bool:
            return any(arg.accept(self) for arg in sub.args)

    def visit_non_generic_type_spec(self, sup: specs.NonGenericTypeSpec) -> bool:
        return self._sub.accept(self.NonGenericVisitor(sup))

    def visit_union_spec(self, sup: specs.UnionSpec) -> bool:
        return any(arg.accept(self) for arg in sup.args)
