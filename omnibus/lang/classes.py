import abc
import functools
import sys
import types
import typing as ta

from .lang import new_type


T = ta.TypeVar('T')
Ty = ta.TypeVar('Ty', bound=type)
K = ta.TypeVar('K')
V = ta.TypeVar('V')
ExceptionT = ta.TypeVar('ExceptionT', bound=Exception)


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


def _make_abstract(obj: T) -> T:
    if callable(obj):
        return abc.abstractmethod(obj)
    elif isinstance(obj, property):
        return property(
            abc.abstractmethod(obj.fget) if obj.fget is not None else None,
            abc.abstractmethod(obj.fset) if obj.fset is not None else None,
            abc.abstractmethod(obj.fdel) if obj.fdel is not None else None,
        )
    elif isinstance(obj, classmethod) or isinstance(obj, staticmethod):
        return type(obj)(abc.abstractmethod(obj))
    else:
        return obj


class ProtocolException(TypeError):

    def __init__(self, reqs: ta.Set[str]) -> None:
        super().__init__()
        self._reqs = reqs

    def __repr__(self) -> str:
        return f'{type(self).__name__}({self._reqs})'


class _ProtocolMeta(abc.ABCMeta):

    def __new__(mcls, name, bases, namespace):
        for k, v in list(namespace.items()):
            absv = _make_abstract(v)
            if absv is not v:
                namespace[k] = absv

        reqs = {k: v for k, v in namespace.items() if getattr(v, '__isabstractmethod__', False)}
        user_subclasshook = namespace.pop('__subclasshook__', None)

        def get_missing_reqs(cls):
            reqset = set(reqs)
            for mro_cls in cls.__mro__:
                reqset -= set(mro_cls.__dict__)
            return reqset

        def __subclasshook__(cls, subclass):
            if get_missing_reqs(subclass):
                return False
            if user_subclasshook is not None:
                ret = user_subclasshook(cls, subclass)
            else:
                ret = super().__subclasshook__(subclass)
            return True if ret is NotImplemented else ret

        namespace['__subclasshook__'] = classmethod(__subclasshook__)

        def __protocolcheck__(cls, subclass):
            missing_reqs = get_missing_reqs(subclass)
            if missing_reqs:
                raise ProtocolException(missing_reqs)
            try:
                chain = super().__protocolcheck__
            except AttributeError:
                pass
            else:
                chain(subclass)

        namespace['__protocolcheck__'] = classmethod(__protocolcheck__)

        kls = super().__new__(mcls, name, bases, namespace)
        return kls


class Protocol(metaclass=_ProtocolMeta):

    def __new__(cls, impl: Ty) -> Ty:
        cls.__protocolcheck__(impl)
        return impl

    def __init__(self, *args, **kwarg) -> None:
        raise TypeError


class Descriptor(Protocol):

    def __get__(self, instance, owner):
        raise NotImplementedError


class Abstract(abc.ABC):

    def __forceabstract__(self):
        raise TypeError

    setattr(__forceabstract__, '__isabstractmethod__', True)

    def __init_subclass__(cls, **kwargs) -> None:
        if Abstract in cls.__bases__:
            cls.__forceabstract__ = Abstract.__forceabstract__
        else:
            cls.__forceabstract__ = False
        super().__init_subclass__(**kwargs)


abstract = abc.abstractmethod


def is_abstract(obj: ta.Any) -> bool:
    return bool(getattr(obj, '__abstractmethods__', [])) or (
        isinstance(obj, type) and
        issubclass(obj, Abstract) and
        getattr(obj.__dict__.get('__forceabstract__', None), '__isabstractmethod__', False)
    )


class _InterfaceMeta(abc.ABCMeta):

    def __new__(mcls, name, bases, namespace):
        if 'Interface' not in globals():
            return super().__new__(mcls, name, bases, namespace)
        if Interface not in bases:
            raise TypeError
        for k, v in list(namespace.items()):
            absv = _make_abstract(v)
            if absv is not v:
                namespace[k] = absv
        bases = tuple(b for b in bases if b is not Interface)
        return super().__new__(abc.ABCMeta, name, bases, namespace)


class Interface(metaclass=_InterfaceMeta):
    pass


class FinalException(TypeError):

    def __init__(self, _type: ta.Type) -> None:
        super().__init__()

        self._type = _type

    def __repr__(self) -> str:
        return f'{type(self).__name__}({self._type})'


class Final(Abstract):

    def __init_subclass__(cls, **kwargs) -> None:
        for base in cls.__bases__:
            if base is not Abstract and base is not Final and issubclass(base, Final):
                raise FinalException(base)
        super().__init_subclass__(**kwargs)


class SealedException(TypeError):

    def __init__(self, _type) -> None:
        super().__init__()

        self._type = _type

    def __repr__(self) -> str:
        return f'{type(self).__name__}({self._type})'


