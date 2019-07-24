import abc
import collections
import functools
import heapq
import io
import itertools
import operator
import os
import random
import sys
import time
import typing as ta

from . import callables
from . import check
from . import lang
from . import properties
from . import toolz


T = ta.TypeVar('T')


map_ = map
filter_ = filter
zip_ = zip


_BUILDER_FNS = []


class IterableTransform(lang.Abstract):

    @abc.abstractmethod
    def __call__(self, items):  # -> items
        raise NotImplementedError

    def __pos__(self):
        return compose(self, eager)

    def __neg__(self):
        return compose(self, lazy)

    def __invert__(self):
        return compose(self, flatten)

    def __and__(self, other):
        return chain(self, other)

    def __rand__(self, other):
        return chain(other, self)

    def __or__(self, other):
        return compose(self, other)

    def __ror__(self, other):
        return compose(other, self)

    def __mul__(self, other):
        return compose(self, map(other))

    def __matmul__(self, other):
        return compose(self, filter(other))


def alias(*bases):
    return callables.alias(*(bases + (IterableTransform,)))


def constructor(*bases, **kwargs):
    builder = kwargs.pop('builder', False)
    if kwargs:
        raise TypeError(kwargs)

    def inner(fn):
        fn = callables.constructor(*(bases + (IterableTransform,)))(fn)
        if builder:
            _BUILDER_FNS.append(fn)
        return fn
    return inner


def void(it, exception=lambda item: RuntimeError('Unreachable', item)):
    for item in it:
        raise exception(item)


def ilen(it) -> int:
    c = 0
    for _ in it:
        c += 1
    return c


def with_(it):
    with it:
        yield from it


Readable = ta.Callable[[int], ta.Any]


def read(readable: Readable, size=65536):
    while True:
        obj = readable(size)
        if not obj:
            break
        yield obj


@alias()
def flatten(items):
    return itertools.chain.from_iterable(items)


@constructor(builder=True)
def compose(*children):
    all(check.callable(child) for child in children)
    children = list(flatten(child.args if isinstance(child, compose) else [child]
                            for child in children))

    def run(items):
        for child in children:
            items = child(items)
        return items
    return run


@alias()
def nop(items):
    return items


@alias()
def lazy(items):
    yield from items


@alias()
def eager(items):
    return items if isinstance(items, (list, tuple)) else list(items)


@alias()
def discard(items):
    for _ in items:
        pass
    return
    yield


@constructor(builder=True)
def apply(function):
    check.callable(function)

    def run(items):
        for item in items:
            function(item)
            yield item

    return run


@constructor(builder=True)
def map(function):
    return functools.partial(map_, check.callable(function))


@constructor(builder=True)
def filter(predicate):
    return functools.partial(filter_, check.callable(predicate))


@constructor(builder=True)
def filter_false(predicate):
    return functools.partial(itertools.filterfalse, check.callable(predicate))


@alias()
def zip(*its):
    return zip_(*its)


@alias()
def zip_same_length(*its):
    missing = object()
    for t in itertools.zip_longest(*its):
        if missing in t:
            raise ValueError(its)
        yield t


@constructor()
def type_filter(type):
    return filter(lambda obj: isinstance(obj, type))


@constructor()
def type_remove(type):
    return filter(lambda obj: not isinstance(obj, type))


@constructor(builder=True)
def flat_map(function):
    return compose(map(function), flatten)


@constructor()
def unreachable(exception=lambda item: RuntimeError('Unreachable', item)):
    def run(items):
        for item in items:
            raise exception(item)
        return
        yield
    return run


@constructor()
def chain(*children):
    all(check.callable(child) for child in children)

    def run(items):
        for child in children:
            yield from child(items)

    return run


@constructor()
def permute(*children):
    all(check.callable(child) for child in children)

    def run(items):
        for permutation in itertools.permutations(children):
            yield from compose(*permutation)(items)

    return run


@constructor()
def interleave(*children):
    all(check.callable(child) for child in children)

    def run(items):
        for item in items:
            for child in children:
                yield child((item,))

    return run


@constructor()
def broadcast(*children):
    all(check.callable(child) for child in children)
    return compose(interleave(*children), flatten)


@constructor(builder=True)
def guard(predicate, exception_type=ValueError):
    def run(items):
        for item in items:
            if not predicate(item):
                raise exception_type(item)
            yield item
    return run


@constructor()
def type_guard(type, exception_type=TypeError):
    return guard(lambda item: isinstance(item, type), exception_type=exception_type)


@constructor()
def chunk(capacity, weigh=callables.const(1)):
    check.callable(weigh)

    def run(items):
        chunk_weight = 0
        chunk = []
        for item in items:
            item_weight = weigh(item)
            if chunk_weight + item_weight > capacity:
                yield chunk
                chunk = []
                chunk_weight = 0
            chunk.append(item)
            chunk_weight += item_weight
        if chunk:
            yield chunk

    return run


