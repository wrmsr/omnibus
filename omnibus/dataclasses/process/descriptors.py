import abc
import dataclasses as dc
import typing as ta

from ... import defs


_CYTHON_ENABLED = True


class AbstractFieldDescriptor(abc.ABC):

    def __init__(
            self,
            *,
            default_: ta.Any = dc.MISSING,
            frozen: bool = None,
            name: str = False,
            pre_set: ta.Callable[[object, object], None] = None,
            post_set: ta.Callable[[object, object], None] = None,
    ) -> None:
        super().__init__()

        self._default_ = default_
        self._frozen = frozen
        self._name = name
        self._pre_set = pre_set
        self._post_set = post_set

    defs.repr('name')
    defs.getter('default_', 'frozen', 'name', 'pre_set', 'post_set')

    def __set_name__(self, owner, name):
        if self._name is None:
            self._name = name

    def __get__(self, instance, owner=None):
        if instance is not None:
            try:
                return self._get(instance)
            except AttributeError:
                pass
        if self._default_ is not dc.MISSING:
            return self._default_
        raise AttributeError(self._name)

    @abc.abstractmethod
    def _get(self, instance):
        raise NotImplementedError

    def __set__(self, instance, value):
        if self._frozen:
            raise dc.FrozenInstanceError(f'cannot assign to field {self._name!r}')
        if self._pre_set is not None:
            value = self._pre_set(instance, value)
        self._set(instance, value)
        if self._post_set is not None:
            self._post_set(instance, value)

    @abc.abstractmethod
    def _set(self, instance, value):
        raise NotImplementedError

    def __delete__(self, instance):
        if self._frozen:
            raise dc.FrozenInstanceError(f'cannot delete field {self._name!r}')
        self._del(instance)

    @abc.abstractmethod
    def _del(self, instance):
        raise NotImplementedError


class PyFieldDescriptor(AbstractFieldDescriptor):

    def __init__(
            self,
            attr: str,
            **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        self._attr = attr

    defs.repr('attr', 'name')
    defs.getter('attr')

    def _get(self, instance):
        return getattr(instance, self._attr)

    def _set(self, instance, value):
        setattr(instance, self._attr, value)

    def _del(self, instance):
        delattr(instance, self._attr)


FieldDescriptor = PyFieldDescriptor

if _CYTHON_ENABLED:
    try:
        from ..._ext.cy.dataclasses import FieldDescriptor as CyFieldDescriptor
    except ImportError:
        pass
    else:
        FieldDescriptor = CyFieldDescriptor
