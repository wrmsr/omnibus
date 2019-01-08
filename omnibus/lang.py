import abc
import collections.abc
import concurrent.futures
import contextlib
import contextvars
import datetime
import enum
import functools
import importlib
import re
import sys
import time
import types
import typing as ta
import weakref

import pkg_resources


T = ta.TypeVar('T')
Ty = ta.TypeVar('T', bound=ta.Type)
K = ta.TypeVar('K')
V = ta.TypeVar('V')
Self = ta.TypeVar('Self')
EnumT = ta.TypeVar('EnumT', bound=enum.Enum)
ExceptionT = ta.TypeVar('ExceptionT', bound=Exception)
IteratorTOrT = ta.Union[ta.Iterator[T], T]
BytesLike = ta.Union[bytes, bytearray]
CallableT = ta.TypeVar('CallableT', bound=ta.Callable)

_NOT_SET = object()


def cls_dct_fn(offset=1):
    def outer(fn):
        @functools.wraps(fn)
        def inner(*args, **kwargs):
            try:
                cls_dct = kwargs.pop('cls_dct')
            except KeyError:
                cls_dct = sys._getframe(offset).f_locals
            return fn(cls_dct, *args, **kwargs)
        return inner
    return outer


@cls_dct_fn()
def public(cls_dct, target, *names: str):
    __all__ = cls_dct.setdefault('__all__', [])
    subtargets = ta.cast(list, target if isinstance(target, tuple) else (target,))
    for subtarget in subtargets:
        subnames = names or (subtarget.__name__,)
        for subname in subnames:
            if subname in cls_dct or subname in __all__:
                raise NameError(subname)
            cls_dct[subname] = target
            __all__.append(subname)
    return target


@cls_dct_fn()
def public_as(cls_dct, *names):
    def inner(target):
        return public(target, *names, cls_dct=cls_dct)
    return inner


def register_on(reg, name=None):
    def inner(obj):
        obj_name = name if name is not None else obj.__name__
        if hasattr(reg, obj_name):
            raise NameError(obj_name)
        setattr(reg, obj_name, obj)
        return obj
    return inner


def attr_repr(obj: ta.Any, *attrs: str) -> str:
    return '%s(%s)' % (
        type(obj).__name__,
        ', '.join('%s=%r' % (attr, getattr(obj, attr)) for attr in attrs))


def arg_repr(*args, **kwargs) -> str:
    return ', '.join(*(
        list(map(repr, args)) +
        [f'{k}={repr(v)}' for k, v in kwargs.items()]
    ))


def new_type(
        name: str,
        bases: ta.Sequence[ta.Any],
        namespace: ta.Mapping[str, ta.Any],
        **kwargs
) -> ta.Type:
    return types.new_class(
        name,
        tuple(bases),
        kwds=kwargs,
        exec_body=lambda ns: ns.update(namespace),
    )


def super_meta(
        super_meta: ta.Type,
        meta: ta.Type,
        name: str,
        bases: ta.Sequence[ta.Any],
        namespace: ta.Mapping[str, ta.Any],
        **kwargs
) -> ta.Type:
    resolved_bases = types.resolve_bases(bases)
    if resolved_bases is not bases:
        if '__orig_bases__' in namespace:
            raise TypeError((bases, resolved_bases))
        namespace['__orig_bases__'] = bases
    return super_meta.__new__(meta, name, resolved_bases, namespace, **kwargs)


def is_lambda(f: ta.Any) -> bool:
    l = lambda: 0
    return isinstance(f, type(l)) and f.__name__ == l.__name__


def is_descriptor(obj: ta.Any) -> bool:
    return (
        hasattr(obj, '__get__') or
        hasattr(obj, '__set__') or
        hasattr(obj, '__delete__')
    )


def unwrap_instance_weakproxy(proxy: weakref.ProxyType, cls: ta.Type[T]) -> T:
    if not isinstance(proxy, weakref.ProxyType):
        raise TypeError(proxy)
    inst = proxy.__repr__.__self__
    if not isinstance(inst, cls):
        raise TypeError(inst)
    return inst


def singleton(*args, **kwargs) -> ta.Callable[[ta.Type[T]], ta.Callable[..., T]]:
    def inner(cls):
        obj = cls(*args, **kwargs)
        obj.__name__ = cls.__name__
        return obj
    return inner