@constructor(builder=True)
def route(router):
    check.callable(router)

    def run(items):
        for target, group in itertools.groupby(items, router):
            if target is None:
                yield group
            else:
                yield target(group)

    return run


@constructor(builder=True)
def sorted_route(router, target_order=()):
    check.callable(router)

    def run(items):
        item_lists_by_target = {}
        for item in items:
            item_lists_by_target.setdefault(router(item), []).append(item)
        for target in target_order:
            try:
                target_items = item_lists_by_target.pop(target)
            except KeyError:
                continue
            if target is None:
                yield target_items
            else:
                yield target(target_items)
        for target, target_items in item_lists_by_target.items():
            if target is None:
                yield target_items
            else:
                yield target(target_items)

    return run


def _unpack_pairs(items):
    check.arg(len(items) % 2 == 0)
    return items[::2], items[1::2]


@constructor(builder=True)
def match(*predicates_and_targets, **kwargs):
    if not kwargs.pop('strict', False):
        predicates_and_targets += (callables.const(True), None)
    predicates, targets = _unpack_pairs(predicates_and_targets)
    predicate_target_pairs = list(zip_(predicates, targets))
    check.arg(all(callable(predicate) for predicate in predicates))
    check.arg(all(callable(target) or target is None for target in targets))

    def router(item):
        for route_predicate, target in predicate_target_pairs:
            if route_predicate(item):
                return target
        raise ValueError(item)

    if kwargs.pop('sorted', False):
        kwargs.setdefault('target_order', targets)
        route_ = sorted_route
    else:
        route_ = route
    return route_(router, **kwargs)


@constructor(builder=True)
def type_match(*types_and_targets, **kwargs):
    target_types, targets = _unpack_pairs(types_and_targets)
    check.arg(all(isinstance(o, type) or (isinstance(o, tuple) and all(isinstance(oi, type) for oi in o))
                  for o in target_types))

    def predicate(target_type, obj):
        return isinstance(obj, target_type)

    predicates = [functools.partial(predicate, target_type) for target_type in target_types]
    return match(*list(flatten(zip_(predicates, targets))), **kwargs)


@constructor(builder=True)
def flat_match(*args, **kwargs):
    return compose(match(*args, **kwargs), flatten)


@constructor(builder=True)
def flat_type_match(*args, **kwargs):
    return compose(type_match(*args, **kwargs), flatten)


@constructor(builder=True)
def map_type(type, fn):
    def run(items):
        for item in items:
            if isinstance(item, type):
                yield fn(item)
            else:
                yield item
    return run


@constructor(builder=True)
def flat_map_type(type, fn):
    def run(items):
        for item in items:
            if isinstance(item, type):
                for out in fn(item):
                    yield out
            else:
                yield item
    return run


@constructor(builder=True)
def apply_type(type, fn):
    def run(items):
        for item in items:
            if isinstance(item, type):
                fn(item)
            yield item
    return run


@constructor(builder=True)
def map_types(*types_and_fns):
    types, fns = _unpack_pairs(types_and_fns)
    return compose(*[map_type(type, fn) for type, fn in zip_(types, fns)])


@constructor(builder=True)
def flat_map_types(*types_and_fns):
    types, fns = _unpack_pairs(types_and_fns)
    return compose(*[flat_map_type(type, fn) for type, fn in zip_(types, fns)])


@constructor(builder=True)
def apply_types(*types_and_fns):
    types, fns = _unpack_pairs(types_and_fns)
    return compose(*[apply_type(type, fn) for type, fn in zip_(types, fns)])


@constructor()
def context_managed(wrapped, fn):
    def run(in_items):
        with fn(in_items):
            yield from wrapped(in_items)
    return run


@constructor(builder=True)
def chunked_flat_map(function, capacity, **kwargs):
    return compose(chunk(capacity, **kwargs), map(function), flatten)


@constructor(builder=True)
def map_randomly(function, chance):
    def run(item):
        if random.random() < chance:
            item = function(item)
        return item
    return map(run)


@constructor(builder=True)
def map_periodically(function, interval):
    last_run_time = None

    def run(item):
        nonlocal last_run_time
        if last_run_time is None:
            last_run_time = time.time()
            return item
        time_since_last_run = time.time() - last_run_time
        if time_since_last_run < interval:
            return item
        item = function(item)
        last_run_time = time.time()
        return item

    return map(run)


@constructor(builder=True)
def map_every_nth(function, n):
    remaining = n

    def run(item):
        nonlocal remaining
        remaining -= 1
        if remaining < 1:
            remaining = n
            item = function(item)
        return item

    return map(run)


