"""  # noqa
WATCH:
 - https://github.com/python/typing/issues/213 :|||

FIXME:
 - overhaul Protcol - https://www.python.org/dev/peps/pep-0544/
  - 3.8 only :|
  - kill @Protocol usage
 - lol, it's __subclasshook__ not __subclasscheck__
 - also threadlocal default? but can hopefully die after hook fix

TODO:
 - common _VirtualMeta, Protocol mandatory in bases, flatten like Intersection
 - 'Value' ? AnyVal equiv, runtime-present yet erased/non-instantiated, NewType+
  - usable for check - return NotEmpty[str] actually returns str at runtime but NotEmpty[T] in type
   - virtual intersection really - T -> Intersection[T, NotEmpty]
    - implying ta.Intersection still needs to exist not just class I(..., lang.classes.virtual.Intersection): ... :/
     - class HashableT(ta.Generic[T], Hashable, Intersection): ...
     - def check.hashable(obj: T) -> Hashable[T] .. no


https://zio.dev/docs/howto/howto_use_layers

https://github.com/python/mypy/commit/ad6c717c408c6ab6d21a488ab1f89930448ae83c


class IntMod3(int):

    def __new__(cls, val):
        if not isinstance(val, int) or val % 3 != 0:
            raise TypeError(val)
        return val

    def __instancecheck__(self, instance):
        return isinstance(instance, int) and instance % 3 == 0

    @classmethod
    def all(cls) -> ta.Iterator[int]:
        for i in itertools.count():
            if i % 3 == 0:
                yield i
"""
import abc
import threading
import typing as ta

from .restrict import make_abstract
from .restrict import NotInstantiable


Ty = ta.TypeVar('Ty', bound=type)


class _ProtocolMeta(abc.ABCMeta):

    def __new__(mcls, name, bases, namespace):
        if 'Protocol' not in globals():
            return super().__new__(mcls, name, bases, namespace)
        if Protocol not in bases:
            raise TypeError

        for k, v in list(namespace.items()):
            absv = make_abstract(v)
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
            if cls is not kls:
                return super(kls, cls).__subclasshook__(subclass)
            if get_missing_reqs(subclass):
                return False
            if user_subclasshook is not None:
                ret = user_subclasshook(cls, subclass)
            else:
                ret = super(kls, cls).__subclasshook__(subclass)
            return True if ret is NotImplemented else ret

        namespace['__subclasshook__'] = classmethod(__subclasshook__)

        kls = super().__new__(abc.ABCMeta, name, tuple(b for b in bases if b is not Protocol), namespace)
        return kls


class Protocol(metaclass=_ProtocolMeta):

    def __new__(cls, impl: Ty) -> Ty:
        raise TypeError

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

    # FIXME: USE __SUBCLASSHOOK__ NOT THIS.
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
