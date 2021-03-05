import logging
import typing as ta

from .errors import Error
from .errors import Errors
from .logging import Logger
from .logging import StdlibLogger
from .metrics import Metric
from .metrics import Metrics
from .runtime import Runtime


_log = logging.getLogger(__name__)


class DefaultMetrics(Metrics):
    def send(self, metric: Metric) -> None:
        pass


class DefaultErrors(Errors):
    def report(self, error: Error) -> None:
        pass


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
