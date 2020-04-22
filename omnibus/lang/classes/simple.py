import abc
import functools
import typing as ta


T = ta.TypeVar('T')
K = ta.TypeVar('K')
V = ta.TypeVar('V')


def singleton(*args, **kwargs) -> ta.Callable[[ta.Type[T]], ta.Callable[..., T]]:
    def inner(cls):
        obj = cls(*args, **kwargs)
        obj.__name__ = cls.__name__
        return obj
    return inner


class SimpleMetaDict(dict):

    def update(self, m: ta.Mapping[K, V], **kwargs: V) -> None:
        for k, v in m.items():
            self[k] = v
        for k, v in kwargs.items():
            self[k] = v


class _staticfunction(staticmethod):
    """
    Allows calling @staticmethods within a classbody. Vanilla @staticmethods are not callable:

        TypeError: 'staticmethod' object is not callable
    """

    def __init__(self, fn: ta.Callable) -> None:
        super().__init__(fn)
        functools.update_wrapper(self, fn)

    def __repr__(self) -> str:
        return f'{type(self).__name__}({self.__func__})'

    def __call__(self, *args, **kwargs):
        return self.__func__(*args, **kwargs)


staticfunction = staticmethod
globals()['staticfunction'] = _staticfunction


class _InnerMeta(abc.ABCMeta):

    def __get__(self, instance, owner):
        if instance is not None:
            def bound(*args, **kwargs):
                obj = self.__new__(self, *args, **kwargs)
                obj.__outer__ = instance
                obj.__init__(*args, **kwargs)
                return obj
            return bound
        return self


class Inner(ta.Generic[T], metaclass=_InnerMeta):

    __outer__: T = None

    def __init__(self, *args, **kwargs) -> None:
        if self.__outer__ is None:
            raise TypeError
        super().__init__(*args, **kwargs)

    @property
    def _outer(self) -> T:
        if self.__outer__ is None:
            raise TypeError
        return self.__outer__
