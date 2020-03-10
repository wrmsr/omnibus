import functools
import typing as ta

from .. import callables
from .types import Manifest


def get_manifest_injection_kwargs(impl: ta.Optional[ta.Callable]) -> ta.Optional[ta.Set[str]]:
    if impl is None:
        return None
    try:
        implargspec = callables.get_cached_full_arg_spec(impl)
    except TypeError:
        return None
    else:
        return {a for a in implargspec.kwonlyargs if implargspec.annotations.get(a) is Manifest}


def inject_manifest(impl: ta.Optional[ta.Callable], manifest: Manifest) -> ta.Callable:
    manifestkw = get_manifest_injection_kwargs(impl)
    if manifestkw:
        impl = functools.partial(impl, **{k: manifest for k in manifestkw})
    return impl