class AttrAccessor(ta.Generic[T]):

    def __init__(
            self,
            getter: ta.Callable[[str], T],
            translated_exceptions: ta.Iterable[ta.Type[Exception]] = [],
    ) -> None:
        super().__init__()

        self.__getter = getter
        self.__translated_exceptions = tuple(translated_exceptions)

    def __getattr__(self, name: str) -> T:
        try:
            return self.__getter(name)
        except self.__translated_exceptions:
            raise AttributeError(name)

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return AttrAccessor(
                self.__getter.__get__(instance, owner),
                self.__translated_exceptions
            )

    @classmethod
    def from_dict(cls, dct: ta.Dict[str, T]) -> 'AttrAccessor[T]':
        return cls(dct.__getitem__, (KeyError,))


def anon_object(name: str) -> ta.Any:
    return new_type(name, (object,), {})()


def dir_dict(
        obj: ta.Any,
        *,
        default=_NOT_SET,
        public: bool = False,
        filter: ta.Callable[[str], bool] = None,
) -> ta.Dict[str, ta.Any]:
    if filter is None:
        filter = lambda _: True  # noqa
    args = (default,) if default is not _NOT_SET else ()
    return {a: getattr(obj, a, *args) for a in dir(obj) if filter(a) and not (public and a.startswith('_'))}


def cached_nullary(fn: ta.Callable[[], T]) -> ta.Callable[[], T]:
    value = not_set = object()

    @functools.wraps(fn)
    def inner():
        nonlocal value
        if value is not_set:
            value = fn()
        return value

    return inner


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


class FinalException(Exception):

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


class SealedException(Exception):

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


class _Marker(Final):

    def __mro_entries__(self, bases, **kwargs):
        return (Final, NotInstantiable)


Marker = _Marker()


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


class staticfunction(staticmethod):
    """
    Allows calling @staticmethods within a classbody. Vanilla @staticmethods are not callable:

        TypeError: 'staticmethod' object is not callable
    """

    def __call__(self, *args, **kwargs):
        return self.__func__(*args, **kwargs)


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


class VoidException(Exception):
    pass


def void(*args, **kwargs) -> ta.NoReturn:
    raise VoidException


# region ContextManagers


class ContextManaged:

    def __enter__(self: Self) -> Self:
        return self

    def __exit__(
            self,
            exc_type: ta.Optional[ta.Type[Exception]],
            exc_val: ta.Optional[Exception],
            exc_tb: ta.Optional[types.TracebackType]
    ) -> ta.Optional[bool]:
        return


class ContextManageable(Protocol, ta.Generic[T]):

    def __enter__(self) -> T:
        raise NotImplementedError

    def __exit__(
            self,
            exc_type: ta.Optional[ta.Type[Exception]],
            exc_val: ta.Optional[Exception],
            exc_tb: ta.Optional[types.TracebackType]
    ) -> ta.Optional[bool]:
        raise NotImplementedError


class ExitStacked:

    @property
    def _exit_stack(self) -> contextlib.ExitStack:
        try:
            return self.__exit_stack
        except AttributeError:
            es = self.__exit_stack = contextlib.ExitStack()
            return es

    def _enter_context(self, context_manager: ContextManageable[T]) -> T:
        return self._exit_stack.enter_context(context_manager)

    def __enter__(self: Self) -> Self:
        super().__enter__()
        self._exit_stack.__enter__()
        return self

    def __exit__(
            self,
            exc_type: ta.Optional[ta.Type[Exception]],
            exc_val: ta.Optional[Exception],
            exc_tb: ta.Optional[types.TracebackType]
    ) -> ta.Optional[bool]:
        self._exit_stack().__exit__(exc_type, exc_val, exc_tb)
        return super().__exit__(exc_type, exc_val, exc_tb)


@contextlib.contextmanager
def maybe_managing(obj: T) -> T:
    if isinstance(obj, ContextManageable):
        with obj:
            yield obj
    else:
        yield obj


@contextlib.contextmanager
def disposing(obj: T, attr: str = 'dispose') -> T:
    try:
        yield obj
    finally:
        getattr(obj, attr)()


@contextlib.contextmanager
def defer(fn: ta.Callable):
    try:
        yield fn
    finally:
        fn()


