import typing as ta

from .. import c3
from .. import check
from .. import reflect as rfl
from .. import registries
from .types import Impl
from .types import T
from .types import TypeOrSpec
from .types import Dispatcher
from .types import AmbiguousDispatchError
from .types import UnregisteredDispatchError
from .types import Manifest


def generic_issubclass(left: ta.Type, right: ta.Type) -> bool:
    if rfl.is_generic(right):
        right = check.not_none(rfl.erase_generic(right))
    return issubclass(left, right)


def generic_compose_mro(
        cls: T,
        types: ta.Sequence[T] = None,
):
    return c3.compose_mro(
        cls,
        list(types),
        getbases=rfl.generic_bases,
        issubclass=generic_issubclass,
    )


class ErasingDispatcher(Dispatcher[Impl]):

    _dict: ta.Dict[ta.Type, Impl]

    def __init__(self, registry: registries.Registry[ta.Type, Impl] = None) -> None:
        super().__init__()

        if registry is not None:
            self._registry = check.isinstance(registry, registries.Registry)
        else:
            self._registry = registries.DictRegistry()

    @property
    def registry(self) -> registries.Registry[TypeOrSpec, Impl]:
        return self._registry

    def _resolve(self, cls: ta.Type) -> ta.Optional[ta.Tuple[ta.Type, Impl]]:
        mro = generic_compose_mro(cls, list(self._registry.keys()))
        match = None
        for t in mro:
            if match is not None:
                # If *match* is an implicit ABC but there is another unrelated,
                # equally matching implicit ABC, refuse the temptation to guess.
                if (
                        t in self._registry and
                        t not in cls.__mro__ and
                        match not in cls.__mro__ and
                        not issubclass(match, t)
                ):
                    raise AmbiguousDispatchError(match, t)
                break
            if t in self._registry:
                match = t

        try:
            return match, self._registry[match]
        except registries.NotRegisteredException:
            raise UnregisteredDispatchError(match)

    def _erase(self, cls: TypeOrSpec) -> ta.Type:
        return check.isinstance(rfl.erase_generic(cls.erased_cls if isinstance(cls, rfl.TypeSpec) else cls), type)

    def __setitem__(self, cls: TypeOrSpec, impl: Impl) -> None:
        cls = self._erase(cls)
        self._registry[cls] = impl

    def __getitem__(self, cls: TypeOrSpec) -> ta.Tuple[ta.Optional[Impl], ta.Optional[Manifest]]:
        ecls = self._erase(cls)
        try:
            impl = self._registry[ecls]
        except registries.NotRegisteredException:
            match, impl = self._resolve(ecls)
            return impl, Manifest(cls, match)
        else:
            return impl, Manifest(cls, ecls)

    def __contains__(self, cls: TypeOrSpec) -> bool:
        cls = self._erase(cls)
        return cls in self._registry