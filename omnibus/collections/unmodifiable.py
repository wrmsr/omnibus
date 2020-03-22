import typing as ta


T = ta.TypeVar('T')
K = ta.TypeVar('K')
V = ta.TypeVar('V')


class UnmodifiableMapping(ta.Mapping[K, V]):
    pass