def context_wrapped(cm: ta.Callable[[], ta.ContextManager]) -> ta.Callable:
    def outer(fn):
        @functools.wraps(fn)
        def inner(*args, **kwargs):
            with cm():
                return fn(*args, **kwargs)
        return inner
    return outer


@contextlib.contextmanager
def context_var_setting(var: contextvars.ContextVar[T], val: T) -> T:
    prev = var.set(val)
    try:
        yield val
    finally:
        var.reset(prev)


def manage_maybe_iterator(
        manager_factory: ta.Callable[[], ta.ContextManager[ta.Any]],
        maybe_iterator_factory: ta.Callable[[], IteratorTOrT]
) -> IteratorTOrT:
    with manager_factory():
        result = maybe_iterator_factory()
    if isinstance(result, collections.abc.Iterator):
        def inner():
            with manager_factory():
                yield from result
        return inner()
    else:
        return result


# endregion


# region Strings


def camelize(name: str) -> str:
    return ''.join(map(str.capitalize, name.split('_')))


def decamelize(name: str) -> str:
    uppers: ta.List[ta.Optional[int]] = [i for i, c in enumerate(name) if c.isupper()]
    return '_'.join([name[l:r].lower() for l, r in zip([None] + uppers, uppers + [None])]).strip('_')


def prefix_lines(s: str, p: str) -> str:
    return '\n'.join([p + l for l in s.split('\n')])


def indent_lines(s: str, num: int) -> str:
    return prefix_lines(s, ' ' * num)


def is_dunder(name: str) -> bool:
    return (
        name[:2] == name[-2:] == '__' and
        name[2:3] != '_' and
        name[-3:-2] != '_' and
        len(name) > 4
    )


def is_sunder(name: str) -> bool:
    return (
        name[0] == name[-1] == '_' and
        name[1:2] != '_' and
        name[-2:-1] != '_' and
        len(name) > 2
    )


# endregion


# region Enums


def parse_enum(obj: ta.Union[EnumT, str], cls: ta.Type[EnumT]) -> EnumT:
    if isinstance(obj, cls):
        return cls
    elif not isinstance(obj, str) or obj.startswith('__'):
        raise ValueError(f'Illegal {cls!r} name: {obj!r}')
    else:
        return getattr(cls, obj)


class SimpleDict(dict):

    def update(self, m: ta.Mapping[K, V], **kwargs: V) -> None:
        for k, v in m.items():
            self[k] = v
        for k, v in kwargs.items():
            self[k] = v


class _AutoEnumMeta(enum.EnumMeta):

    class Dict(SimpleDict, enum._EnumDict):

        def __init__(self, src: enum._EnumDict) -> None:
            super().__init__()
            self.update(src)
            if hasattr(src, '_generate_next_value'):
                self._generate_next_value = src._generate_next_value

        def __setitem__(self, key, value):
            if value is Ellipsis:
                value = enum.auto()
            return super().__setitem__(key, value)

    def __new__(mcls, name, bases, namespace):
        if 'AutoEnum' not in globals():
            return type.__new__(mcls, name, bases, namespace)
        bases = tuple(b if b is not AutoEnum else enum.Enum for b in bases)
        return super().__new__(mcls, name, bases, namespace)

    @classmethod
    def __prepare__(mcls, cls, bases):
        if 'AutoEnum' not in globals():
            return {}
        bases = tuple(b if b is not AutoEnum else enum.Enum for b in bases)
        return _AutoEnumMeta.Dict(super().__prepare__(cls, bases))


class AutoEnum(metaclass=_AutoEnumMeta):
    pass


class _ValueEnumMeta(type):

    IGNORED_BASES = {
        object,
    }

    IGNORED_ATTRS = {
        '_by_name',
    }

    def __new__(mcls, name, bases, namespace):
        cls = super().__new__(mcls, name, bases, namespace)
        by_name = {}
        for mrocls in cls.__mro__:
            if mrocls in mcls.IGNORED_BASES:
                continue
            for k, v in mrocls.__dict__.items():
                if k not in by_name and k not in mcls.IGNORED_ATTRS and not is_dunder(k):
                    by_name[k] = v
        cls._by_name = by_name
        return cls


class ValueEnum(metaclass=_ValueEnumMeta):

    def __new__(cls, *args, **kwargs):
        raise TypeError


