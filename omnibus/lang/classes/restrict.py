"""
TODO:
 - resurrect Interface is_abstract - ellipsis, raise, return
 - Markers become ta.Literals after dropping 3.7? or same just diff anns
 - eagerly abstract - if Abstract not explicitly in baseclass list of new subclasses enforce concreteness eagerlly
  - .. **make this default**?
 - frozen_after_init?
"""
import abc
import functools
import types
import typing as ta
import weakref


T = ta.TypeVar('T')


_DISABLE_CHECKS = False


def make_abstract(obj: T) -> T:
    if callable(obj):
        return ta.cast(T, abc.abstractmethod(obj))
    elif isinstance(obj, property):
        return ta.cast(T, property(
            abc.abstractmethod(obj.fget) if obj.fget is not None else None,  # type: ignore
            abc.abstractmethod(obj.fset) if obj.fset is not None else None,  # type: ignore
            abc.abstractmethod(obj.fdel) if obj.fdel is not None else None,  # type: ignore
        ))
    elif isinstance(obj, (classmethod, staticmethod)):
        return ta.cast(T, type(obj)(abc.abstractmethod(obj.__func__)))
    else:
        return obj


class Abstract(abc.ABC):
    __slots__ = ()

    def __forceabstract__(self):
        raise TypeError

    setattr(__forceabstract__, '__isabstractmethod__', True)

    def __init_subclass__(cls, **kwargs) -> None:
        if Abstract in cls.__bases__:
            cls.__forceabstract__ = Abstract.__forceabstract__  # type: ignore
        else:
            cls.__forceabstract__ = False  # type: ignore

        super().__init_subclass__(**kwargs)  # type: ignore

        if not _DISABLE_CHECKS and Abstract not in cls.__bases__:
            ams = {a for a, o in cls.__dict__.items() if is_abstract_method(o)}
            seen = set(cls.__dict__)
            for b in cls.__bases__:
                ams.update(set(getattr(b, '__abstractmethods__', [])) - seen)
                seen.update(dir(b))
            if ams:
                raise TypeError(f'Cannot subclass abstract class {cls.__name__} with abstract methods {", ".join(map(str, sorted(ams)))}')  # noqa


abstract = abc.abstractmethod


def is_abstract_method(obj: ta.Any) -> bool:
    return bool(getattr(obj, '__isabstractmethod__', False))


def is_abstract_class(obj: ta.Any) -> bool:
    return bool(getattr(obj, '__abstractmethods__', [])) or (
        isinstance(obj, type) and (
            Abstract in obj.__bases__ or (
                Abstract in obj.__mro__ and
                getattr(obj.__dict__.get('__forceabstract__', None), '__isabstractmethod__', False)
            )
        )
    )


def is_abstract(obj: ta.Any) -> bool:
    return is_abstract_method(obj) or is_abstract_class(obj)


class _AbstractSkeleton:

    def pass_(self):
        pass

    def ellipsis(self):
        ...

    def return_none(self):
        return None

    def raise_not_implemented_error_type(self):
        raise NotImplementedError

    def raise_not_implemented_error_instance(self):
        raise NotImplementedError()

    FUNCTIONS = {
        pass_,
        ellipsis,
        return_none,
        raise_not_implemented_error_type,
        raise_not_implemented_error_instance,
    }


def is_abstract_impl(obj: ta.Any) -> bool:
    if is_abstract(obj):
        return True
    elif isinstance(obj, property):
        obj = obj.fget
    elif isinstance(obj, (classmethod, staticmethod)):
        obj = obj.__func__
    elif not isinstance(obj, types.FunctionType):
        return False
    for skelfn in _AbstractSkeleton.FUNCTIONS:
        if (
                obj.__code__.co_code == skelfn.__code__.co_code and
                obj.__code__.co_consts == skelfn.__code__.co_consts
        ):
            return True
    return False


class _InterfaceMeta(abc.ABCMeta):

    def __new__(mcls, name, bases, namespace):
        if 'Interface' not in globals():
            return super().__new__(mcls, name, bases, namespace)
        if Interface not in bases:
            raise TypeError
        for k, v in list(namespace.items()):
            if not isinstance(v, (types.FunctionType, property, classmethod, staticmethod)) or not is_abstract_impl(v):
                continue
            absv = make_abstract(v)
            if absv is not v:
                namespace[k] = absv
        bases = tuple(b for b in bases if b is not Interface)
        return super().__new__(abc.ABCMeta, name, bases, namespace)


class Interface(metaclass=_InterfaceMeta):
    __slots__ = ()


class FinalException(TypeError):

    def __init__(self, _type: ta.Type) -> None:
        super().__init__()

        self._type = _type

    def __repr__(self) -> str:
        return f'{type(self).__name__}({self._type})'


