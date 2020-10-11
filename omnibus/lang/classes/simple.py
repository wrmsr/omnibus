import abc
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

    def update(self, m: ta.Mapping[K, V], **kwargs: V) -> None:  # type: ignore
        for k, v in m.items():
            self[k] = v
        for k, v in kwargs.items():  # type: ignore
            self[k] = v


class _InnerMeta(abc.ABCMeta):

    def __get__(self, instance, owner=None):
        if instance is not None:
            def bound(*args, **kwargs):
                obj = self.__new__(self, *args, **kwargs)
                obj.__outer__ = instance
                obj.__init__(*args, **kwargs)
                return obj
            return bound
        return self


class Inner(ta.Generic[T], metaclass=_InnerMeta):

    __outer__: ta.Optional[T] = None

    def __init__(self, *args, **kwargs) -> None:
        if self.__outer__ is None:
            raise TypeError
        super().__init__(*args, **kwargs)  # type: ignore

    @property
    def _outer(self) -> T:
        if self.__outer__ is None:
            raise TypeError
        return self.__outer__
