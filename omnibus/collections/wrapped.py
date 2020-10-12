"""
TODO:
 - __add__ handle 'cannot add tuple and list' somehow - functools.__wrapped__ equiv?
  - do as set/frozenset __or__ - lval wins
"""
import functools
import itertools
import typing as ta

from .. import lang


TF = ta.TypeVar('TF')
TT = ta.TypeVar('TT')
KF = ta.TypeVar('KF')
KT = ta.TypeVar('KT')
VF = ta.TypeVar('VF')
VT = ta.TypeVar('VT')


class Wrapped(lang.Abstract):
    pass


@functools.total_ordering
class WrappedSequence(ta.MutableSequence[TT], ta.Generic[TF, TT], Wrapped, lang.Final):

    def __init__(
            self,
            encoder: ta.Callable[[TF], TT],
            decoder: ta.Callable[[TT], TF],
            target: ta.MutableSequence[TF],
    ) -> None:
        super().__init__()

        if not callable(encoder):
            raise TypeError(encoder)
        if not callable(decoder):
            raise TypeError(decoder)
        if target is None:
            raise TypeError(target)
        self._encoder = encoder
        self._decoder = decoder
        self._target = target

    def __repr__(self) -> str:
        return '%s(%r)' % (type(self).__name__, self._target)

    def __add__(self, o: object) -> ta.MutableSequence[TT]:
        return WrappedSequence(
            self._encoder,
            self._decoder,
            [*self._target, *map(self._encoder, o)],  # type: ignore
        )

    def __contains__(self, x: object) -> bool:
        return self._encoder(x) in self._target  # type: ignore

    def __delitem__(self, idx: ta.Union[int, slice]) -> None:
        del self._target[idx]

    def __eq__(self, o: object) -> bool:
        if not len(self._target) == len(o):  # type: ignore
            return False
        for l, r in zip(self, o):  # type: ignore
            if l != r:
                return False
        return True

    def __getitem__(self, i: ta.Union[int, slice]) -> TT:  # type: ignore
        return self._decoder(self._target[i])  # type: ignore

    def __iadd__(self, it: ta.Iterable[TT]) -> ta.MutableSequence[TT]:  # type: ignore
        self._target += map(self._encoder, it)  # type: ignore
        return self

    def __iter__(self) -> ta.Iterator[TT]:
        return map(self._decoder, self._target)  # type: ignore

    def __len__(self) -> int:
        return len(self._target)

    def __lt__(self, s: ta.Sequence[ta.Any]) -> bool:
        missing = object()
        for l, r in itertools.zip_longest(self, s, fillvalue=missing):
            if l is missing:
                return False
            elif r is missing:
                return True
            elif l < r:
                return True
            elif r < l:
                return False
        return False

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

    def __reversed__(self) -> ta.Iterator[TT]:
        return map(self._decoder, reversed(self._target))  # type: ignore

    def __setitem__(self, idx: ta.Union[int, slice], obj: ta.Union[TT, ta.Iterable[TT]]) -> None:
        if isinstance(idx, int):
            self._target[idx] = self._encoder(obj)
        elif isinstance(idx, slice):
            self._target[idx] = map(self._encoder, obj)  # type: ignore
        else:
            raise TypeError(idx)

    def append(self, obj: TT) -> None:
        self._target.append(self._encoder(obj))  # type: ignore

    def clear(self) -> None:
        self._target.clear()

    def count(self, x: ta.Any) -> int:
        return self._target.count(self._encoder(x))

    def extend(self, it: ta.Iterable[TT]) -> None:
        self._target.extend(map(self._encoder, it))  # type: ignore

    def index(self, x: ta.Any, *args, **kwargs) -> int:  # type: ignore
        return self._target.index(self._encoder(x), *args, **kwargs)

    def insert(self, idx: int, o: TT) -> None:
        self._target.insert(idx, self._encoder(o))  # type: ignore

    def pop(self, idx: int = -1) -> TT:
        return self._target.pop(idx)  # type: ignore

    def remove(self, obj: TT) -> None:
        self._target.remove(self._encoder(obj))  # type: ignore

    def reverse(self) -> None:
        self._target.reverse()