class Final(Abstract):
    __slots__ = ()

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)

        abstracts = set()
        for base in cls.__bases__:
            if base is Abstract:
                raise FinalException(base)
            elif base is Final:
                continue
            elif Final in base.__mro__:
                raise FinalException(base)
            else:
                abstracts.update(getattr(base, '__abstractmethods__', []))

        for a in abstracts:
            try:
                v = cls.__dict__[a]
            except KeyError:
                raise FinalException(a)
            if is_abstract(v):
                raise FinalException(a)


class SealedException(TypeError):

    def __init__(self, _type) -> None:
        super().__init__()

        self._type = _type

    def __repr__(self) -> str:
        return f'{type(self).__name__}({self._type})'


class Sealed:
    __slots__ = ()

    def __init_subclass__(cls, **kwargs) -> None:
        for base in cls.__bases__:
            if base is not Abstract:
                if Sealed in base.__bases__:
                    if cls.__module__ != base.__module__:
                        raise SealedException(base)
        super().__init_subclass__(**kwargs)  # type: ignore


class PackageSealed:
    __slots__ = ()

    def __init_subclass__(cls, **kwargs) -> None:
        for base in cls.__bases__:
            if base is not Abstract:
                if PackageSealed in base.__bases__:
                    if cls.__module__.split('.')[:-1] != base.__module__.split('.')[:-1]:
                        raise SealedException(base)
        super().__init_subclass__(**kwargs)  # type: ignore


class NotInstantiable(Abstract):
    __slots__ = ()

    def __new__(cls, *args, **kwargs) -> ta.NoReturn:  # type: ignore
        raise TypeError


class NotPicklable:
    __slots__ = ()

    def __getstate__(self) -> ta.NoReturn:
        raise TypeError

    def __setstate__(self, state) -> ta.NoReturn:
        raise TypeError


_MARKER_NAMESPACE_KEYS: ta.Optional[ta.Set[str]] = None


class _MarkerMeta(abc.ABCMeta):

    def __new__(mcls, name, bases, namespace):
        global _MARKER_NAMESPACE_KEYS
        if _MARKER_NAMESPACE_KEYS is None:
            if not (namespace.get('__module__') == __name__ and name == 'Marker'):
                raise RuntimeError
            _MARKER_NAMESPACE_KEYS = set(namespace)
        else:
            if set(namespace) - _MARKER_NAMESPACE_KEYS:
                raise TypeError('Markers must not include contents. Did you mean to use Namespace?')
            if Final not in bases:
                bases += (Final,)
        return super().__new__(mcls, name, bases, namespace)

    def __instancecheck__(self, instance):
        return instance is self

    def __repr__(cls) -> str:
        return f'<{cls.__name__}>'


class Marker(NotInstantiable, metaclass=_MarkerMeta):
    """A marker."""

    __slots__ = ()


class _Namespace(Final):

    def __mro_entries__(self, bases, **kwargs):
        return (Final, NotInstantiable)


Namespace = _Namespace()


class AttrAccessForbiddenException(Exception):

    def __init__(self, name: str = None, *args, **kwargs) -> None:
        super().__init__(*((name,) if name is not None else ()), *args, **kwargs)  # type: ignore
        self.name = name


class AccessForbiddenDescriptor:

    def __init__(self, name: str = None) -> None:
        super().__init__()

        self._name = name

    def __set_name__(self, owner: ta.Type, name: str) -> None:
        if self._name is None:
            self._name = name
        elif name != self._name:
            raise NameError(name)

    def __get__(self, instance, owner=None):
        raise AttrAccessForbiddenException(self._name)


def access_forbidden():
    return AccessForbiddenDescriptor()


class Override:

    def __init__(self, fn: ta.Callable) -> None:
        super().__init__()

        self._fn = fn
        functools.update_wrapper(self, fn)
        self.__call__ = fn.__call__  # type: ignore

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self._fn!r})'

    def __set_name__(self, owner: ta.Type, name: str) -> None:
        if not any(hasattr(b, name) for b in owner.__bases__):
            raise TypeError(name)

    def __get__(self, instance: ta.Any, owner: ta.Optional[ta.Type] = None) -> ta.Callable:
        return self._fn.__get__(instance, owner)  # type: ignore

    def __call__(self, *args, **kwargs):
        return self._fn(*args, **kwargs)


def override(fn: T) -> T:
    return ta.cast(T, Override(fn))  # type: ignore


_FINALS: ta.MutableSet[ta.Any] = weakref.WeakSet()


def final(obj):
    _FINALS.add(obj)
    return obj


def check_finals(cls: type, bcls: type) -> type:
    if bcls not in cls.__mro__:
        raise TypeError(cls, bcls)
    c = 0
    for a, o in bcls.__dict__.items():
        if o not in _FINALS:
            continue
        c += 1
        if getattr(cls, a) is not o:
            raise TypeError(cls, bcls, a)
    if not c:
        raise TypeError('no finals', bcls)
    return cls
