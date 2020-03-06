import abc
import typing as ta

from .. import check
from .. import defs
from .. import lang


F = ta.TypeVar('F')
T = ta.TypeVar('T')
U = ta.TypeVar('U')
R = ta.TypeVar('R')
C = ta.TypeVar('C')


# region Captures


class Capture(ta.Generic[T]):
    pass


class Captures:

    _NIL: 'Captures'

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
        return Captures(capture, value, Captures._NIL) if value is not None else Captures.NIL

    def add_all(self, other: 'Captures') -> 'Captures':
        if self is Captures._NIL:
            return self
        else:
            return Captures(self._capture, self._value, self._next.add_all(other))

    def get(self, capture: 'Capture[T]') -> T:
        if self is Captures._NIL:
            raise TypeError
        elif self._capture is capture:
            return self._value
        else:
            return self._next.get(capture)

    @staticmethod
    def empty() -> 'Captures':
        return Captures._NIL


Captures._NIL = Captures(None, None, None)


# endregion


# region Matches


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


# endregion


# region Properties


class Property(lang.Final, ta.Generic[F, T]):

    def __init__(self, function: ta.Callable[[F], lang.Maybe[T]]) -> None:
        super().__init__()

        self._function = check.callable(function)

    @property
    def function(self) -> ta.Callable[[F], lang.Maybe[T]]:
        return self._function

    @classmethod
    def of(cls, function: ta.Callable[[F], T]) -> 'Property[F, T]':
        return cls(lambda v: lang.Maybe(function(v)))

    def matching(self, pattern: 'Pattern[R]') -> 'PropertyPatternPair[F, R]':
        return PropertyPatternPair(self, pattern)

    def captured(self, capture: Capture[T]) -> 'PropertyPatternPair[F, T]':
        return self.matching(Pattern.any().captured(capture))

    def equals(self, value: T) -> 'PropertyPatternPair[F, T]':
        return self.matching(EqualsPattern(value, None))

    def filtering(self, predicate: ta.Callable[[T], bool]) -> 'PropertyPatternPair[F, T]':
        return self.matching(FilterPattern(predicate, None))


class PropertyPatternPair(ta.Generic[F, R]):

    def __init__(self, property: Property[F, ta.Any], pattern: 'Pattern[R]') -> None:
        super().__init__()

        self._property = check.isinstance(property, Property)
        self._pattern = check.isinstance(pattern, Pattern)

    @property
    def pattern(self) -> 'Pattern[R]':
        return self._pattern

    @property
    def property(self) -> 'Property[F, ta.Any]':
        return self._property


# endregion


# region Patterns


class Pattern(lang.Abstract, ta.Generic[T]):

    def __init__(self, next: ta.Optional['Pattern']) -> None:
        super().__init__()

        self._next = next

    @property
    def next(self) -> ta.Optional['Pattern']:
        return self._next

    @abc.abstractmethod
    def accept(self, visitor: 'Visitor[R, C]', context: C) -> R:
        raise NotImplementedError

    @abc.abstractmethod
    def accept_matcher(self, matcher: 'Matcher[T]', value: ta.Any, captures: Captures) -> Match[T]:
        raise NotImplementedError

    @classmethod
    def any(cls) -> 'Pattern[ta.Any]':
        return cls.type(object)

    @classmethod
    def type(cls, cls_: ta.Type[T]) -> 'Pattern[T]':
        return TypePattern(cls_)

    def capture(self, capture: Capture[T]) -> 'Pattern[T]':
        return CapturePattern(capture, self)

    def filter(self, predicate: ta.Callable[[T], bool]) -> 'Pattern[T]':
        return FilterPattern(predicate, self)

    def with_(self, property_pattern_pair: PropertyPatternPair[T, ta.Any]) -> 'Pattern[T]':
        return WithPattern(property_pattern_pair, self)


class CapturePattern(Pattern[T]):

    def __init__(self, capture: Capture[T], next: Pattern) -> None:
        super().__init__(check.not_none(next))

        self._capture = capture

    @property
    def capture(self) -> Capture[T]:
        return self._capture

    def accept(self, visitor: 'Visitor[R, C]', context: C) -> R:
        return visitor.visit_capture(self, context)

    def accept_matcher(self, matcher: 'Matcher[T]', value: ta.Any, captures: Captures) -> Match[T]:
        return matcher.match_capture(self, value, captures)


class EqualsPattern(Pattern[T]):

    def __init__(self, value: T, next: ta.Optional[Pattern]) -> None:
        super().__init__(next)

        self._value = value

    @property
    def value(self) -> T:
        return self._value

    def accept(self, visitor: 'Visitor[R, C]', context: C) -> R:
        return visitor.visit_equals(self, context)

    def accept_matcher(self, matcher: 'Matcher[T]', value: ta.Any, captures: Captures) -> Match[T]:
        return matcher.match_equals(self, value, captures)


