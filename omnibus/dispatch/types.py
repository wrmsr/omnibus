"""
TODO:
 - simple typeclasses, boilerplate is just too much

NOTE:
 - dispatch _below_ injector - usable without
  - but this much simpler - main usecase is intra-class shit (registry properties)
"""
import abc
import typing as ta

from .. import check
from .. import lang
from .. import reflect as rfl
from .. import registries


T = ta.TypeVar('T')
R = ta.TypeVar('R')
Impl = ta.TypeVar('Impl')
TypeOrSpec = ta.Union[ta.Type, rfl.Spec]


class DispatchError(Exception):
    pass


class AmbiguousDispatchError(DispatchError):
    pass


class UnregisteredDispatchError(DispatchError):
    pass


class Manifest(lang.Final):

    def __init__(
            self,
            cls: TypeOrSpec,
            match: TypeOrSpec,
            *,
            vars: ta.Optional[ta.Mapping[ta.TypeVar, rfl.Spec]] = None,
    ) -> None:
        super().__init__()

        self._cls = cls
        self._match = match
        self._vars = vars
        self._spec: ta.Optional[rfl.Spec] = None

    @property
    def cls(self) -> TypeOrSpec:
        return self._cls

    @property
    def match(self) -> TypeOrSpec:
        return self._match

    @property
    def spec(self) -> rfl.Spec:
        if self._spec is None:
            self._spec = rfl.spec(self._cls)
        return self._spec

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self._cls!r}, {self._match!r})'

    def __getitem__(self, var: ta.TypeVar) -> rfl.Spec:
        if self._vars is None:
            raise TypeError
        return self._vars[var]

    def __eq__(self, other):
        return (
            self.__class__ == other.__class__ and
            self._cls == other._type and
            self._match == other._match
        )


class Dispatcher(lang.Abstract, ta.Generic[Impl]):

    @abc.abstractmethod
    def key(self, obj: ta.Any) -> TypeOrSpec:
        raise NotImplementedError

    @abc.abstractproperty
    def registry(self) -> registries.Registry[TypeOrSpec, Impl]:
        raise NotImplementedError

    @abc.abstractmethod
    def register_many(self, keys: ta.Iterable[TypeOrSpec], impl: Impl) -> 'Dispatcher[Impl]':
        raise NotImplementedError

    def register(self, key: TypeOrSpec, impl: Impl) -> 'Dispatcher[Impl]':
        check.not_none(key)
        return self.register_many([key], impl)

    def registering(self, *keys: TypeOrSpec) -> 'ta.Callable[[Impl], Impl]':
        def inner(impl: Impl) -> Impl:
            self.register_many(keys, impl)
            return impl
        return inner

    def __setitem__(self, key: TypeOrSpec, impl: Impl) -> None:
        self.register(key, impl)

    @abc.abstractmethod
    def dispatch(self, key: TypeOrSpec) -> ta.Tuple[ta.Optional[Impl], ta.Optional[Manifest]]:
        raise NotImplementedError

    def __getitem__(self, obj: ta.Any) -> ta.Optional[Impl]:
        return self.dispatch(self.key(obj))[0]

    @abc.abstractmethod
    def __contains__(self, key: TypeOrSpec) -> bool:
        raise NotImplementedError


class CacheGuard(lang.Abstract):

    @abc.abstractmethod
    def update(self, cls: TypeOrSpec) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def maybe_clear(self) -> bool:
        raise NotImplementedError
