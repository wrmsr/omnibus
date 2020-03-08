import threading
import typing as ta
import weakref

from . import check
from . import lang


lang.warn_unstable()


K = ta.TypeVar('K')
V = ta.TypeVar('V')


class NOT_SET(lang.Marker):
    pass


class AlreadyRegisteredException(Exception):
    pass


class Registry(ta.Mapping[K, V]):

    def __init__(
            self,
            *,
            lock: ta.Optional[lang.ContextManageable] = NOT_SET,
            weak: bool = False,
    ) -> None:
        super().__init__()

        self._weak = bool(weak)

        if lock is NOT_SET:
            self._lock = threading.RLock()
        elif lock is None:
            self._lock = lang.ContextManaged()
        else:
            self._lock = lock

        dct: ta.MutableMapping[K, V]
        if self._weak:
            dct = weakref.WeakValueDictionary()
        else:
            dct = {}
        self._dct = dct

    def __setitem__(self, k: K, v: V) -> None:
        self.register(k, v)

    def __getitem__(self, k: K) -> V:
        return self._dct[k]

    def __len__(self) -> int:
        return len(self._dct)

    def __iter__(self) -> ta.Iterator[K]:
        return iter(self._dct)

    def __contains__(self, o: object) -> bool:
        return o in self._dct

    def items(self) -> ta.AbstractSet[ta.Tuple[K, V]]:
        return self._dct.items()

    def keys(self) -> ta.AbstractSet[K]:
        return self._dct.keys()

    def values(self) -> ta.ValuesView[V]:
        return self._dct.values()

    def register_many(self, dct: ta.Mapping[K, V]) -> 'Registry[K, V]':
        with self._lock:
            for k, v in dct.items():
                check.not_none(k)

                try:
                    ov = self[k]
                except KeyError:
                    pass
                else:
                    raise AlreadyRegisteredException(k, v, ov)

                self._dct[k] = v

        return self

    def register(self, k: K, v: V) -> 'Registry[K, V]':
        check.not_none(k)
        return self.register_many({k: v})