@constructor(builder=True)
def apply_randomly(function, chance):
    def inner(item):
        function(item)
        return item
    return map_randomly(inner, chance)


@constructor(builder=True)
def apply_periodically(function, interval):
    def inner(item):
        function(item)
        return item
    return map_periodically(inner, interval)


@constructor(builder=True)
def apply_every_nth(function, n):
    def inner(item):
        function(item)
        return item
    return map_every_nth(inner, n)


class Deduplicated(ta.NamedTuple):
    num_seen: int
    num_deduplicated: int
    item: ta.Any
    item_keys: ta.Collection[ta.Any]
    output: ta.Collection[ta.Any]


@constructor()
def deduplicate(keys=callables.tuple, verbose=False):
    """Deduplicates items where keys is a callable returning for a given item a tuple of values by
    which the item is to be deduplicated. Implemented such that the final item in the tuple will be
    placed in a set, not a dict, for memory efficiency - as such the highest cardinality key component
    should be last in the key tuple.

    When verbose is not truthy simply yields deduplicated items. When verbose is truthy yields for
    each item a dict of the following keys:
      'num_seen' - the number of deduplicated items yielded
      'num_deduplicated' - the number of duplicate items not yielded
      'item' - the item
      'item_keys' - the keys by which the item was deduplicated
      'output' - an empty tuple if the item was a duplicate, otherwise a tuple containing the item
    """

    num_seen = 0
    num_deduplicated = 0
    seen = {}

    def inner(item):
        nonlocal num_seen, num_deduplicated, seen

        item_keys = keys(item)
        check.state(item_keys, message='Keys must not be empty')
        item_keys = (None,) + item_keys
        dst = seen

        for item_key in item_keys[:-3]:
            check.state(isinstance(dst, dict), message='Keys must always be the same length.')
            try:
                dst = dst[item_key]
            except KeyError:
                next_dst = {}
                dst[item_key] = next_dst
                dst = next_dst

        item_key = item_keys[-2]
        try:
            dst = dst[item_key]
        except KeyError:
            next_dst = set()
            dst[item_key] = next_dst
            dst = next_dst

        check.state(isinstance(dst, set), message='Keys must always be the same length.')
        item_key = item_keys[-1]
        if item_key in dst:
            output = ()
            num_deduplicated += 1
        else:
            dst.add(item_key)
            output = (item,)
            num_seen += 1

        return Deduplicated(
            num_seen,
            num_deduplicated,
            item,
            item_keys[1:],
            output,
        )

    if verbose:
        return map(inner)
    else:
        return compose(
            map(inner),
            map(lambda dct: dct.output),
            flatten)


@constructor()
def merge_on(function):
    check.callable(function)

    def inner(its):
        indexed_its = [((function(item), it_idx, item)
                        for it_idx, item in zip_(itertools.repeat(it_idx), it))
                       for it_idx, it in enumerate(its)]

        grouped_indexed_its = itertools.groupby(
            heapq.merge(*indexed_its),
            key=lambda item_tuple: item_tuple[0])

        return ((fn_item, [(it_idx, item) for _, it_idx, item in grp])
                for fn_item, grp in grouped_indexed_its)

    return inner


@constructor()
def expand_indexed_pairs(width=None, default=None):
    def inner(seq):
        width_ = width
        if width_ is None:
            width_ = (max(idx for idx, _ in seq) + 1) if seq else 0
        result = [default] * width_
        for idx, value in seq:
            if idx < width_:
                result[idx] = value
        return result
    return inner


@constructor()
def cut_lines(max_buf_size=10 * 1024 * 1024, Buf=io.StringIO):
    def inner(chunks):
        buf = Buf()
        for chunk in chunks:
            if os.linesep not in chunk:
                buf.write(chunk)
            else:
                line_chunks = chunk.splitlines()
                buf.write(line_chunks[0])
                yield buf.getvalue()
                if buf.tell() > max_buf_size:
                    buf.close()
                    buf = Buf()
                else:
                    buf.seek(0, 0)
                    buf.truncate()
                for i in range(1, len(line_chunks) - 1):
                    yield line_chunks[i]
                buf.write(line_chunks[-1])
        if buf.tell() > 0:
            yield buf.getvalue()
    return inner


@alias()
def multi_combinations(*its: ta.Iterable[T]) -> ta.Iterable[ta.Sequence[T]]:
    if not its:
        return
    it, *rest = its
    if not rest:
        for item in it:
            yield [item]
        return
    for item in it:
        for suffix in multi_combinations(*rest):
            yield [item] + suffix  # noqa


_BuilderMethod = collections.namedtuple('_BuilderAtt', 'fn args kwargs')
_BUILDER_METHOD_ATTR = '__iterable_transform_builder_method__'


