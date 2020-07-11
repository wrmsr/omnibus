"""  # noqa
WATCH:
 - https://github.com/python/typing/issues/213 :|||

FIXME:
 - overhaul Protocol
  - make like Interface
  - https://www.python.org/dev/peps/pep-0544/
  - 3.8 only :|
  - kill @Protocol usage

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
import types
import typing as ta

from .restrict import make_abstract
from .restrict import NotInstantiable
from .restrict import Final


Ty = ta.TypeVar('Ty', bound=type)


def _make_not_instantiable():
    def __new__(cls, *args, **kwargs):
        raise TypeError(cls)

    def __init__(self, *args, **kwargs):
        raise TypeError(self)

    return {
        '__new__': __new__,
        '__initT__': __init__,
    }


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

        namespace.update(_make_not_instantiable())

        kls = super().__new__(abc.ABCMeta, name, tuple(b for b in bases if b is not Protocol), namespace)
        return kls


class Protocol(metaclass=_ProtocolMeta):
    pass


def protocol_check(proto: type) -> ta.Callable[[Ty], Ty]:
    def inner(cls):
        if not issubclass(cls, proto):
            raise TypeError(cls)
        return cls
    # if not issubclass(type(proto), _ProtocolMeta):
    #     raise TypeError(proto)
    return inner


class Descriptor(Protocol):

    def __get__(self, instance, owner=None):
        raise NotImplementedError


class Picklable(Protocol):

    def __getstate__(self):
        raise NotImplementedError

    def __setstate__(self, state):
        raise NotImplementedError


class _IntersectionMeta(abc.ABCMeta):

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

        is_checking = threading.local()

        def __subclasshook__(self, subclass):
            try:
                value = is_checking.value
            except AttributeError:
                value = is_checking.value = False
            if value:
                return False
            try:
                is_checking.value = True
                for base in self.__bases__:
                    if base is Intersection:
                        continue
                    if not issubclass(subclass, base):
                        return False
                return True
            finally:
                is_checking.value = False

        namespace['__subclasshook__'] = classmethod(__subclasshook__)

        namespace.update(_make_not_instantiable())

        return super().__new__(mcls, name, tuple(new_bases), namespace, **kwargs)


class Intersection(metaclass=_IntersectionMeta):
    pass


class Callable(NotInstantiable, Final):

    @classmethod
    def __instancecheck__(cls, instance):
        return callable(instance)

    @classmethod
    def __subclasscheck__(cls, subclass):
        if not hasattr(subclass, '__call__'):
            return False
        call = subclass.__call__
        if isinstance(call, types.MethodWrapperType) and call.__self__ is subclass:
            return False
        return True
