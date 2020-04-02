class Callable:
    def __call__(self, *args, **kwds): ...


class Hashable:
    def __hash__(self): ...


class Iterable:
    def __iter__(self): ...


class Iterator(Iterable):
    def __next__(self): ...
    def __iter__(self): ...


class Reversible(Iterable):
    def __reversed__(self): ...


class Generator(Iterator):
    def __next__(self): ...
    def send(self, value): ...
    def throw(self, typ, val=None, tb=None): ...
    def close(self): ...


class Sized:
    def __len__(self): ...


class Container:
    def __contains__(self, x): ...


class Collection(Sized, Iterable, Container):
    pass


# region Async


class Awaitable:
    def __await__(self): ...


class Coroutine(Awaitable):
    def send(self, value): ...
    def throw(self, typ, val=None, tb=None): ...
    def close(self): ...


class AsyncIterable:
    def __aiter__(self): ...


class AsyncIterator(AsyncIterable):
    async def __anext__(self): ...
    def __aiter__(self): ...


class AsyncGenerator(AsyncIterator):
    async def __anext__(self): ...
    async def asend(self, value): ...
    async def athrow(self, typ, val=None, tb=None): ...
    async def aclose(self): ...


# endregion


# region Sequence


class Sequence(Reversible, Collection):
    def __getitem__(self, index): ...
    def __iter__(self): ...
    def __contains__(self, value): ...
    def __reversed__(self): ...
    def index(self, value, start=0, stop=None): ...
    def count(self, value): ...


class ByteString(Sequence):
    pass


class MutableSequence(Sequence):
    def __setitem__(self, index, value): ...
    def __delitem__(self, index): ...
    def insert(self, index, value): ...
    def append(self, value): ...
    def clear(self): ...
    def reverse(self): ...
    def extend(self, values): ...
    def pop(self, index=-1): ...
    def remove(self, value): ...
    def __iadd__(self, values): ...


# endregion


# region Set


class Set(Collection):
    def __le__(self, other): ...
    def __lt__(self, other): ...
    def __gt__(self, other): ...
    def __ge__(self, other): ...
    def __eq__(self, other): ...
    def __and__(self, other): ...
    __rand__ = __and__
    def isdisjoint(self, other): ...
    def __or__(self, other): ...
    __ror__ = __or__
    def __sub__(self, other): ...
    def __rsub__(self, other): ...
    def __xor__(self, other): ...
    __rxor__ = __xor__


class MutableSet(Set):
    def add(self, value): ...
    def discard(self, value): ...
    def remove(self, value): ...
    def pop(self): ...
    def clear(self): ...
    def __ior__(self, it): ...
    def __iand__(self, it): ...
    def __ixor__(self, it): ...
    def __isub__(self, it): ...


# endregion


# region Mapping


class Mapping(Collection):
    def __getitem__(self, key): ...
    def get(self, key, default=None): ...
    def __contains__(self, key): ...
    def keys(self): ...
    def items(self): ...
    def values(self): ...
    def __eq__(self, other): ...
    __reversed__ = None


class MappingView(Sized):
    def __len__(self): ...
    def __repr__(self): ...


class KeysView(MappingView, Set):
    def __contains__(self, key): ...
    def __iter__(self): ...


class ItemsView(MappingView, Set):
    def __contains__(self, item): ...
    def __iter__(self): ...


class ValuesView(MappingView, Collection):
    def __contains__(self, value): ...
    def __iter__(self): ...


class MutableMapping(Mapping):
    def __setitem__(self, key, value): ...
    def __delitem__(self, key): ...
    def pop(self, key, default=None): ...
    def popitem(self): ...
    def clear(self): ...
    def update(self, other=(), **kwds): ...
    def setdefault(self, key, default=None): ...


# endregion
