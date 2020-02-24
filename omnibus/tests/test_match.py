import abc
import typing as ta

from .. import defs
from .. import lang


T = ta.TypeVar('T')
U = ta.TypeVar('U')


class Capture(ta.Generic[T]):
    pass


class Captures:

    def __init__(self, capture: Capture, value: ta.Any, next: 'Captures') -> None:
        super().__init__()

        self._capture = capture
        self._value = value
        self._next = next

    defs.repr('capture', 'value')

    @property
    def capture(self) -> Capture:
        return self._capture

    @property
    def value(self) -> ta.Any:
        return self._value


class Match(lang.Sealed, lang.Abstract, ta.Generic[T]):

    @abc.abstractproperty
    def is_present(self) -> bool:
        raise NotImplementedError

    @abc.abstractproperty
    def value(self) -> T:
        raise NotImplementedError

    @abc.abstractproperty
    def captures(self) -> 'Captures':
        raise NotImplementedError

    @abc.abstractmethod
    def filter(self, predicate: ta.Callable[[T], bool]) -> 'Match[T]':
        raise NotImplementedError

    @abc.abstractmethod
    def map(self, mapper: ta.Callable[[T], U]) -> 'Match[T]':
        raise NotImplementedError

    @abc.abstractmethod
    def flat_map(self, mapper: ta.Callable[[T], 'Match[U]']) -> 'Match[T]':
        raise NotImplementedError

    @classmethod
    def of(cls, value: T, captures: 'Captures') -> 'Match[T]':
        return PresentMatch(value, captures)

    @classmethod
    def empty(cls) -> 'Match[T]':
        return EmptyMatch()


class PresentMatch(Match[T]):

    def __init__(self, value: T, captures: 'Captures') -> None:
        super().__init__()

        self._value = value
        self._captures = captures

    @property
    def value(self) -> T:
        return self._value

    @property
    def captures(self) -> 'Captures':
        return self._captures

    @property
    def is_present(self) -> bool:
        return True

    def filter(self, predicate: ta.Callable[[T], bool]) -> 'Match[T]':
        return self if predicate(self._value) else Match.empty()

    def map(self, mapper: ta.Callable[[T], U]) -> 'Match[T]':
        return Match.of(mapper(self._value), self._captures)

    def flat_map(self, mapper: ta.Callable[[T], 'Match[U]']) -> 'Match[T]':
        return mapper(self._value)


class EmptyMatch(Match[T]):

    @property
    def is_present(self) -> bool:
        return False

    @property
    def value(self) -> bool:
        raise TypeError

    @property
    def captures(self) -> 'Captures':
        raise TypeError

    def filter(self, predicate: ta.Callable[[T], bool]) -> 'Match[T]':
        return self

    def map(self, mapper: ta.Callable[[T], U]) -> 'Match[T]':
        return self

    def flat_map(self, mapper: ta.Callable[[T], 'Match[U]']) -> 'Match[T]':
        return self


class Property:
    pass


class PropertyPatternPair:
    pass


class Pattern:
    pass


class CapturePattern(Pattern):
    pass


class EqualsPattern(Pattern):
    pass


class FilterPattern(Pattern):
    pass


class TypeOfPattern(Pattern):
    pass


class WithPattern(Pattern):
    pass


class DefaultMatcher:
    pass
