"""
Given their special status, these are more formal than other interfaces (which increasingly tend to just be callables
taking a dataclass, in which Nop* is just void).

We want to support and balance the following:
 - contextual (threadlocal and.. 'otherwise') overriding
 - not needing to propagate kwargs
 - injection friendliness, yet with sane injectorless defaults
 - honoring the 'log' module-global idiom, largely for interop with embedding

TODO:
 - def runtime.log -> caller lookup :/ like stdlib does lols
 - inheritable thread local
"""
import abc
import contextlib
import dataclasses as dc
import io
import logging
import sys
import threading
import traceback
import types
import typing as ta


def _find_caller(ofs: int = 0) -> types.FrameType:
    f = sys._getframe(2 + ofs)  # noqa
    while hasattr(f, 'f_code'):
        if f.f_code.co_filename != __file__:
            return f
        f = f.f_back
    raise RuntimeError


_log = logging.getLogger(__name__)


class Logger(abc.ABC):

    def __init__(self):
        super().__init__()
        self._wrapped: ta.Optional[logging.Logger] = None

    @property
    def wrapped(self) -> logging.Logger:
        if self._wrapped is None:
            self._wrapped = LoggerAdapter(self)
        return self._wrapped

    def debug(self, msg: str, *args, **kwargs) -> None:
        if self.is_enabled_for(logging.DEBUG):
            self._log(logging.DEBUG, msg, args, **kwargs)

    def info(self, msg: str, *args, **kwargs) -> None:
        if self.is_enabled_for(logging.INFO):
            self._log(logging.INFO, msg, args, **kwargs)

    def warning(self, msg: str, *args, **kwargs) -> None:
        if self.is_enabled_for(logging.WARNING):
            self._log(logging.WARNING, msg, args, **kwargs)

    def error(self, msg: str, *args, **kwargs) -> None:
        if self.is_enabled_for(logging.ERROR):
            self._log(logging.ERROR, msg, args, **kwargs)

    def exception(self, msg: str, *args, exc_info=True, **kwargs) -> None:
        self.error(msg, *args, exc_info=exc_info, **kwargs)

    def critical(self, msg: str, *args, **kwargs) -> None:
        if self.is_enabled_for(logging.CRITICAL):
            self._log(logging.CRITICAL, msg, args, **kwargs)

    def log(self, level: int, msg: str, *args, **kwargs) -> None:
        if not isinstance(level, int):
            raise TypeError('Level must be an integer.')
        if self.is_enabled_for(level):
            self._log(level, msg, args, **kwargs)

    def is_enabled_for(self, level: int) -> bool:
        return level >= self.get_effective_level()

    @abc.abstractmethod
    def get_effective_level(self) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def _log(
            self,
            level: int,
            msg: str,
            args: ta.Any,
            *,
            exc_info: ta.Any = None,
            extra: ta.Any = None,
            stack_info: bool = False,
    ) -> None:
        raise NotImplementedError


class StdlibLogger(Logger):
    def __init__(self, underlying: logging.Logger) -> None:
        super().__init__()
        if not isinstance(underlying, logging.Logger):
            raise TypeError(underlying)
        self._underlying = underlying

    def is_enabled_for(self, level: int) -> bool:
        return self._underlying.isEnabledFor(level)

    def get_effective_level(self) -> int:
        return self._underlying.getEffectiveLevel()

    def _find_caller(self, stack_info: bool = False) -> ta.Tuple[str, int, str, ta.Optional[str]]:
        f = _find_caller(1)
        # TODO: ('(unknown file)', 0, '(unknown function)', None) ?

        sinfo = None
        if stack_info:
            sio = io.StringIO()
            sio.write('Stack (most recent call last):\n')
            traceback.print_stack(f, file=sio)
            sinfo = sio.getvalue()
            sio.close()
            if sinfo[-1] == '\n':
                sinfo = sinfo[:-1]

        return (f.f_code.co_filename, f.f_lineno, f.f_code.co_name, sinfo)

    def _log(
            self,
            level: int,
            msg: str,
            args: ta.Any,
            *,
            exc_info: ta.Any = None,
            extra: ta.Any = None,
            stack_info: bool = False,
    ) -> None:
        fn, lno, func, sinfo = self._find_caller(stack_info)

        if exc_info:
            if isinstance(exc_info, BaseException):
                exc_info = (type(exc_info), exc_info, exc_info.__traceback__)
            elif not isinstance(exc_info, tuple):
                exc_info = sys.exc_info()

        record = self._underlying.makeRecord(
            name=self._underlying.name,
            level=level,
            fn=fn,
            lno=lno,
            msg=msg,
            args=args,
            exc_info=exc_info,
            func=func,
            extra=extra,
            sinfo=sinfo,
        )

        self._underlying.handle(record)