# @functools.total_ordering
# class WrappedSet(ta.MutableSet[TT], ta.Generic[TF, TT], Wrapped, lang.Final):
#     """
#     '__iand__',
#     '__ior__',
#     '__isub__',
#     '__iter__',
#     '__ixor__',
#     '__len__',
#     '__rand__',
#     '__ror__',
#     '__rsub__',
#     '__rxor__',
#     'add',
#     'clear',
#     'discard',
#     'pop',
#     'remove',
#     """
#
#     def __init__(
#             self,
#             encoder: ta.Callable[[TF], TT],
#             decoder: ta.Callable[[TT], TF],
#             target: ta.MutableSet[TF],
#     ) -> None:
#         super().__init__()
#
#         self._encoder = check.callable(encoder)
#         self._decoder = check.callable(decoder)
#         self._target = check.not_none(target)
#
#     def __repr__(self) -> str:
#         return '%s(%r)' % (type(self).__name__, self._target)
#
#     def __and__(self, s: ta.AbstractSet[ta.Any]) -> ta.AbstractSet[TT]:
#         return WrappedSet(
#             self._encoder,
#             self._decoder,
#             self._target & set(map(self._encoder(s))),
#         )
#
#     def __contains__(self, x: object) -> bool:
#         return self._encoder(x) in self._target
#
#     def __eq__(self, o: object) -> bool:
#         if not len(self._target) == len(o):
#             return False
#         if not all(i in o for i in self):
#             return False
#         if not all(i in self for i in o):
#             return False
#         return True
#
#     def __iter__(self) -> ta.Iterator[TT]:
#         return map(self._decoder, self._target)
#
#     def __len__(self) -> int:
#         return len(self._target)
#
#     def __lt__(self, s: ta.AbstractSet[ta.Any]) -> bool:
#         missing = object()
#         for l, r in itertools.zip_longest(self, s, fillvalue=missing):
#             if l is missing:
#                 return False
#             elif r is missing:
#                 return True
#             elif l < r:
#                 return True
#             elif r < l:
#                 return False
#         return False
#
#     def __ne__(self, o: object) -> bool:
#         return self._target != o
#
#     def __or__(self, s: ta.AbstractSet[TT]) -> ta.AbstractSet[TT]:
#         return self._target | s
#
#     def __sub__(self, s: ta.AbstractSet[ta.Any]) -> ta.AbstractSet[TT]:
#         return self._target - s
#
#     def __xor__(self, s: ta.AbstractSet[TT]) -> ta.AbstractSet[TT]:
#         return self._target ^ s
#
#     def isdisjoint(self, s: ta.Iterable[ta.Any]) -> bool:
#         return self._target.isdisjoint(s)


# class WrappedMapping(ta.MutableMapping[KT, VT], ta.Generic[KF, KT, VF, VT], Wrapped, lang.Final):
#     """
#     '__contains__',
#     '__delitem__',
#     '__eq__',
#     '__getitem__',
#     '__iter__',
#     '__len__',
#     '__ne__',
#     '__reversed__',
#     '__setitem__',
#     'clear',
#     'get',
#     'items',
#     'keys',
#     'pop',
#     'popitem',
#     'setdefault',
#     'update',
#     'values',
#     """
#
#     def __init__(
#             self,
#             target: ta.MutableMapping[KF, VF],
#     ) -> None:
#         super().__init__()
#
#         self._target = check.not_none(target)
#
#     def __repr__(self) -> str:
#         return '%s(%r)' % (type(self).__name__, self._target)
#
#     def __contains__(self, o: object) -> bool:
#         return o in self._target
#
#     def __eq__(self, o: object) -> bool:
#         return self._target == o
#
#     def __getitem__(self, k: K) -> V:
#         return self._target[k]
#
#     def __iter__(self) -> ta.Iterator[T]:
#         return iter(self._target)
#
#     def __ne__(self, o: object) -> bool:
#         return self._target != o
#
#     def __len__(self) -> int:
#         return len(self._target)
#
#     def get(self, k: K, default=None) -> ta.Optional[V]:
#         return self._target.get(k)
#
#     def items(self) -> ta.AbstractSet[ta.Tuple[K, V]]:
#         return self._target.items()
#
#     def keys(self) -> ta.AbstractSet[K]:
#         return self._target.keys()
#
#     def values(self) -> ta.ValuesView[V]:
#         return self._target.values()
