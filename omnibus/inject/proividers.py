import typing as ta

from .. import dataclasses as dc
from .. import lang
from .types import Injector
from .types import Key
from .types import Provider


T = ta.TypeVar('T')
K = ta.TypeVar('K')
V = ta.TypeVar('V')


@dc.dataclass(frozen=True)
class ValueProvider(Provider[T]):
    value: T

    def __call__(self) -> T:
        return self.value


@dc.dataclass(frozen=True)
class CallableProvider(Provider[T]):
    callable: ta.Callable[[], T]

    def __call__(self) -> T:
        return self.callable()


@dc.dataclass(frozen=True)
class ClassProvider(CallableProvider[T], lang.Final):
    cls: ta.Type[T]


@dc.dataclass(frozen=True)
class LinkedProvider(Provider[T], lang.Final):
    key: Key[T]

    def __call__(self) -> T:
        return Injector.current.get_instance(self.key)


@dc.dataclass(frozen=True)
class ProviderLinkedProvider(Provider[T], lang.Final):
    key: Key[T]

    def __call__(self) -> T:
        return Injector.current.get_instance(Key(Provider[self.key.type], self.key.annotation))()


@dc.dataclass(frozen=True)
class DelegatedProvider(Provider[T], lang.Final):
    key: Key[T]
    injector: 'Injector'

    def __call__(self) -> T:
        return self.injector.get_instance(self.key)