# endregion


# region Arithmetic


def get_bit(bit: int, value: int) -> int:
    return (value >> bit) & 1


def get_bits(bits_from: int, num_bits: int, value: int) -> int:
    return (value & ((1 << (bits_from + num_bits)) - 1)) >> bits_from


def set_bit(bit: int, bit_value: ta.Union[bool, int], value: int) -> int:
    if bit_value:
        return value | (1 << bit)
    else:
        return value & ~(1 << bit)


def set_bits(bits_from: int, num_bits: int, bits_value: int, value: int) -> int:
    return value & ~(((1 << num_bits) - 1) << bits_from) | (bits_value << bits_from)


class Infinity(Final):

    def __repr__(self):
        return 'Infinity'

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, Infinity)

    def __ne__(self, other):
        return not isinstance(other, Infinity)

    def __lt__(self, other):
        return False

    def __le__(self, other):
        return False

    def __gt__(self, other):
        return True

    def __ge__(self, other):
        return True

    def __neg__(self):
        return NEGATIVE_INFINITY


class NegativeInfinity(Final):

    def __repr__(self):
        return '-Infinity'

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, NegativeInfinity)

    def __ne__(self, other):
        return not isinstance(other, NegativeInfinity)

    def __lt__(self, other):
        return True

    def __le__(self, other):
        return True

    def __gt__(self, other):
        return False

    def __ge__(self, other):
        return False

    def __neg__(self):
        return INFINITY


INFINITY = Infinity()

NEGATIVE_INFINITY = NegativeInfinity()


# endregion


# region DateTimes


def to_seconds(value: datetime.timedelta) -> float:
    return 86400 * value.days + value.seconds + 0.000001 * value.microseconds


def months_ago(date: datetime.date, num: int) -> datetime.date:
    ago_year = date.year
    ago_month = date.month - num
    while ago_month < 1:
        ago_year -= 1
        ago_month += 12
    while ago_month > 12:
        ago_year += 1
        ago_month -= 12
    return datetime.date(ago_year, ago_month, 1)


TIMEDELTA_STR_RE = re.compile(
    r'^\s*'
    r'((?P<days>-?\d+)\s*days?,\s*)?'
    r'(?P<hours>\d?\d):(?P<minutes>\d\d)'
    r':(?P<seconds>\d\d+(\.\d+)?)'
    r'\s*$')


def parse_date(s: str) -> datetime.date:
    if s.lower() in ['today', 'now']:
        return datetime.date.today()
    elif s.lower() == 'yesterday':
        return datetime.date.today() - datetime.timedelta(days=1)
    elif s.lower().endswith(' days ago'):
        num = int(s.split(' ', 1)[0])
        return datetime.date.today() - datetime.timedelta(days=num)
    elif s.lower().endswith(' months ago'):
        months = int(s.split(' ', 1)[0])
        return months_ago(datetime.date.today(), months)
    else:
        return datetime.date(*map(int, s.split('-', 3)))


TIMEDELTA_DHMS_RE = re.compile(
    r'^\s*'
    r'(?P<negative>-)?'
    r'((?P<days>\d+(\.\d+)?)\s*(d|days?))?'
    r',?\s*((?P<hours>\d+(\.\d+)?)\s*(h|hours?))?'
    r',?\s*((?P<minutes>\d+(\.\d+)?)\s*(m|minutes?))?'
    r',?\s*((?P<seconds>\d+(\.\d+)?)\s*(s|secs?|seconds?))?'
    r'\s*$')


def parse_timedelta(s: str) -> datetime.timedelta:
    match = TIMEDELTA_DHMS_RE.match(s)
    if not match:
        match = TIMEDELTA_STR_RE.match(s)
    if not match:
        raise ValueError
    timedelta_kwargs = {
        k: float(v)
        for k, v in match.groupdict().items()
        if k != 'negative' and v is not None}
    if not timedelta_kwargs:
        raise ValueError()
    sign = -1 if match.groupdict().get('negative') else 1
    return sign * datetime.timedelta(**timedelta_kwargs)


# endregion


# region Imports


def lazy_import(name: str, package: str = None) -> ta.Callable[[], ta.Any]:
    return cached_nullary(functools.partial(importlib.import_module, name, package=package))


