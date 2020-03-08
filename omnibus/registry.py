import typing as ta

from . import lang


lang.warn_unstable()


K = ta.TypeVar('K')
V = ta.TypeVar('V')


class Registry(ta.Mapping[K, V]):

    def __init__(
            self,
            *,
            weak_keys: bool = False,
            weak_values: bool = False,
    ) -> None:
        super().__init__()
