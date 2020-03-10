import collections.abc
import contextlib
import contextvars
import functools
import threading
import types
import typing as ta


T = ta.TypeVar('T')
Self = ta.TypeVar('Self')
IteratorTOrT = ta.Union[ta.Iterator[T], T]
CallableT = ta.TypeVar('CallableT', bound=ta.Callable)


_NOT_SET = object()


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
        try:
            superfn = super().__enter__
        except AttributeError:
            ret = self
        else:
            ret = superfn()
        self._exit_stack.__enter__()
        return ret

    def __exit__(
            self,
            exc_type: ta.Optional[ta.Type[Exception]],
            exc_val: ta.Optional[Exception],
            exc_tb: ta.Optional[types.TracebackType]
    ) -> ta.Optional[bool]:
        self._exit_stack.__exit__(exc_type, exc_val, exc_tb)
        try:
            superfn = super().__exit__
        except AttributeError:
            return None
        else:
            return superfn(exc_type, exc_val, exc_tb)


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


ContextWrappable = ta.Union[ta.ContextManager, str, ta.Callable[..., ta.ContextManager]]


class ContextWrapped:

    def __init__(self, fn: ta.Callable, cm: ContextWrappable) -> None:
        super().__init__()

        self._fn = fn
        self._cm = cm

        functools.update_wrapper(self, fn)

    def __get__(self, instance, owner):
        if instance is None and owner is None:
            return self
        fn = self._fn.__get__(instance, owner)
        cm = self._cm
        if isinstance(self._cm, str):
            if instance is not None:
                cm = getattr(instance, cm)
            elif owner is not None:
                cm = getattr(owner, cm)
            else:
                raise TypeError(cm)
        elif hasattr(cm, '__enter__'):
            pass
        elif callable(cm):
            cm = cm.__get__(instance, owner)
        else:
            raise TypeError(cm)
        return type(self)(fn, cm)

    def __call__(self, *args, **kwargs):
        if isinstance(self._cm, str):
            raise TypeError(self._cm)
        cm = self._cm
        if not hasattr(cm, '__enter__') and callable(cm):
            cm = cm(*args, **kwargs)
        with cm:
            return self._fn(*args, **kwargs)


def context_wrapped(cm: ContextWrappable) -> ta.Callable[[CallableT], CallableT]:
    def inner(fn):
        return ContextWrapped(fn, cm)
    return inner


@contextlib.contextmanager
def context_var_setting(var: contextvars.ContextVar[T], val: T) -> T:
    token = var.set(val)
    try:
        yield val
    finally:
        var.reset(token)


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


def default_lock(value: ta.Any, default: ta.Any) -> ContextManageable:
    if value is None:
        value = default
    if value is True:
        return threading.RLock()
    elif value is False or value is None:
        return ContextManaged()
    elif isinstance(value, ContextManageable):
        return value
    elif callable(value):
        value = value()
        if not isinstance(value, ContextManageable):
            raise TypeError(value)
        return value
    else:
        raise TypeError(value)