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


DEF _method_descriptor_flag_noinstance  = 0
DEF _method_descriptor_flag_nosubclass   = 1
DEF _method_descriptor_flag_callable    = 2


def __MethodDescriptor__check_get(self, instance, owner):
    flags_tup: tuple = self._flags_tup

    if flags_tup[_method_descriptor_flag_noinstance]:
        if instance is not None:
            raise TypeError(f'Cannot take instancemethod of {self.__func__}')

    if flags_tup[_method_descriptor_flag_nosubclass]:
        _owner = self._owner
        if _owner is None:
            _owner = self._owner = [c for c in reversed(owner.__mro__) if self in c.__dict__.values()][0]
        if owner is not _owner:
            raise TypeError(f'Cannot access {self.__func__} of class {_owner} from class {owner}')


def __MethodDescriptor___get__(self, instance, owner=None):
    if owner is not None:
        if instance is None:
            return self
        owner = instance.__class__

    self._check_get(instance, owner)
    return self._get(instance, owner)


def __MethodDescriptor___call__(self, *args, **kwargs):
    flags_tup: tuple = self._flags_tup

    if not flags_tup[_method_descriptor_flag_callable]:
        raise TypeError(f'Cannot __call__ {self}')

    return self.__func__(*args, **kwargs)


def _MethodDescriptor_func__get(self, instance, owner):
    return self.__func__.__get__(instance, owner)
