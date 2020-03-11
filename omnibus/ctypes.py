"""
TODO:
- lazy eval anns
- __repr__
- def type(...) for bitfield widths
"""
import ctypes as ct
import types
import typing as ta

from . import check
from . import code as bco
from . import lang


c_void_pp = ct.POINTER(ct.c_void_p)


_AUTO_IGNORED_KEYS = {
    '__init__',
    '__module__',
    '__qualname__',
    '_fields_',
    '_functions_',
}


def _extract_function_annotations(fn: types.FunctionType) -> ta.Union[ta.Any, ta.Iterable[ta.Any]]:
    code: types.CodeType = fn.__code__
    check.arg(code.co_argcount and code.co_varnames[0] == 'self')
    check.arg(not fn.__defaults__)
    check.arg(not code.co_kwonlyargcount)
    check.arg(not (code.co_flags & bco.CO_VARKEYWORDS))
    if code.co_flags & bco.CO_VARARGS:
        args = code.co_varnames[1:-1]
    else:
        args = code.co_varnames[1:]

    def fix(t):
        if t is ta.Any:
            return ct.c_void_p
        else:
            return t

    anns = fn.__annotations__ or {}
    return fix(anns.get('return', ct.c_void_p)), [fix(anns.get(a, ct.c_void_p)) for a in args]


def _build_meta(base: ta.Type) -> ta.Type:
    class _Meta(type(base)):

        class Dict(lang.SimpleMetaDict):

            def __setitem__(self, key, value):
                if key in _AUTO_IGNORED_KEYS:
                    super().__setitem__(key, value)
                else:
                    if isinstance(value, types.FunctionType):
                        ret, args = _extract_function_annotations(value)
                        value = ct.CFUNCTYPE(ret, *args)
                    self.setdefault('_fields_', []).append((key, value))

        @classmethod
        def __prepare__(mcls, cls, bases):
            return _Meta.Dict(super().__prepare__(cls, bases))

        def __new__(mcls, name, bases, namespace, **kwargs):
            if bases == (base,):
                return super().__new__(mcls, name, bases, namespace, **kwargs)
            else:
                return type(base).__new__(mcls, name, bases, namespace, **kwargs)

    return _Meta


class AutoStructure(ct.Structure, metaclass=_build_meta(ct.Structure)):
    pass


class AutoUnion(ct.Union, metaclass=_build_meta(ct.Union)):
    pass


class _AutoDLLMeta(type(ct.CDLL)):

    class Dict(lang.SimpleMetaDict):

        def __setitem__(self, key, value):
            if key in _AUTO_IGNORED_KEYS:
                super().__setitem__(key, value)
            else:
                if isinstance(value, types.FunctionType):
                    self.setdefault('_functions_', []).append((key, _extract_function_annotations(value)))
                else:
                    super().__setitem__(key, value)

    @classmethod
    def __prepare__(mcls, cls, bases):
        return _AutoDLLMeta.Dict(super().__prepare__(cls, bases))


class AutoDLL(ct.CDLL, metaclass=_AutoDLLMeta):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for k, [ret, args_] in getattr(type(self), '_functions_', []):
            fn = getattr(self, k)
            fn.restype = ret
            fn.argtypes = args_
