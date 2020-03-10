import functools
import typing as ta

from .. import callables
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

    def register(*clss, impl=None):
        if impl is None:
            return lambda _impl: register(*clss, impl=_impl)
        for cls in clss:
            dispatcher[cls] = impl
        return impl

    def wrapper(arg, *args, **kw):
        impl, manifest = dispatcher[dispatcher.key(arg)]
        impl = inject_manifest(impl, manifest)
        return impl(arg, *args, **kw)

    def inner(func):
        functools.update_wrapper(wrapper, func)
        argspec = callables.get_cached_full_arg_spec(func)
        try:
            wrapper.__annotations__ = {'return': argspec.annotations['return']}
        except KeyError:
            pass

        wrapper.Dispatcher = dispatcher
        wrapper.register = register
        wrapper.dispatcher = dispatcher
        wrapper.clear_cache = dispatcher.clear

        register(object, impl=func)
        return wrapper

    return inner
