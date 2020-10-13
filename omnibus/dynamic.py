"""
Dynamically scoped variables (implemented by stackwalking). Unlike threadlocals these are generator-correct both in
binding and retrieval, and unlike ContextVars they require no manual context management. They are however *slow* and
should be used sparingly (once per sql statement executed not once per inner function call).

TODO:
 - clj-style binding conveyance
 - contextvar/async interop
 - 'partializer'
"""
import contextlib
import functools
import sys
import types
import typing as ta
import weakref

from . import lang


T = ta.TypeVar('T')


_HOISTED_CODE_DEPTH: ta.MutableMapping[types.CodeType, int] = weakref.WeakKeyDictionary()
_MAX_HOIST_DEPTH = 0


def hoist(depth=0):
    def inner(fn):
        _HOISTED_CODE_DEPTH[fn.__code__] = depth
        global _MAX_HOIST_DEPTH
        _MAX_HOIST_DEPTH = max(_MAX_HOIST_DEPTH, depth)
        return fn
    return inner


hoist()(contextlib.ExitStack.enter_context)


class MISSING(lang.Marker):
    pass


class UnboundVarError(ValueError):
    pass


class Var(ta.Generic[T]):

    def __init__(
            self,
            default: ta.Union[T, ta.Type[MISSING]] = MISSING,
            *,
            new: ta.Union[ta.Callable[[], T], ta.Type[MISSING]] = MISSING,
            validate: ta.Callable[[T], None] = None,
    ) -> None:
        super().__init__()

        new: ta.Any
        if default is not MISSING and new is not MISSING:
            raise TypeError('Cannot set both default and new')
        elif default is not MISSING:
            new = lambda: default
        self._new = ta.cast(ta.Union[ta.Type[MISSING], ta.Callable[[], T]], new)
        self._validate = validate
        self._bindings_by_frame: ta.MutableMapping[types.FrameType, ta.MutableMapping[int, Binding]] = weakref.WeakValueDictionary()  # noqa

    def __call__(self, *args, **kwargs) -> ta.Union[T, ta.ContextManager[T]]:
        if not args:
            if kwargs:
                raise TypeError(kwargs)
            return self.value
        elif len(args) == 1:
            return self.binding(*args, **kwargs)
        else:
            raise TypeError(args)

    def binding(self, value: T, *, offset: int = 0) -> ta.ContextManager[T]:
        if self._validate is not None:
            self._validate(self.value)
        return Binding(self, value, offset=offset)

    def with_binding(self, value):
        def outer(fn):
            @functools.wraps(fn)
            def inner(*args, **kwargs):
                with self.binding(value):
                    return fn(*args, **kwargs)
            return inner
        return outer

    def with_binding_fn(self, binding_fn):
        this = self

        def outer(fn):
            class Descriptor:
                func_name = fn.__name__

                @staticmethod
                @functools.wraps(fn)
                def __call__(*args, **kwargs):
                    with this.binding(binding_fn(*args, **kwargs)):
                        return fn(*args, **kwargs)

                def __get__(self, obj, cls=None):
                    bound_binding_fn = binding_fn.__get__(obj, cls)
                    bound_fn = fn.__get__(obj, cls)

                    @functools.wraps(fn)
                    def inner(*args, **kwargs):
                        with this.binding(bound_binding_fn(*args, **kwargs)):
                            return bound_fn(*args, **kwargs)

                    inner.func_name = fn.__name__
                    return inner

            dct = dict((k, getattr(fn, k)) for k in functools.WRAPPER_ASSIGNMENTS)
            return lang.new_type(fn.__name__, (Descriptor,), dct)()

        return outer

    @property
    def values(self) -> ta.Iterator[T]:
        frame = sys._getframe().f_back
        while frame:
            try:
                frame_bindings = self._bindings_by_frame[frame]
            except KeyError:
                pass
            else:
                for level, frame_binding in sorted(frame_bindings.items()):
                    yield frame_binding._value
            frame = frame.f_back

        if self._new is not MISSING:
            yield self._new()

    def __iter__(self) -> ta.Iterator[T]:
        return self.values

    @property
    def value(self) -> T:
        try:
            return next(self.values)
        except StopIteration:
            raise UnboundVarError


class Binding(ta.Generic[T]):

    _frame = None
    _frame_bindings = None
    _level = None

    def __init__(self, var: Var[T], value: T, *, offset: int = 0) -> None:
        super().__init__()

        self._var = var
        self._value = value
        self._offset = offset

    def __enter__(self) -> T:
        frame = sys._getframe(self._offset).f_back
        lag_frame = frame
        while lag_frame is not None:
            for cur_depth in range(_MAX_HOIST_DEPTH + 1):
                if lag_frame is None:
                    break
                try:
                    lag_hoist = _HOISTED_CODE_DEPTH[lag_frame.f_code]
                except KeyError:
                    pass
                else:
                    if lag_hoist >= cur_depth:
                        frame = lag_frame = lag_frame.f_back
                        break
                lag_frame = lag_frame.f_back
            else:
                break

        self._frame = frame
        try:
            self._frame_bindings = self._var._bindings_by_frame[self._frame]
        except KeyError:
            self._frame_bindings = self._var._bindings_by_frame[self._frame] = weakref.WeakValueDictionary()
            self._level = 0
        else:
            self._level = min(self._frame_bindings.keys() or [1]) - 1

        self._frame_bindings[self._level] = self
        return self._value

    def __exit__(self, et, e, tb):
        if self._frame_bindings[self._level] is not self:
            raise TypeError

        del self._frame_bindings[self._level]
        del self._frame_bindings
        del self._frame


class Dyn:

    def __init__(self) -> None:
        super().__init__()

        self.__var = Var()

    def __call__(self, **kwargs):
        return self.__var.binding(kwargs)

    def __getattr__(self, key):
        for dct in self.__var.values:
            try:
                return dct[key]
            except KeyError:
                pass
        raise AttributeError(key)


dyn = Dyn()


class _GeneratorContextManager(contextlib._GeneratorContextManager):

    @hoist(2)
    def __enter__(self):
        return super().__enter__()


def contextmanager(fn: ta.Callable[..., ta.Iterator[T]]) -> ta.ContextManager[T]:
    @functools.wraps(fn)
    def helper(*args, **kwds):
        return _GeneratorContextManager(fn, args, kwds)
    return helper  # noqa
