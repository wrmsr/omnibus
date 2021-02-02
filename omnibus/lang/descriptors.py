import abc
import functools
import typing as ta


BUILTIN_METHOD_DESCRIPTORS = (classmethod, staticmethod)


def is_method_descriptor(obj: ta.Any) -> bool:
    return isinstance(obj, (*BUILTIN_METHOD_DESCRIPTORS, _MethodDescriptor))


def unwrap_method_descriptors(fn: ta.Callable) -> ta.Callable:
    while is_method_descriptor(fn):
        fn = fn.__func__  # type: ignore  # noqa
    return fn


class _MethodDescriptorFlags(ta.NamedTuple):
    noinstance: bool
    nosubclass: bool
    callable: bool


_DEFAULT_METHOD_DESCRIPTOR_FLAGS = _MethodDescriptorFlags(*([False] * len(_MethodDescriptorFlags._fields)))


def _new_method_descriptor_flags(**kwargs) -> _MethodDescriptorFlags:
    return _DEFAULT_METHOD_DESCRIPTOR_FLAGS._replace(**kwargs)


def _merge_method_descriptor_flags(l: _MethodDescriptorFlags, *rs: _MethodDescriptorFlags) -> _MethodDescriptorFlags:
    for r in rs:
        l = _MethodDescriptorFlags(*[getattr(l, a) or getattr(r, a) for a in _MethodDescriptorFlags._fields])
    return l


class _MethodDescriptor:
    __func__: ta.ClassVar[ta.Callable]

    def __init__(
            self,
            fn: ta.Callable,
            *,
            _flags: _MethodDescriptorFlags = _DEFAULT_METHOD_DESCRIPTOR_FLAGS,
            **kwargs
    ):
        while True:
            if isinstance(fn, _MethodDescriptor):
                _flags = _merge_method_descriptor_flags(_flags, fn._flags)
                fn = fn.__func__
            elif isinstance(fn, BUILTIN_METHOD_DESCRIPTORS):
                fn = fn.__func__
            elif callable(fn):
                break
            else:
                raise TypeError(fn)

        if isinstance(self, BUILTIN_METHOD_DESCRIPTORS):
            super().__init__(fn, **kwargs)
        else:
            self.__func__ = fn
            super().__init__(**kwargs)

        functools.update_wrapper(self, self.__func__)
        self._flags = _flags
        self._flags_tup = tuple(_flags)

    _owner: ta.Optional[type] = None

    def __repr__(self):
        return f'{type(self).__name__}({self.__func__})'

    def _check_get(self, instance, owner):
        flags = self._flags

        if flags.noinstance:
            if instance is not None:
                raise TypeError(f'Cannot take instancemethod of {self.__func__}')

        if flags.nosubclass:
            _owner = self._owner
            if _owner is None:
                _owner = self._owner = [c for c in reversed(owner.__mro__) if self in c.__dict__.values()][0]
            if owner is not _owner:
                raise TypeError(f'Cannot access {self.__func__} of class {_owner} from class {owner}')

    @abc.abstractmethod
    def _get(self, instance, owner):
        raise NotImplementedError

    def __get__(self, instance, owner=None):
        if owner is not None:
            if instance is None:
                return self
            owner = instance.__class__

        self._check_get(instance, owner)
        return self._get(instance, owner)

    def __call__(self, *args, **kwargs):
        flags = self._flags

        if not flags.callable:
            raise TypeError(f'Cannot __call__ {self}')

        return self.__func__(*args, **kwargs)


class MethodDescriptor(_MethodDescriptor):
    def _get(self, instance, owner):
        return self.__func__.__get__(instance, owner)  # noqa


class ClassMethodDescriptor(_MethodDescriptor, classmethod):
    _get = classmethod.__get__


class StaticMethodDescriptor(_MethodDescriptor, staticmethod):
    _get = staticmethod.__get__


_MethodDescriptor._py__check_get = _MethodDescriptor._check_get  # noqa
_MethodDescriptor._py___get__ = _MethodDescriptor.__get__  # noqa
_MethodDescriptor._py___call__ = _MethodDescriptor.__call__  # noqa
MethodDescriptor._py__get = MethodDescriptor._get  # noqa

try:
    from .._ext.cy import lang as _cy
except ImportError:
    pass

else:
    _MethodDescriptor._check_get = _cy.__MethodDescriptor__check_get  # noqa
    _MethodDescriptor.__get__ = _cy.__MethodDescriptor___get__  # noqa
    _MethodDescriptor.__call__ = _cy.__MethodDescriptor___call__  # noqa
    MethodDescriptor._get = _cy._MethodDescriptor_func__get  # noqa


def _new_method_descriptor(fn: ta.Callable, **kwargs) -> _MethodDescriptor:
    if isinstance(fn, classmethod):
        return ClassMethodDescriptor(fn, **kwargs)
    elif isinstance(fn, staticmethod):
        return StaticMethodDescriptor(fn, **kwargs)
    else:
        kwargs['_flags'] = kwargs.get('_flags', _DEFAULT_METHOD_DESCRIPTOR_FLAGS)._replace(callable=True)  # noqa
        return MethodDescriptor(fn, **kwargs)


def _new_flags_method_descriptor(fn: ta.Callable, **kwargs) -> _MethodDescriptor:
    return _new_method_descriptor(fn, _flags=_new_method_descriptor_flags(**kwargs))


def nosubclass(fn):
    return _new_flags_method_descriptor(fn, nosubclass=True)


def noinstance(fn):
    return _new_flags_method_descriptor(fn, noinstance=True)


class _staticfunction(StaticMethodDescriptor):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not _staticfunction._check_flags(self._flags):
            raise TypeError

    @staticmethod
    def _check_flags(flags: _MethodDescriptorFlags) -> bool:
        return not flags.nosubclass and not flags.noinstance

    __get__ = staticmethod.__get__


def staticfunction(fn):
    return _staticfunction(fn, _flags=_new_method_descriptor_flags(callable=True))