def _raise_obj_type_error(obj, *args, **kwargs):
    raise TypeError(obj)


class _RaiseTypeErrorDescriptor:
    def __init__(self):
        super().__init__()
        self._name = None

    def __set_name__(self, owner, name):
        if name and self._name is None:
            self._name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        raise TypeError(instance, *([self._name] if self._name else []))


class LoggerAdapter(logging.Logger):

    def __init__(self, underlying: Logger) -> None:  # noqa
        # Explicitly no call to super
        if not isinstance(underlying, Logger):
            raise TypeError(underlying)
        self._underlying = underlying

    name = _RaiseTypeErrorDescriptor()
    level = _RaiseTypeErrorDescriptor()
    parent = _RaiseTypeErrorDescriptor()
    propagate = _RaiseTypeErrorDescriptor()
    handlers = _RaiseTypeErrorDescriptor()
    disabled = _RaiseTypeErrorDescriptor()

    setLevel = _raise_obj_type_error

    def isEnabledFor(self, level: int) -> bool:
        return self._underlying.is_enabled_for(level)

    def getEffectiveLevel(self) -> int:
        return self._underlying.get_effective_level()

    getChild = _raise_obj_type_error

    def debug(self, msg: ta.Any, *args, **kwargs) -> None:
        self._underlying.debug(msg, *args, **kwargs)

    def info(self, msg: ta.Any, *args, **kwargs) -> None:
        self._underlying.info(msg, *args, **kwargs)

    def warning(self, msg: ta.Any, *args, **kwargs) -> None:
        self._underlying.warning(msg, *args, **kwargs)

    def warn(self, msg: ta.Any, *args, **kwargs) -> None:
        self._underlying.warning(msg, *args, **kwargs)

    def error(self, msg: ta.Any, *args, **kwargs) -> None:
        self._underlying.error(msg, *args, **kwargs)

    def exception(self, msg: ta.Any, *args, **kwargs) -> None:
        self._underlying.exception(msg, *args, **kwargs)

    def critical(self, msg: ta.Any, *args, **kwargs) -> None:
        self._underlying.critical(msg, *args, **kwargs)

    def log(self, level: int, msg: ta.Any, *args, **kwargs) -> None:
        self._underlying.log(level, msg, *args, **kwargs)

    def _log(  # noqa
            self,
            level: int,
            msg: str,
            args: ta.Any,
            exc_info: ta.Any = None,
            extra: ta.Any = None,
            stack_info: bool = False,
    ) -> None:
        self._underlying._log(  # noqa
            level,
            msg,
            args,
            exc_info=exc_info,
            extra=extra,
            stack_info=stack_info,
        )

    filter = _raise_obj_type_error
    addHandler = _raise_obj_type_error
    removeHandler = _raise_obj_type_error
    findCaller = _raise_obj_type_error
    handle = _raise_obj_type_error
    makeRecord = _raise_obj_type_error
    hasHandlers = _raise_obj_type_error


@dc.dataclass(frozen=True)
class Error:
    exc: ta.Optional[BaseException] = None


class Errors(abc.ABC):
    @abc.abstractmethod
    def report(self, error: Error) -> None:
        raise NotImplementedError


class DefaultErrors(Errors):
    def report(self, error: Error) -> None:
        pass


@dc.dataclass(frozen=True)
class Metric:
    name: str
    value: ta.Optional[float] = None


