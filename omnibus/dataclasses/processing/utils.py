import inspect
import typing as ta


def get_flat_fn_args(fn: ta.Callable) -> ta.List[str]:
    argspec = inspect.getfullargspec(fn)
    if (
            argspec.varargs or
            argspec.varkw or
            argspec.defaults or
            argspec.kwonlyargs or
            argspec.kwonlydefaults
    ):
        raise TypeError(fn)
    return list(argspec.args)
