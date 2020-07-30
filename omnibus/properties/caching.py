"""
TODO:
 - properties.init? eager cached, ~ideally~ automatically on __init__
  - not really possible without explicit help/call or baseclass
"""
import abc
import functools
import textwrap
import typing as ta

from .. import lang
from .. import pydevd
from .base import Property


T = ta.TypeVar('T')


def _mangle(s: str) -> str:
    for r in '.<>$':
        s = s.replace(r, '__')
    return s


class _GetterProperty(Property[T], lang.Abstract):

    def __new__(
            cls,
            func: ta.Callable[[ta.Any], T],
            *args,
            lock: lang.DefaultLockable = None,
            stateful: bool = False,
            **kwargs
    ):
        func = cls._unwrap(func)
        lock = lang.default_lock(lock, False)
        stateful = bool(stateful)

        __get__ = cls._build_getter(
            func,
            *args,
            lock=lock,
            stateful=stateful,
            **kwargs
        )

        bcls = type(
            cls.__name__,
            (cls,),
            {
                '__get__': __get__,
                '__new__': super().__new__,
            },
        )

        return bcls(
            func,
            *args,
            lock=lock,
            stateful=stateful,
            **kwargs
        )

    def __init__(
            self,
            func: ta.Callable[[ta.Any], T],
            *,
            lock: lang.DefaultLockable = None,
            stateful: bool = False,
    ) -> None:
        super().__init__()

        functools.update_wrapper(self, func)
        self._func = func
        self._lock = lock
        self._stateful = stateful

        self._name: ta.Optional[str] = None

    def __set_name__(self, owner, name):
        if self._name is None:
            self._name = name
        elif name != self._name:
            raise TypeError(f'Cannot assign the two different names ({self._name!r} and {name!r}).')

    @classmethod
    def _name_getter(cls, func: ta.Callable) -> str:
        try:
            co = func.__code__
            glo = func.__globals__
            suffix = f'{glo["__name__"]}__{co.co_firstlineno}'
        except Exception:  # noqa
            suffix = hex(id(func))[2:]
        return _mangle(f'_{cls.__name__}__get__{func.__name__}__{suffix}')

    @abc.abstractclassmethod
    def _build_getter(
            cls,
            func: ta.Callable[[ta.Any], T],
            *args,
            lock: lang.DefaultLockable = None,
            stateful: bool = False,
            **kwargs
    ) -> ta.Callable[[object, object], T]:
        raise NotImplementedError


class CachedProperty(_GetterProperty[T]):

    @classmethod
    def _build_getter(
            cls,
            func: ta.Callable[[ta.Any], T],
            *,
            lock: lang.DefaultLockable = None,
            stateful: bool = False,
    ) -> ta.Callable[[object, object], T]:
        fn_name = cls._name_getter(func)
        ns = {
            'fn_name': fn_name,
            'T': T,
            'forbid_debugger_call': pydevd.forbid_debugger_call,
            'lock': lock,
            'func': func,
        }

        exec(
            textwrap.dedent(f"""
            def {fn_name}(self, instance, owner=None) -> T:
                if instance is None:
                    return self

                {"forbid_debugger_call()" if stateful else ""}

                if self._name is None:
                    raise TypeError('Need name assigned')

                with lock():
                    try:
                        value = instance.__dict__[self._name]
                    except KeyError:
                        value = instance.__dict__[self._name] = func(instance)

                return value
            """),
            ns,
        )

        return ns[fn_name]


def cached(fn: ta.Callable[..., T]) -> T:
    return CachedProperty(fn)


def locked_cached(fn: ta.Callable[..., T]) -> T:
    return CachedProperty(fn, lock=True)


def stateful_cached(fn: ta.Callable[..., T]) -> T:
    return CachedProperty(fn, stateful=True)


class CachedClassProperty(_GetterProperty[T]):

    @classmethod
    def _unwrap(cls, fn):
        if isinstance(fn, classmethod):
            return fn.__func__
        return super()._unwrap(fn)

    @classmethod
    def _build_bound(
            cls,
            func: ta.Callable[[ta.Any], T],
            get: ta.Callable,
            owner: type,
            value: T,
    ) -> type:
        fn_name = cls._name_getter(func) + '__bound__' + _mangle(owner.__qualname__)
        ns = {
            'T': T,
            'owner': owner,
            'value': value,
            'get': get,
        }

        exec(
            textwrap.dedent(f"""
            def {fn_name}(self, binstance, bowner=None) -> T:
                if bowner is owner:
                    return value
                else:
                    return get(binstance, bowner)
            """),
            ns,
        )

        return type(
            fn_name,
            (object,),
            {
                '__get__': ns[fn_name],
                '_value': value,
            }
        )()

    @classmethod
    def _build_getter(
            cls,
            func: ta.Callable[[ta.Any], T],
            *,
            lock: lang.DefaultLockable = None,
            stateful: bool = False,
    ) -> ta.Callable[[object, object], T]:
        fn_name = cls._name_getter(func)
        ns = {
            'T': T,
            'forbid_debugger_call': pydevd.forbid_debugger_call,
            'lock': lock,
            'func': func,
            '_build_bound': cls._build_bound,
            'cls': cls,
        }

        exec(
            textwrap.dedent(f"""
            def {fn_name}(self, instance, owner=None) -> T:
                if owner is None:
                    return func(owner)

                {"forbid_debugger_call()" if stateful else ""}

                with lock():
                    try:
                        bound = owner.__dict__[self._name]
                    except KeyError:
                        bound = None
                    if bound is None or bound is self:
                        bound = _build_bound(func, {fn_name}.__get__(self, cls), owner, func(owner))
                        setattr(owner, self._name, bound)

                return bound._value
            """),
            ns,
        )

        return ns[fn_name]


def cached_class(fn: ta.Callable[..., T]) -> T:
    return CachedClassProperty(fn)


def locked_cached_class(fn: ta.Callable[..., T]) -> T:
    return CachedClassProperty(fn, lock=True)


def stateful_cached_class(fn: ta.Callable[..., T]) -> T:
    return CachedClassProperty(fn, stateful=True)
