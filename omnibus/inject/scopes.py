import threading
import typing as ta

from .. import lang
from ..collections import IdentityKeyDict
from .types import Scope
from .types import Binding


T = ta.TypeVar('T')


class NoScope(Scope, lang.Final):

    def provide(self, binding: Binding[T]) -> T:
        return binding.provider()


class AbstractSingletonScope(Scope, lang.Abstract):

    def __init__(self) -> None:
        super().__init__()

        self._values: ta.MutableMapping[Binding, ta.Any] = IdentityKeyDict()
        self._lock = threading.RLock()

    def provide(self, binding: Binding[T]) -> T:
        try:
            return self._values[binding]
        except KeyError:
            pass
        with self._lock:
            try:
                return self._values[binding]
            except KeyError:
                pass
            value = self._values[binding] = binding.provider()
            return value


class SingletonScope(AbstractSingletonScope, lang.Final):
    pass


class EagerSingletonScope(AbstractSingletonScope, lang.Final):
    pass


class ThreadScope(Scope):

    def __init__(self) -> None:
        super().__init__()

        self._local = threading.local()

    def provide(self, binding: Binding[T]) -> T:
        try:
            values = self._local.values
        except AttributeError:
            values = self._local.values = IdentityKeyDict()
        try:
            return values[binding]
        except KeyError:
            value = values[binding] = binding.provider()
            return value
