import typing as ta

import pytest

from ... import c3
from ... import check
from ... import lang
from ... import reflect as rfl
from ... import registries
from ..types import Dispatcher
from ..types import Impl
from ..types import Manifest
from ..types import TypeOrSpec


T = ta.TypeVar('T')


class A:
    pass


class B:
    pass


class C(A):
    pass


class D(A):
    pass


class E(D):
    pass


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


def test_is_subclass():
    def isc(sub, sup):
        return rfl.get_spec(sup).accept(IsSubclassVisitor(rfl.get_spec(sub)))

    assert isc(int, int)
    assert isc(int, object)
    assert isc(int, ta.Any)


class GenericDispatcher(Dispatcher[Impl]):

    def __init__(self, registry: registries.Registry[rfl.Spec, Impl] = None) -> None:
        super().__init__()

        if registry is not None:
            self._registry = check.isinstance(registry, registries.Registry)
        else:
            self._registry = registries.DictRegistry()

    def key(self, obj: ta.Any) -> rfl.Spec:
        return rfl.get_spec(obj)

    @property
    def registry(self) -> registries.Registry[TypeOrSpec, Impl]:
        return self._registry

    def register_many(self, keys: ta.Iterable[TypeOrSpec], impl: Impl) -> 'Dispatcher[Impl]':
        for key in keys:
            cls = rfl.get_spec(key)
            self._registry[cls] = impl
        return self

    def _resolve(self, spec: rfl.Spec) -> ta.Optional[ta.Tuple[ta.Type, Impl]]:
        # mro = generic_compose_mro(cls, list(self._registry.keys()))
        # try:
        #     return match, self._registry[match]
        # except registries.NotRegisteredException:
        #     raise UnregisteredDispatchError(match)
        raise NotImplementedError

    def dispatch(self, key: TypeOrSpec) -> ta.Tuple[ta.Optional[Impl], ta.Optional[Manifest]]:
        spec = rfl.get_spec(key)
        try:
            impl = self._registry[spec]
        except registries.NotRegisteredException:
            match, impl = self._resolve(spec)
            return impl, Manifest(key, match)
        else:
            return impl, Manifest(key, spec)

    def __contains__(self, key: TypeOrSpec) -> bool:
        raise NotImplementedError


@pytest.mark.xfail()
def test_generic():
    disp = GenericDispatcher()

    disp[ta.Tuple[A, A]] = 'aa'
    disp[ta.Tuple[A, B]] = 'ab'

    impl, manifest = disp.dispatch(ta.Tuple[A, B])

    assert manifest.spec.erased_cls is tuple
    assert manifest.spec.args[0].cls is A
    assert manifest.spec.args[1].cls is B
