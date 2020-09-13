import typing as ta

from .. import check
from .. import dataclasses as dc
from .. import lang
from .types import Injector
from .types import Key
from .types import MultiBinding
from .types import MultiProvider


T = ta.TypeVar('T')
K = ta.TypeVar('K')
V = ta.TypeVar('V')


@dc.dataclass(frozen=True)
class SetBinding(MultiBinding[T], lang.Final):
    pass


@dc.dataclass(frozen=True)
class SetProvider(MultiProvider[ta.AbstractSet[T]], lang.Final):
    set_key: Key[ta.AbstractSet[T]]

    def __call__(self) -> ta.AbstractSet[T]:
        ret = set()
        bindings = Injector.current.get_bindings(Key(SetBinding[self.set_key.type], self.set_key.annotation))
        for binding in bindings:
            check.isinstance(binding, SetBinding)
            ret.add(binding.provide())
        return ret


@dc.dataclass(frozen=True)
class DictBinding(MultiBinding[T], lang.Final):
    assignment: K


@dc.dataclass(frozen=True)
class DictProvider(MultiProvider[ta.Mapping[K, V]], lang.Final):
    dict_key: Key[ta.Mapping[K, V]]

    def __call__(self) -> ta.Mapping[K, V]:
        ret = {}
        bindings = Injector.current.get_bindings(Key(DictBinding[self.dict_key.type], self.dict_key.annotation))
        for binding in bindings:
            check.isinstance(binding, DictBinding)
            check.not_in(binding.assignment, ret)
            ret[binding.assignment] = binding.provide()
        return ret
