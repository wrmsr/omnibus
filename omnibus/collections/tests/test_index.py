"""
TODO:
 - boost::MultiIndex - sorted.py?
  - https://www.boost.org/doc/libs/1_73_0/libs/multi_index/doc/reference/index.html
   - Index reference
   - Ordered indices
   - Ranked indices
   - Hashed indices
   - Sequenced indices
   - Random access indices
   - Key Extraction
"""
import dataclasses as dc
import operator as op
import typing as ta

import pytest

from ..identity import IdentitySet


T = ta.TypeVar('T')
K = ta.TypeVar('K')
Key = ta.Callable[[T], K]


class Index(ta.Generic[T], ta.Collection[T]):

    class _KeyEntry(ta.NamedTuple, ta.Generic[T, K]):
        name: ta.Optional[str]
        key: Key[T, K]
        map: ta.MutableMapping[K, T]

    def __init__(
            self,
            primary_key: Key[T, K],
            keys: ta.Optional[ta.Mapping[str, Key[T, K]]] = None,
    ) -> None:
        super().__init__()

        self._keys: ta.MutableMapping[ta.Optional[str], Index._KeyEntry[T, K]] = {}
        self._items: ta.MutableSet[T] = IdentitySet()

        self.add_key(None, primary_key)
        if keys:
            for kn, k in keys.items():
                self.add_key(kn, k)

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self) -> ta.Iterator[T]:
        return iter(self._items)

    def __contains__(self, item: T) -> bool:
        return item in self._items

    def __getitem__(self, k: ta.Any) -> T:
        return self._keys[None].map[k]

    def add_key(self, name: ta.Optional[str], key: Key[T, K]) -> None:
        if name in self._keys:
            raise NameError(name)

        dct = {}
        for item in self._items:
            k = key(item)
            if k in dct:
                raise KeyError(k)
            dct[k] = item

        self._keys[name] = Index._KeyEntry(name, key, dct)

    def add(self, item: T) -> None:
        self.add_all([item])

    def add_all(self, items: ta.Iterable[T]) -> None:
        items = list(items)

        for item in items:
            if item is None or item in self._items:
                raise ValueError(item)
            for ke in self._keys.values():
                k = ke.key(item)
                if k in ke.map:
                    raise KeyError(k)

        for item in items:
            for ke in self._keys.values():
                k = ke.key(item)
                ke.map[k] = item

            self._items.add(item)


@dc.dataclass(frozen=True)
class Thing:
    id: int
    name: str
    value: float


def test_index():
    idx: Index[Thing] = Index(op.attrgetter('id'))
    print(idx)

    ts = [
        Thing(0, 'zero', .0),
        Thing(1, 'one', .1),
        Thing(2, 'two', .2),
    ]
    idx.add_all(ts)

    print(idx[0])
    print(idx[1])
    print(idx[2])
    with pytest.raises(KeyError):
        print(idx[3])
