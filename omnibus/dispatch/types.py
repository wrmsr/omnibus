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
            _cls: TypeOrSpec,
            _match: TypeOrSpec,
            *,
            _spec: rfl.Spec = None,
    ) -> None:
        super().__init__()

        self._cls = _cls
        self._match = _match
        self._spec = _spec

    @property
    def cls(self) -> TypeOrSpec:
        return self._cls

    @property
    def match(self) -> TypeOrSpec:
        return self._match

    @property
    def spec(self) -> rfl.Spec:
        if self._spec is None:
            self._spec = rfl.get_spec(self._cls)
        return self._spec

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self._cls!r}, {self._match!r})'

    def __iter__(self) -> ta.Iterator[ta.Type]:
        if rfl.is_generic(self._cls):
            return iter(self._cls.__args__)
        else:
            raise TypeError

    def __eq__(self, other):
        return (
            self.__class__ == other.__class__ and
            self._cls == other._type and
            self._match == other._match
        )


class Dispatcher(lang.Abstract, ta.Generic[Impl]):

    @staticmethod
    def key(obj: ta.Any) -> TypeOrSpec:
        return obj.__class__

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

    def __getitem__(self, key: TypeOrSpec) -> ta.Tuple[ta.Optional[Impl], ta.Optional[Manifest]]:
        return self.dispatch(key)

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