def import_module(dotted_path: str) -> types.ModuleType:
    if not dotted_path:
        raise ImportError(dotted_path)
    mod = __import__(dotted_path, globals(), locals(), [])
    for name in dotted_path.split('.')[1:]:
        try:
            mod = getattr(mod, name)
        except AttributeError:
            raise AttributeError('Module %r has no attribute %r' % (mod, name))
    return mod


def import_module_attr(dotted_path: str) -> ta.Any:
    module_name, _, class_name = dotted_path.rpartition('.')
    mod = import_module(module_name)
    try:
        return getattr(mod, class_name)
    except AttributeError:
        raise AttributeError('Module %r has no attr %r' % (module_name, class_name))


def yield_importable(package_root: str, *, recursive: bool = False) -> ta.Iterator[str]:
    def rec(dir):
        if dir.split('.')[-1] == '__pycache__':
            return

        try:
            module = sys.modules[dir]
        except KeyError:
            try:
                __import__(dir)
            except ImportError:
                return
            module = sys.modules[dir]
        if module.__file__ is None:
            return

        for file in pkg_resources.resource_listdir(dir, '.'):
            if file.endswith('.py') and not file.startswith('_'):
                yield dir + '.' + file[:-3]
            elif recursive and '.' not in file:
                try:
                    yield from rec(dir + '.' + file)
                except (ImportError, NotImplementedError):
                    pass

    yield from rec(package_root)


def yield_import_all(
        package_root: str,
        *,
        globals: ta.Dict[str, ta.Any] = None,
        locals: ta.Dict[str, ta.Any] = None,
        recursive: bool = False,
) -> ta.Iterator[types.ModuleType]:
    for import_path in yield_importable(package_root, recursive=recursive):
        yield __import__(import_path, globals=globals, locals=locals)


def import_all(package_root: str, *, recursive: bool = False) -> None:
    for _ in yield_import_all(package_root, recursive=recursive):
        pass


# endregion


# region Async


def sync_await(fn: ta.Callable[..., T], *args, **kwargs) -> T:
    async def gate():
        nonlocal ret
        ret = await fn(*args, **kwargs)
    ret = not_set = object()
    cr = gate()
    with contextlib.closing(cr):
        try:
            cr.send(None)
        except StopIteration:
            pass
        if ret is not_set or cr.cr_await is not None or cr.cr_running:
            raise TypeError('Not terminated')
    return ret


def sync_list(fn: ta.Callable[..., ta.AsyncIterator[T]], *args, **kwargs) -> ta.List[T]:
    async def inner():
        nonlocal lst
        lst = [v async for v in fn(*args, **kwargs)]
    lst = None
    sync_await(inner)
    if not isinstance(lst, list):
        raise TypeError(lst)
    return lst


async def async_list(fn: ta.Callable[..., ta.AsyncIterator[T]], *args, **kwargs) -> ta.List[T]:
    return [v async for v in fn(*args, **kwargs)]


class SyncableIterable(ta.Generic[T]):

    def __init__(self, obj) -> None:
        super().__init__()
        self._obj = obj

    def __iter__(self) -> ta.Iterator[T]:
        async def inner():
            async for i in self._obj:
                yield i
        return iter(sync_list(inner))

    def __aiter__(self) -> ta.AsyncIterator[T]:
        return self._obj.__aiter__()


def syncable_iterable(fn: ta.Callable[..., ta.AsyncIterator[T]]) -> ta.Callable[..., SyncableIterable[T]]:
    @functools.wraps(fn)
    def inner(*args, **kwargs):
        return SyncableIterable(fn(*args, **kwargs))
    return inner


def await_futures(
        futures: ta.Sequence[concurrent.futures.Future],
        *,
        timeout_s: ta.Union[int, float] = 60,
        timeout_exception: Exception = RuntimeError('Future timeout'),
        tick_interval: ta.Union[int, float] = 0.1,
        tick_fn: ta.Callable[..., bool] = lambda: True,
) -> bool:
    start = time.time()
    pos = 0
    while tick_fn():
        for pos in range(pos, len(futures)):
            if not futures[pos].done():
                break
        else:
            return True
        if time.time() >= (start + timeout_s):
            raise timeout_exception
        time.sleep(tick_interval)
    return False


# endregion
