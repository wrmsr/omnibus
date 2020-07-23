from dataclasses import FrozenInstanceError
from libcpp cimport bool


MISSING = object()


cdef class Descriptor:

    cdef public str attr
    cdef public object default_
    cdef public bool frozen
    cdef public str name

    def __init__(
            self,
            str attr,
            *,
            object default_ = MISSING,
            bool frozen = False,
            str name = None,
            **kwargs
    ):
        super().__init__(**kwargs)

        self.attr = attr
        self.default_ = default_
        self.frozen = frozen
        self.name = name

    def __set_name__(self, owner, name):
        if self.name is None:
            self.name = name

    def __get__(self, instance, owner):
        if instance is not None:
            return getattr(instance, self.attr)
        elif self.default_ is not MISSING:
            return self.default_
        else:
            raise AttributeError(self.name)

    def __set__(self, instance, value):
        if self.frozen:
            raise FrozenInstanceError(f'cannot assign to field {self.name!r}')
        setattr(instance, self.attr, value)

    def __delete__(self, instance):
        if self.frozen:
            raise FrozenInstanceError(f'cannot delete field {self.name!r}')
        delattr(instance, self.attr)