class FilterPattern(Pattern[T]):

    def __init__(self, predicate: ta.Callable[[T], bool], next: ta.Optional[Pattern]) -> None:
        super().__init__(next)

        self._predicate = predicate

    @property
    def predicate(self) -> ta.Callable[[T], bool]:
        return self._predicate

    def accept(self, visitor: 'Visitor[R, C]', context: C) -> R:
        return visitor.visit_filter(self, context)

    def accept_matcher(self, matcher: 'Matcher[T]', value: ta.Any, captures: Captures) -> Match[T]:
        return matcher.match_filter(self, value, captures)


class TypePattern(Pattern[T]):

    def __init__(self, cls: ta.Type[T]) -> None:
        super().__init__(None)

        self._cls = cls

    @property
    def cls(self) -> ta.Type[T]:
        return self._cls

    def accept(self, visitor: 'Visitor[R, C]', context: C) -> R:
        return visitor.visit_type(self, context)

    def accept_matcher(self, matcher: 'Matcher[T]', value: ta.Any, captures: Captures) -> Match[T]:
        return matcher.match_type(self, value, captures)


class WithPattern(Pattern[T]):

    def __init__(self, property_pattern_pair: PropertyPatternPair[T, ta.Any], next: ta.Optional[Pattern]) -> None:
        super().__init__(next)

        self._property_pattern_pair = property_pattern_pair

    @property
    def property_pattern_pair(self) -> PropertyPatternPair[T]:
        return self._property_pattern_pair

    def accept(self, visitor: 'Visitor[R, C]', context: C) -> R:
        return visitor.visit_with(self, context)

    def accept_matcher(self, matcher: 'Matcher[T]', value: ta.Any, captures: Captures) -> Match[T]:
        return matcher.match_with(self, value, captures)


class Visitor(ta.Generic[R, C]):

    def process(self, pattern: Pattern, context: C) -> R:
        return pattern.accept(self, context)

    def visit(self, pattern: Pattern, context: C) -> R:
        raise TypeError(pattern)

    def visit_capture(self, pattern: CapturePattern, context: C) -> R:
        return self.visit(pattern, context)

    def visit_equals(self, pattern: EqualsPattern, context: C) -> R:
        return self.visit(pattern, context)

    def visit_filter(self, pattern: FilterPattern, context: C) -> R:
        return self.visit(pattern, context)

    def visit_type(self, pattern: TypePattern, context: C) -> R:
        return self.visit(pattern, context)

    def visit_with(self, pattern: WithPattern, context: C) -> R:
        return self.visit(pattern, context)


# endregion


# region Matchers


class Matcher(ta.Generic[T]):

    def match(self, pattern: Pattern[T], value: ta.Any, captures: Captures = Captures.empty()) -> Match[T]:
        raise TypeError(pattern)

    def match_capture(self, pattern: CapturePattern[T], value: ta.Any, captures: Captures) -> Match[T]:
        return self.match(pattern, value, captures)

    def match_equals(self, pattern: EqualsPattern[T], value: ta.Any, captures: Captures) -> Match[T]:
        return self.match(pattern, value, captures)

    def match_filter(self, pattern: FilterPattern[T], value: ta.Any, captures: Captures) -> Match[T]:
        return self.match(pattern, value, captures)

    def match_type(self, pattern: TypePattern[T], value: ta.Any, captures: Captures) -> Match[T]:
        return self.match(pattern, value, captures)

    def match_with(self, pattern: WithPattern[T], value: ta.Any, captures: Captures) -> Match[T]:
        return self.match(pattern, value, captures)


class DefaultMatcher(Matcher[T]):

    def match(self, pattern: Pattern[T], value: ta.Any, captures: Captures = Captures.empty()) -> Match[T]:
        if pattern.next is not None:
            match = self.match(pattern.next, value, captures)
            return match.flat_map(lambda v: pattern.accept_matcher(self, v, match.captures))
        else:
            return pattern.accept_matcher(self, value, captures)

    def match_capture(self, pattern: CapturePattern[T], value: ta.Any, captures: Captures) -> Match[T]:
        return Match.of(value, captures.add_all(Captures.of_optional(pattern.capture, value)))

    def match_equals(self, pattern: EqualsPattern[T], value: ta.Any, captures: Captures) -> Match[T]:
        return Match.of(value, captures).filter(lambda v: pattern.value == v)

    def match_filter(self, pattern: FilterPattern[T], value: ta.Any, captures: Captures) -> Match[T]:
        return Match.of(value, captures).filter(pattern.predicate)

    def match_type(self, pattern: TypePattern[T], value: ta.Any, captures: Captures) -> Match[T]:
        if isinstance(value, pattern.cls):
            return Match.of(value, captures)
        else:
            return Match.empty()

    """  # noqa
        Function<? super T, Optional<?>> property = (Function<? super T, Optional<?>>) withPattern.getProperty().getFunction();
        Optional<?> propertyValue = property.apply((T) object);
        Match<?> propertyMatch = propertyValue
                .map(value -> match(withPattern.getPattern(), value, captures))
                .orElse(Match.empty());
        return propertyMatch.map(ignored -> (T) object);
    """

    def match_with(self, pattern: WithPattern[T], value: ta.Any, captures: Captures) -> Match[T]:
        raise NotImplementedError


# endregion
