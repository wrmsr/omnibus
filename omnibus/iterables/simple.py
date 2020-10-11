import itertools
import typing as ta


T = ta.TypeVar('T')


len_ = len


chain = itertools.chain.from_iterable


def void(it, exception=lambda item: RuntimeError('Unreachable', item)):
    for item in it:
        raise exception(item)


def len(it) -> int:
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


def unique_list(it: ta.Iterable[T]) -> ta.List[T]:
    seen = set()
    lst = []
    for e in it:
        if e not in seen:
            lst.append(e)
            seen.add(e)
    return lst


def split_filter(
        pred: ta.Callable[[T], bool],
        it: ta.Iterable[T],
) -> ta.Tuple[ta.Sequence[T], ta.Sequence[T]]:
    true = []
    false = []
    for e in it:
        if pred(e):
            true.append(e)
        else:
            false.append(e)
    return true, false
