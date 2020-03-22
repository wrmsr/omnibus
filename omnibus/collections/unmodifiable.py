import typing as ta

from .. import check


T = ta.TypeVar('T')
K = ta.TypeVar('K')
V = ta.TypeVar('V')


class UnmodifiableSequence(ta.Sequence[T]):

    def __init__(self, target: ta.Sequence[T]) -> None:
        super().__init__()

        self._target = check.not_none(target)


class UnmodifiableSet(ta.AbstractSet[T]):

    def __init__(self, target: ta.AbstractSet[T]) -> None:
        super().__init__()

        self._target = check.not_none(target)


class UnmodifiableMapping(ta.Mapping[K, V]):

    def __init__(self, target: ta.Mapping[K, V]) -> None:
        super().__init__()

        self._target = check.not_none(target)

