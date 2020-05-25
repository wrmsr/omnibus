import functools
import typing as ta

from .. import code
from .. import lang
from .. import reflect as rfl
from .caching import CachingDispatcher
from .erasing import ErasingDispatcher
from .manifests import inject_manifest
from .types import CacheGuard


T = ta.TypeVar('T')
R = ta.TypeVar('R')
Impl = ta.TypeVar('Impl')
TypeOrSpec = ta.Union[ta.Type, rfl.Spec]


def function(
        *,
        guard: CacheGuard = None,
        lock: lang.ContextManageable = None,
        **kwargs
) -> ta.Callable[[ta.Callable[..., R]], ta.Callable[..., R]]:
    dispatcher = CachingDispatcher(
        ErasingDispatcher(**kwargs),
        guard,
        lock=lock,
    )

    def register(fn):
        ann = getattr(fn, '__annotations__', {})
        if not ann:
            raise TypeError

        _, key = next(iter(ta.get_type_hints(fn).items()))
        if not isinstance(key, type):
            raise TypeError(key)

        dispatcher.register(key, fn)
        return fn

    def registering(*clss):
        def inner(impl):
            dispatcher.register_many(clss, impl)
            return impl
        return inner

    def wrapper(arg, *args, **kw):
        impl, manifest = dispatcher.dispatch(dispatcher.key(arg))
        impl = inject_manifest(impl, manifest)
        return impl(arg, *args, **kw)

    def inner(func):
        functools.update_wrapper(wrapper, func)
        argspec = code.get_full_arg_spec(func)
        try:
            wrapper.__annotations__ = {'return': argspec.annotations['return']}
        except KeyError:
            pass

        wrapper.register = register
        wrapper.registering = registering
        wrapper.dispatcher = dispatcher
        wrapper.clear_cache = dispatcher.clear

        registering(object)(func)
        return wrapper

    return inner