def builder():
    def inner(cls):
        if '_filter' in cls.__dict__:
            raise AttributeError('_filter')

        methods = []
        seen = set()
        for scls in cls.__mro__:
            try:
                scls_methods = getattr(scls, _BUILDER_METHOD_ATTR)
            except AttributeError:
                continue
            for name, method in scls_methods:
                if name not in seen:
                    seen.add(name)
                    methods.append((name, method))
        if not methods:
            raise TypeError('Must have at least one builder method')

        @properties.cached
        def _filter(self):
            lst = []
            for name, method in methods:
                lst.append(method.fn(*(method.args + (getattr(self, name),)), **method.kwargs))
            return compose(*lst)
        cls._filter = _filter

        def __call__(self, *args, **kwargs):
            return self._filter(*args, **kwargs)
        # FIXME: allow overriding
        cls.__call__ = __call__

        return cls

    return inner


def _bind_builder(fn):
    def outer(*args, **kwargs):
        def inner(meth):
            cls_dct = sys._getframe(1).f_locals
            methods = cls_dct.setdefault(_BUILDER_METHOD_ATTR, [])
            if meth.__name__ in methods:
                raise AttributeError(meth.__name__)
            methods.append((meth.__name__, _BuilderMethod(fn, args, kwargs)))
            return meth
        return inner
    setattr(builder, fn.__name__, outer)


for _fn in _BUILDER_FNS:
    _bind_builder(_fn)


@constructor()
def sliding_window(n: int):
    def inner(it):
        return toolz.sliding_window(n, it)
    return inner


class PeekIterator(ta.Iterator[T]):

    def __init__(self, it: ta.Iterator[T]) -> None:
        super().__init__()

        self._it = it
        self._pos = -1

    def __iter__(self) -> ta.Iterator[T]:
        return self

    @property
    def done(self) -> bool:
        try:
            self.peek()
            return False
        except StopIteration:
            return True

    def __next__(self) -> T:
        if hasattr(self, '_next_item'):
            self._item = self._next_item
            del self._next_item
        else:
            try:
                self._item = next(self._it)
            except StopIteration:
                raise
        self._pos += 1
        return self._item

    def peek(self) -> T:
        if hasattr(self, '_next_item'):
            return self._next_item
        try:
            self._next_item = next(self._it)
        except StopIteration:
            raise
        return self._next_item

    def next_peek(self) -> T:
        next(self)
        return self.peek()

    def takewhile(self, fn):
        while fn(self.peek()):
            yield next(self)

    def skipwhile(self, fn):
        while fn(self.peek()):
            next(self)

    def takeuntil(self, fn):
        return self.takewhile(toolz.compose(operator.not_, fn))

    def skipuntil(self, fn):
        self.skipwhile(toolz.compose(operator.not_, fn))

    def takethrough(self, pos):
        return self.takewhile(lambda _: self._pos < pos)

    def skipthrough(self, pos):
        self.skipwhile(lambda _: self._pos < pos)

    def taketo(self, pos):
        return self.takethrough(pos - 1)

    def skipto(self, pos):
        self.skipthrough(pos - 1)


class ProxyIterator(ta.Iterator[T]):

    def __init__(self, fn) -> None:
        self._fn = fn

    def __iter__(self) -> ta.Iterator[T]:
        return self

    def __next__(self) -> T:
        return self._fn()


class PrefetchIterator(ta.Iterator[T]):

    def __init__(self, fn: ta.Callable[[], T] = None) -> None:
        super().__init__()

        self._fn = fn
        self._deque = collections.deque()

    def __iter__(self) -> ta.Iterator[T]:
        return self

    def push(self, item) -> None:
        self._deque.append(item)

    def __next__(self) -> T:
        try:
            return self._deque.popleft()
        except IndexError:
            if self._fn is None:
                raise StopIteration
        return self._fn()


class RetainIterator(ta.Iterator[T]):

    def __init__(self, fn: ta.Callable[[], T]) -> None:
        super().__init__()

        self._fn = fn
        self._deque = collections.deque()

    def __iter__(self) -> ta.Iterator[T]:
        return self

    def pop(self) -> None:
        self._deque.popleft()

    def __next__(self) -> T:
        item = self._fn()
        self._deque.append(item)
        return item


def unzip(it: ta.Iterable[T], width: int = None) -> ta.List:
    if width is None:
        if not isinstance(it, PeekIterator):
            it = PeekIterator(it)
        try:
            width = len(it.peek())
        except StopIteration:
            return []

    its = []

    def next_fn(idx):
        if not next_fn.running:
            raise StopIteration
        try:
            items = next(it)
        except StopIteration:
            next_fn.running = False
            raise
        for item_idx, item in enumerate(items):
            its[item_idx].push(item)
        return next(its[idx])

    next_fn.running = True
    its.extend(PrefetchIterator(functools.partial(next_fn, idx)) for idx in range(width))
    return its
