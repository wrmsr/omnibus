import abc
import typing as ta

from .. import check
from .. import defs
from .. import lang


F = ta.TypeVar('F')
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

    @staticmethod
    def of_optional(capture: 'Capture[T]', value: ta.Optional[T]) -> 'Captures':
        return Captures(capture, value, Captures.NIL) if value is not None else Captures.NIL

    def add_all(self, other: 'Captures') -> 'Captures':
        if self is Captures.NIL:
            return self
        else:
            return Captures(self._capture, self._value, self._next.add_all(other))

    def get(self, capture: 'Capture[T]') -> T:
        if self is Captures.NIL:
            raise TypeError
        elif self._capture is capture:
            return self._value
        else:
            return self._next.get(capture)


Captures.NIL = Captures(None, None, None)


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


class PropertyPatternPair(ta.Generic[T]):
    pass


class Pattern(ta.Generic[T]):

    def __init__(self, next: ta.Optional['Pattern']) -> None:
        super().__init__()

        self._next = next

    @property
    def next(self) -> ta.Optional['Pattern']:
        return self._next


class CapturePattern(Pattern[T]):

    def __init__(self, capture: Capture[T], next: Pattern) -> None:
        super().__init__(check.not_none(next))

        self._capture = capture

    @property
    def capture(self) -> Capture[T]:
        return self._capture


class EqualsPattern(Pattern[T]):

    def __init__(self, value: T, next: ta.Optional[Pattern]) -> None:
        super().__init__(next)

        self._value = value

    @property
    def value(self) -> T:
        return self._value


class FilterPattern(Pattern[T]):

    def __init__(self, predicate: ta.Callable[[T], bool], next: ta.Optional[Pattern]) -> None:
        super().__init__(next)

        self._predicate = predicate

    @property
    def predicate(self) -> ta.Callable[[T], bool]:
        return self._predicate


class TypeOfPattern(Pattern[T]):

    def __init__(self, cls: ta.Type[T]) -> None:
        super().__init__(None)

        self._cls = cls

    @property
    def cls(self) -> ta.Type[T]:
        return self._cls


class WithPattern(Pattern[T]):

    def __init__(self, property_pattern_pair: PropertyPatternPair[T], next: ta.Optional[Pattern]) -> None:
        super().__init__(next)

        self._property_pattern_pair = property_pattern_pair

    @property
    def property_pattern_pair(self) -> PropertyPatternPair[T]:
        return self._property_pattern_pair


class DefaultMatcher:
    pass
