import functools
import sys
import weakref

from . import lang


class NOT_SET(lang.Marker):
    pass


class UnboundVarError(ValueError):
    pass


class Var:

    def __init__(self, default=NOT_SET, *, new=NOT_SET, validate=None):
        super().__init__()

        if default is not NOT_SET and new is not NOT_SET:
            raise TypeError('Cannot set both default and new')
        elif default is not NOT_SET:
            self._new = lambda: default
        else:
            self._new = new
        self._validate = validate
        self._bindings_by_frame = weakref.WeakValueDictionary()

    def __call__(self, *args, **kwargs):
        if not args:
            if kwargs:
                raise TypeError(kwargs)
            return self.value
        elif len(args) == 1:
            return self.binding(*args, **kwargs)
        else:
            raise TypeError(args)

    def binding(self, value, *, offset=1):
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
    def values(self):
        frame = sys._getframe(1).f_back
        while frame:
            try:
                frame_bindings = self._bindings_by_frame[frame]
            except KeyError:
                pass
            else:
                for level, frame_binding in sorted(frame_bindings.items()):
                    yield frame_binding._value
            frame = frame.f_back
        if self._new is not NOT_SET:
            yield self._new()

    def __iter__(self):
        return self.values

    @property
    def value(self):
        try:
            return next(self.values)
        except StopIteration:
            raise UnboundVarError


class Binding:

    def __init__(self, var, value, offset=1):
        super().__init__()

        self._var = var
        self._value = value
        self._offset = offset

    def __enter__(self):
        self._frame = sys._getframe(self._offset).f_back
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
        assert self._frame_bindings[self._level] is self
        del self._frame_bindings[self._level]
        del self._frame_bindings
        del self._frame


class Dyn:

    def __init__(self):
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
