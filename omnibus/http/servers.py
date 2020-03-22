"""
TODO:
 - threadpool
 - greenlet?
 - eventfd
 - https://github.com/MagicStack/httptools
 - https://gist.github.com/mitsuhiko/5721547
 - asyncio
 - firehose
 - netty-style protocol negotiation override
 - app composition (jersey style? inject integrated?)
  - debug app
"""
import abc
import contextlib
import logging
import selectors
import socket as sock
import threading
import typing as ta

from .. import lifecycles
from .. import properties
from .bind import Binder
from .types import App


log = logging.getLogger(__name__)


Self = ta.TypeVar('Self')
ClientAddress = ta.Tuple[str, int]


class WsgiServer(lifecycles.AbstractLifecycle, abc.ABC):

    if hasattr(selectors, 'PollSelector'):
        ServerSelector = selectors.PollSelector
    else:
        ServerSelector = selectors.SelectSelector

    def __init__(
            self,
            binder: Binder,
            app: App,
            *,
            poll_interval: float = 0.5,
            exit_timeout: float = 10.0,
            **kwargs
    ) -> None:
        super().__init__(**kwargs)

        self._binder = binder
        self._app = app
        self._poll_interval = poll_interval
        self._exit_timeout = exit_timeout

        self._lock = threading.RLock()
        self._is_shutdown = threading.Event()
        self._should_shutdown = False

    def _stop(self) -> None:
        acquired = self._lock.acquire(False)
        if not acquired:
            try:
                if not self._is_shutdown.is_set():
                    self.shutdown(True, self._exit_timeout)
            finally:
                self._lock.release()

    @property
    def binder(self) -> Binder:
        return self._binder

    @property
    def app(self) -> App:
        return self._app

    @properties.cached
    def base_environ(self) -> ta.Mapping[str, ta.Any]:
        return {
            'SERVER_NAME': self.binder.name,
            'GATEWAY_INTERFACE': 'CGI/1.1',
            'SERVER_PORT': str(self.binder.port),
            'REMOTE_HOST': '',
            'CONTENT_LENGTH': '',
            'SCRIPT_NAME': '',
        }

    def run(self, poll_interval=None) -> None:
        if poll_interval is None:
            poll_interval = self._poll_interval

        with contextlib.ExitStack() as exit_stack:
            exit_stack.enter_context(self._lock)
            exit_stack.enter_context(self._binder)

            self._binder.listen()

            self._is_shutdown.clear()
            try:
                # XXX: Consider using another file descriptor or connecting to the
                # socket to wake this up instead of polling. Polling reduces our
                # responsiveness to a shutdown request and wastes cpu at all other
                # times.
                with self.ServerSelector() as selector:
                    selector.register(self._binder.fileno(), selectors.EVENT_READ)

                    while not self._should_shutdown:
                        ready = selector.select(poll_interval)
                        if ready:
                            try:
                                request, client_address = self._binder.accept()

                            except OSError:
                                self.handle_error(None, None)
                                return

                            try:
                                self.process_request(request, client_address)

                            except Exception:
                                self.handle_error(request, client_address)
                                self.shutdown_request(request)

            finally:
                self._is_shutdown.set()

    def handle_error(
            self,
            request: ta.Optional[sock.socket],
            client_address: ta.Optional[ClientAddress],
    ) -> None:
        log.exception(f'Server error request={request!r} client_address={client_address!r}')

    def process_request(self, request: sock.socket, client_address: ClientAddress) -> None:
        try:
            self.handle_request(request, client_address)
            self.shutdown_request(request)

        except Exception as e:  # noqa
            self.handle_error(request, client_address)
            self.shutdown_request(request)

    @abc.abstractmethod
    def handle_request(self, request: sock.socket, client_address: ClientAddress) -> None:
        raise NotImplementedError

    def shutdown_request(self, request: sock.socket) -> None:
        try:
            # explicitly shutdown. socket.close() merely releases the socket and waits
            # for GC to perform the actual close.
            request.shutdown(sock.SHUT_WR)

        except OSError:
            # some platforms may raise ENOTCONN here
            pass

        request.close()

    def shutdown(self, block=False, timeout=None):
        self._should_shutdown = True
        if block:
            self._is_shutdown.wait(timeout=timeout)
