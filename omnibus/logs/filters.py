import logging
import threading
import typing as ta


try:
    # FIXME: threading.get_native_id() since 3.8
    from ._ext.cc.os import gettid as _gettid  # noqa

except (ImportError, OSError):
    def _gettid() -> ta.Optional[int]:
        return threading.current_thread().ident


class TidFilter(logging.Filter):

    def filter(self, record):
        record.tid = _gettid()
        return True
