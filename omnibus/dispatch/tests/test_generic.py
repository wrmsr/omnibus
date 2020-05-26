import typing as ta

import pytest

from ... import check
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


class GenericDispatcher(Dispatcher[Impl]):

    def __init__(self, registry: registries.Registry[rfl.Spec, Impl] = None) -> None:
        super().__init__()

        if registry is not None:
            self._registry = check.isinstance(registry, registries.Registry)
        else:
            self._registry = registries.DictRegistry()

    def key(self, obj: ta.Any) -> rfl.Spec:
        return rfl.spec(obj)

    @property
    def registry(self) -> registries.Registry[TypeOrSpec, Impl]:
        return self._registry

    def register_many(self, keys: ta.Iterable[TypeOrSpec], impl: Impl) -> 'Dispatcher[Impl]':
        for key in keys:
            cls = rfl.spec(key)
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
        spec = rfl.spec(key)
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