class Sealed(Abstract):

    def __init_subclass__(cls, **kwargs) -> None:
        for base in cls.__bases__:
            if base is not Abstract:
                if Sealed in base.__bases__ and cls.__module__ != base.__module__:
                    raise SealedException(base)
        super().__init_subclass__(**kwargs)


ExceptionInfo = ta.Tuple[ta.Type[ExceptionT], ExceptionT, types.TracebackType]


def _extension_ignored_attrs() -> ta.Set[str]:
    class C:
        pass
    return set(C.__dict__)


_EXTENSION_IGNORED_ATTRS = _extension_ignored_attrs()


class _ExtensionMeta(type):

    def __new__(mcls, name, bases, namespace, *, _bind=None):
        if not bases:
            return super().__new__(mcls, name, bases, namespace)
        if _bind is not None:
            if bases != (Extension,):
                raise TypeError
            return super().__new__(mcls, name, bases, {'__extensionbind__': _bind, **namespace})

        newbases = []
        binds = []
        for base in bases:
            if issubclass(base, Extension):
                if base.__bases__ != (Extension,) or not hasattr(base, '__extensionbind__'):
                    raise TypeError
                binds.append(base.__extensionbind__)
                del base.__extensionbind__
            else:
                newbases.append(base)

        cls = super().__new__(mcls, name, tuple(newbases), namespace)
        newns = {}
        for mrocls in reversed(cls.__mro__):
            if mrocls is object:
                continue
            for k, v in mrocls.__dict__.items():
                if k not in _EXTENSION_IGNORED_ATTRS:
                    newns[k] = v

        for bind in binds:
            for k, v in newns.items():
                if k in bind.__dict__:
                    raise NameError(k)
                setattr(bind, k, v)

        return None

    def __getitem__(self, bind):
        return new_type(f'{self.__name__}[{bind!r}]', (self,), {}, _bind=bind)


class Extension(metaclass=_ExtensionMeta):
    pass


class Override:

    def __init__(self, fn: ta.Callable) -> None:
        super().__init__()

        self._fn = fn
        functools.update_wrapper(self, fn)
        self.__call__ = fn.__call__

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self._fn!r})'

    def __set_name__(self, owner: ta.Type, name: str) -> None:
        if not any(hasattr(b, name) for b in owner.__bases__):
            raise TypeError(name)

    def __get__(self, instance: ta.Any, owner: ta.Optional[ta.Type]) -> ta.Callable:
        return self._fn.__get__(instance, owner)

    def __call__(self, *args, **kwargs):
        return self._fn(*args, **kwargs)


def override(fn: T) -> T:
    return ta.cast(T, Override(fn))


class NotInstantiable(Abstract):

    def __new__(cls, *args, **kwargs) -> ta.NoReturn:
        raise TypeError


class _MarkerMeta(abc.ABCMeta):

    def __new__(mcls, name, bases, namespace):
        if not (namespace.get('__module__') == __name__ and name == 'Marker'):
            if Final not in bases:
                bases += (Final,)
        return super().__new__(mcls, name, bases, namespace)

    def __repr__(cls) -> str:
        return f'<{cls.__name__}>'


class Marker(NotInstantiable, metaclass=_MarkerMeta):
    pass


class _Namespace(Final):

    def __mro_entries__(self, bases, **kwargs):
        return (Final, NotInstantiable)


Namespace = _Namespace()


class Picklable(Protocol):

    def __getstate__(self):
        raise NotImplementedError

    def __setstate__(self, state):
        raise NotImplementedError


class NotPicklable:

    def __getstate__(self) -> ta.NoReturn:
        raise TypeError

    def __setstate__(self, state) -> ta.NoReturn:
        raise TypeError


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


_MIXIN_IGNORED_ATTRS = {
    '__module__',
    '__qualname__',
}


class _MixinMeta(type):

    def __new__(mcls, name, bases, namespace):
        if 'Mixin' not in globals():
            return super().__new__(mcls, name, bases, namespace)
        try:
            return namespace['__mixin__']
        except KeyError:
            raise RuntimeError('Must call Mixin.capture in class body')


class Mixin(metaclass=_MixinMeta):

    @staticmethod
    def capture() -> None:
        frame = sys._getframe(1)
        body, globals = frame.f_code, frame.f_globals

        def mixin():
            locals = sys._getframe(1).f_locals
            if not all(k in locals for k in _MIXIN_IGNORED_ATTRS):
                raise RuntimeError('Must invoke mixin from class definition body')
            restores = {k: locals[k] for k in _MIXIN_IGNORED_ATTRS}
            exec(body, globals, locals)
            locals.update(restores)

        frame.f_locals['__mixin__'] = mixin


class AttrAccessForbiddenException(Exception):

    def __init__(self, name: str = None, *args, **kwargs) -> None:
        super().__init__(*((name,) if name is not None else ()), *args, **kwargs)
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

    def __get__(self, instance, owner):
        raise AttrAccessForbiddenException(self._name)


def access_forbidden():
    return AccessForbiddenDescriptor()
