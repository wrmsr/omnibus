import functools
import typing as ta

from .base import Property


T = ta.TypeVar('T')


class ValueNotSetException(ValueError):
    pass


class ValueAlreadySetException(ValueError):
    pass


class SetOnceProperty(Property[T]):

    def __init__(self, attr_name: str = None) -> None:
        super().__init__()

        self._attr_name = attr_name or '__%s_%x_value' % (type(self).__name__, id(self))

    def __get__(self, instance, owner):
        if instance is None:
            return self
        try:
            return getattr(instance, self._attr_name)
        except AttributeError:
            raise ValueNotSetException

    def __set__(self, instance, value):
        try:
            getattr(instance, self._attr_name)
        except AttributeError:
            setattr(instance, self._attr_name, value)
        else:
            raise ValueAlreadySetException

    def __delete__(self, instance):
        raise TypeError('Operation not supported')


def set_once(attr_name: str = None):
    return SetOnceProperty(attr_name)


class ClassProperty(Property[T]):

    def __init__(
            self,
            func: ta.Callable[[ta.Any], T],
    ) -> None:
        super().__init__()

        functools.update_wrapper(self, func)
        self._func = self._unwrap(func)

    def __get__(self, obj, cls=None) -> T:
        return self._func(cls)


def class_(fn: ta.Callable[..., T]) -> T:
    return ClassProperty(fn)
