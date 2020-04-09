import sys
import typing as ta


T = ta.TypeVar('T')


def _global_property(fn):
    if not fn.__name__.startswith('_'):
        raise NameError(fn)
    sys._getframe(1).f_globals[fn.__name__[1:]] = fn
    return fn


class Property(ta.Generic[T]):
    pass
