import contextlib
import threading
import typing as ta

from .default import _DEFAULT
from .errors import Errors
from .logging import Logger
from .metrics import Metrics
from .runtime import InvalidatableRuntime
from .runtime import Runtime


get: ta.Callable[..., Runtime]


def log() -> Logger:
    return get().log


def errors() -> Errors:
    return get().errors


def metrics() -> Metrics:
    return get().metrics


class CurrentRuntime(Runtime):

    def log(self) -> Logger:
        return log()

    def errors(self) -> Errors:
        return errors()

    def metrics(self) -> Metrics:
        return metrics()


_CURRENT = threading.local()


def get(default: ta.Optional[Runtime] = None) -> Runtime:
    try:
        rt = _CURRENT.runtime
    except AttributeError:
        if default is not None:
            rt = default
        else:
            rt = _DEFAULT
    if not isinstance(rt, Runtime):
        raise TypeError(rt)
    return rt


@contextlib.contextmanager
def setting_current(runtime: Runtime) -> Runtime:
    if not isinstance(runtime, Runtime):
        raise TypeError(runtime)
    ir = InvalidatableRuntime(runtime)
    try:
        prev = _CURRENT.runtime
    except AttributeError:
        prev = _DEFAULT
        reset = None
    else:
        reset = prev
    try:
        _CURRENT.runtime = ir
        yield prev
    finally:
        if reset is not None:
            _CURRENT.runtime = reset
        else:
            del _CURRENT.runtime
        ir.invalidate()
