import typing as ta


T = ta.TypeVar('T')


class Property(ta.Generic[T]):

    @classmethod
    def _unwrap(cls, fn):
        if isinstance(fn, property):
            if fn.fset is not None or fn.fdel is not None:
                raise TypeError(fn)
            fn = fn.fget
        if callable(fn):
            return fn
        else:
            raise TypeError(fn)
