import dataclasses as dc
import typing as ta

from ... import defs


class PyFieldDescriptor:

    def __init__(
            self,
            attr: str,
            *,
            default_: ta.Any = dc.MISSING,
            frozen: bool = None,
            name: str = False,
            pre_set: ta.Callable[[object], None] = None,
            post_set: ta.Callable[[object], None] = None,
    ) -> None:
        super().__init__()

        self._attr = attr
        self._default_ = default_
        self._frozen = frozen
        self._name = name
        self._pre_set = pre_set
        self._post_set = post_set

    defs.repr('attr', 'name')
    defs.getter('attr', 'default_', 'frozen', 'name', 'pre_set', 'post_set')

    def __set_name__(self, owner, name):
        if self._name is None:
            self._name = name

    def __get__(self, instance, owner=None):
        if instance is not None:
            try:
                return getattr(instance, self._attr)
            except AttributeError:
                pass
        if self._default_ is not dc.MISSING:
            return self._default_
        raise AttributeError(self._name)

    def __set__(self, instance, value):
        if self._frozen:
            raise dc.FrozenInstanceError(f'cannot assign to field {self._name!r}')
        if self._pre_set is not None:
            self._pre_set(value)
        setattr(instance, self._attr, value)
        if self._post_set is not None:
            self._post_set(value)

    def __delete__(self, instance):
        if self._frozen:
            raise dc.FrozenInstanceError(f'cannot delete field {self._name!r}')
        delattr(instance, self._attr)


FieldDescriptor = PyFieldDescriptor

try:
    from ..._ext.cy.dataclasses import FieldDescriptor as CyFieldDescriptor
except ImportError:
    pass
else:
    FieldDescriptor = CyFieldDescriptor
