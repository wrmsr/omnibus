import typing as ta


T = ta.TypeVar('T')


def identity(obj: T) -> T:
    return obj


cdef class constant:

    cdef public object obj

    def __init__(self, obj):
        self.obj = obj

    def __call__(self):
        return self.obj


def is_none(obj: ta.Any) -> bool:
    return obj is None


def is_not_none(obj: ta.Any) -> bool:
    return obj is not None


def cmp(l: ta.Any, r: ta.Any) -> int:
    return (l > r) - (l < r)
