import dataclasses as dc
import datetime
import functools
import logging
import threading
import typing as ta


log = logging.getLogger(__name__)


NOISY_LOGGERS: ta.Set[str] = {
    'boto3.resources.action',
    'datadog.dogstatsd',
    'elasticsearch',
    'kazoo.client',
    'requests.packages.urllib3.connectionpool',
}


@dc.dataclass()
class DictConfig:
    version: int = 1
    incremental: bool = False
    disable_existing_loggers: bool = False
    filters: ta.Dict[str, 'FilterConfig'] = dc.field(default_factory=dict)
    formatters: ta.Dict[str, 'FormatterConfig'] = dc.field(default_factory=dict)
    handlers: ta.Dict[str, 'HandlerConfig'] = dc.field(default_factory=dict)
    loggers: ta.Dict[str, 'LoggerConfig'] = dc.field(default_factory=dict)
    root: 'LoggerConfig' = None


FilterConfig = ta.Dict[str, ta.Any]
FormatterConfig = ta.Dict[str, ta.Any]
HandlerConfig = ta.Dict[str, ta.Any]
LoggerConfig = ta.Dict[str, ta.Any]


class LogFormatter(logging.Formatter):

    converter = datetime.datetime.fromtimestamp

    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            return ct.strftime(datefmt)
        else:
            t = ct.strftime("%Y-%m-%d %H:%M:%S")
            return '%s.%03d' % (t, record.msecs)


try:
    # FIXME: threading.get_native_id() since 3.8
    from ._ext.cc.os import gettid as _gettid

except (ImportError, OSError):
    def _gettid() -> int:
        return threading.current_thread().ident


class TidFilter(logging.Filter):

    def filter(self, record):
        record.tid = _gettid()
        return True


STANDARD_LOG_FORMAT_PARTS = [
    ('asctime', '%(asctime)-15s'),
    ('process', 'pid=%(process)-6s'),
    ('thread', 'tid=%(thread)-16s'),
    ('levelname', '%(levelname)-8s'),
    ('name', '%(name)s'),
    ('separator', '::'),
    ('message', '%(message)s'),
]


def build_log_format(parts: ta.Iterable[ta.Tuple[str, str]]) -> str:
    return ' '.join(v for k, v in parts)


def configure_standard_logging(level: ta.Any = None) -> logging.Handler:
    handler = logging.StreamHandler()
    handler.setFormatter(LogFormatter(build_log_format(STANDARD_LOG_FORMAT_PARTS)))
    handler.addFilter(TidFilter())
    logging.root.addHandler(handler)
    if level is not None:
        logging.root.setLevel(level)
    for noisy_logger in NOISY_LOGGERS:
        logging.getLogger(noisy_logger).setLevel(logging.WARNING)
    return handler


def error_logging(log=log):
    def outer(fn):
        @functools.wraps(fn)
        def inner(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except Exception:
                log.exception(f'Error in {fn!r}')
                raise

        return inner
    return outer