class Metrics(abc.ABC):
    @abc.abstractmethod
    def send(self, metric: Metric) -> None:
        raise NotImplementedError


class DefaultMetrics(Metrics):
    def send(self, metric: Metric) -> None:
        pass


class Runtime(abc.ABC):

    @abc.abstractproperty
    def log(self) -> Logger:
        raise NotImplementedError

    @abc.abstractproperty
    def errors(self) -> Errors:
        raise NotImplementedError

    @abc.abstractproperty
    def metrics(self) -> Metrics:
        raise NotImplementedError

    def __getstate__(self):
        raise TypeError(self)


class SimpleRuntime(Runtime):
    def __init__(
            self,
            proto: ta.Optional[Runtime] = None,
            *,
            log: ta.Optional[Logger] = None,
            errors: ta.Optional[Errors] = None,
            metrics: ta.Optional[Metrics] = None,
    ) -> None:
        super().__init__()
        if proto is not None and not isinstance(proto, Runtime):
            raise TypeError(proto)
        if log is not None and not isinstance(log, Logger):
            raise TypeError(log)
        if errors is not None and not isinstance(errors, Errors):
            raise TypeError(errors)
        if metrics is not None and not isinstance(metrics, Metrics):
            raise TypeError(metrics)
        self._log = log if log is not None else proto.log if proto is not None else None
        self._errors = errors if errors is not None else proto.errors if proto is not None else self._default_errors
        self._metrics = metrics if metrics is not None else proto.metrics if proto is not None else self._default_metrics  # noqa

    @property
    def log(self) -> Logger:
        if self._log is not None:
            return self._log

        # FIXME: use _find_caller() lol
        return StdlibLogger(_log)

    _default_errors: ta.ClassVar[Errors] = DefaultErrors()

    @property
    def errors(self) -> Errors:
        return self._errors

    _default_metrics: ta.ClassVar[Metrics] = DefaultMetrics()

    @property
    def metrics(self) -> Metrics:
        return self._metrics


_DEFAULT = SimpleRuntime()


class ProxyRuntime(Runtime):
    def __init__(self, underlying: Runtime) -> None:
        super().__init__()
        if not isinstance(underlying, Runtime):
            raise TypeError(underlying)
        self._underlying = underlying

    @property
    def underlying(self) -> Runtime:
        return self._underlying

    @underlying.setter
    def underlying(self, underlying: Runtime) -> None:
        if not isinstance(underlying, Runtime):
            raise TypeError(underlying)
        self._underlying = underlying

    def log(self) -> Logger:
        return self._underlying.log

    def errors(self) -> Errors:
        return self._underlying.errors

    def metrics(self) -> Metrics:
        return self._underlying.metrics


class InvalidRuntime(Runtime):

    def log(self) -> Logger:
        raise RuntimeError(self)

    def errors(self) -> Errors:
        raise RuntimeError(self)

    def metrics(self) -> Metrics:
        raise RuntimeError(self)


class InvalidatableRuntime(ProxyRuntime):

    def __init__(self, underlying: Runtime) -> None:
        super().__init__(underlying)
        self._is_invalidated = False

    @property
    def is_invalidated(self) -> bool:
        return self._is_invalidated

    def invalidate(self) -> None:
        if not self._is_invalidated:
            self._is_invalidated = True
            self._underlying = InvalidRuntime()

    @property
    def underlying(self) -> Runtime:
        if self._is_invalidated:
            raise RuntimeError(self)
        return self._underlying

    @underlying.setter
    def underlying(self, underlying: Runtime) -> None:
        if self._is_invalidated:
            raise RuntimeError(self)
        if not isinstance(underlying, Runtime):
            raise TypeError(underlying)
        self._underlying = underlying


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


def configure_standard_logging(level: ta.Any = None) -> logging.Handler:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(name)s %(levelname)s %(module)s %(message)s'))
    logging.root.addHandler(handler)
    if level is not None:
        logging.root.setLevel(level)
    return handler


def test_runtime():
    log().info('hi')
    log().wrapped.info('hi2')


def _main():
    configure_standard_logging('INFO')
    test_runtime()


if __name__ == '__main__':
    _main()
