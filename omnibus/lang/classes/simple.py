import abc
import functools
import threading
import typing as ta


T = ta.TypeVar('T')
K = ta.TypeVar('K')
V = ta.TypeVar('V')


def instance(*args, **kwargs) -> ta.Callable[[ta.Type[T]], ta.Callable[..., T]]:
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


_SINGLETON_INSTANCE_ATTR = '__Singleton_INSTANCE'
_SINGLETON_LOCK = threading.RLock()


def _set_singleton_instance(inst):
    cls = type(inst)
    if _SINGLETON_INSTANCE_ATTR in cls.__dict__:
        raise TypeError(cls)

    inst.__init__()
    old_init = cls.__init__

    @functools.wraps(old_init)
    def new_init(self):
        if type(self) is not cls:
            old_init(self)  # noqa

    setattr(cls, '__init__', new_init)
    setattr(cls, _SINGLETON_INSTANCE_ATTR, inst)

    return inst


class Singleton:

    def __new__(cls):
        return cls.__dict__[_SINGLETON_INSTANCE_ATTR]

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        _set_singleton_instance(super().__new__(cls))  # noqa


class LazySingleton:

    def __new__(cls):
        try:
            return cls.__dict__[_SINGLETON_INSTANCE_ATTR]
        except KeyError:
            pass
        with _SINGLETON_LOCK:
            try:
                return cls.__dict__[_SINGLETON_INSTANCE_ATTR]
            except KeyError:
                pass
            return _set_singleton_instance(super().__new__(cls))
