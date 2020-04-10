import typing as ta


len_ = len


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
