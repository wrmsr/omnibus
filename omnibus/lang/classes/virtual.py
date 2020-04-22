"""
TODO:
 - refresh protocol
  - typing_extensions? no.
  - common _VirtualMeta, Protocol mandatory in bases, flatten like Intersection
"""
import abc
import threading
import typing as ta

from .restrict import _make_abstract
from .restrict import NotInstantiable


Ty = ta.TypeVar('Ty', bound=type)


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


_INTERSECTION_CHECKING = threading.local()
_INTERSECTION_CHECKING._value = False


class _IntersectionMeta(abc.ABCMeta):

    def __subclasscheck__(self, subclass):
        if _INTERSECTION_CHECKING._value:
            return False
        try:
            _INTERSECTION_CHECKING._value = True
            for base in self.__bases__:
                if base is Intersection:
                    continue
                if not issubclass(subclass, base):
                    return False
            return True
        finally:
            _INTERSECTION_CHECKING._value = False

    def __new__(mcls, name, bases, namespace, **kwargs):
        if 'Intersection' not in globals():
            return super().__new__(mcls, name, bases, namespace, **kwargs)
        if Intersection not in bases:
            raise TypeError

        new_bases = []
        seen = set()
        for base in bases:
            if base is Intersection or base in seen:
                continue
            if isinstance(base, _IntersectionMeta):
                for sub in base.__bases__:
                    if sub is Intersection or sub in seen:
                        continue
                    if Intersection in sub.__mro__ or isinstance(type(sub), _IntersectionMeta):
                        raise TypeError(sub)
                    new_bases.append(sub)
                    seen.add(sub)
            else:
                new_bases.append(base)
                seen.add(base)
        new_bases.append(Intersection)

        return super().__new__(mcls, name, tuple(new_bases), namespace, **kwargs)


class Intersection(NotInstantiable, metaclass=_IntersectionMeta):
    pass