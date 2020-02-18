"""
TODO:
- threadpool
- greenlet?
- eventfd
- https://github.com/MagicStack/httptools
- https://gist.github.com/mitsuhiko/5721547
- asyncio
- firehose
"""
import abc
import collections.abc
import contextlib
import datetime
import http  # noqa
import http.server
import json
import logging
import os
import selectors
import socket as sock
import stat
import sys
import threading
import time
import traceback
import types
import typing as ta
import wsgiref.handlers
import wsgiref.simple_server

from . import check
from . import lang


log = logging.getLogger(__name__)


Self = ta.TypeVar('Self')
ClientAddress = ta.Tuple[str, int]
Environ = ta.Dict[str, ta.Any]
StartResponse = ta.Callable[[str, ta.List[ta.Tuple[str, str]]], ta.Callable[[lang.BytesLike], None]]
RawApp = ta.Callable[[Environ, StartResponse], ta.Iterable[lang.BytesLike]]
AppLike = ta.Union['App', RawApp]
BadRequestExceptionT = ta.TypeVar('BadRequestExceptionT', bound='BadRequestException')


class BadRequestException(Exception):
    pass


def format_status(status: http.HTTPStatus) -> str:
    return '%d %s' % (int(status), status.phrase)


STATUS_OK = format_status(http.HTTPStatus.OK)
STATUS_BAD_REQUEST = format_status(http.HTTPStatus.BAD_REQUEST)
STATUS_FORBIDDEN = format_status(http.HTTPStatus.FORBIDDEN)
STATUS_NOT_FOUND = format_status(http.HTTPStatus.NOT_FOUND)
STATUS_METHOD_NOT_ALLOWED = format_status(http.HTTPStatus.METHOD_NOT_ALLOWED)

CONTENT_TYPE = 'Content-Type'
CONTENT_TEXT = 'text/plain'
CONTENT_JSON = 'application/json'
CONTENT_ICON = 'image/x-icon'
CONTENT_BYTES = 'application/octet-stream'


class App(lang.Abstract):

    def __enter__(self: Self) -> Self:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        return None

    @abc.abstractmethod
    def __call__(self, environ: Environ, start_response: StartResponse) -> ta.Iterable[bytes]:
        raise NotImplementedError


class WrapperApp(App):

    def __init__(self, app: AppLike, **kwargs) -> None:
        super().__init__(**kwargs)

        self._app = app

    @property
    def app(self) -> AppLike:
        return self._app

    def __enter__(self: Self) -> Self:
        if hasattr(self._app, '__enter__'):
            self._app.__enter__()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> ta.Any:
        if hasattr(self._app, '__exit__'):
            return self._app.__exit__(exc_type, exc_val, exc_tb)
        else:
            return None

    def __call__(self, environ: Environ, start_response: StartResponse) -> ta.Iterable[bytes]:
        return self._app(environ, start_response)


ADDRESS_FAMILY_NAMES = {
    value: name
    for name in dir(sock)
    if name.startswith('AF_')
    for value in [getattr(sock, name)]
    if isinstance(value, int)
}


class Binder(lang.Abstract):

    @abc.abstractproperty
    def address_family(self) -> int:
        raise NotImplementedError

    _name: str = None

    @property
    def name(self) -> str:
        return self._name

    _port: int = None

    @property
    def port(self) -> int:
        return self._port

    _socket: sock.socket = None

    @property
    def socket(self) -> sock.socket:
        if self._socket is None:
            raise TypeError('Not bound')
        return self._socket

    @abc.abstractmethod
    def _init_socket(self) -> None:
        raise NotImplementedError

    def fileno(self) -> int:
        return self.socket.fileno()

    def __enter__(self: Self) -> Self:
        if self._socket is not None:
            raise TypeError('Already initialized')
        self._init_socket()
        if not isinstance(self._socket, sock.socket):
            raise TypeError('Initialization failure')

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._socket is not None:
            self._socket.close()

    listen_backlog = 5

    def listen(self) -> None:
        self.socket.listen(self.listen_backlog)

    @abc.abstractmethod
    def accept(self, socket: ta.Optional[sock.socket] = None) -> ta.Tuple[sock.socket, ClientAddress]:
        raise NotImplementedError

    @classmethod
    def new(cls, target: ta.Union[ta.Tuple[str, int], str]) -> 'Binder':
        if isinstance(target, str):
            return UnixBinder(target)

        elif isinstance(target, tuple):
            host, port = target
            if not isinstance(host, str) or not isinstance(port, int):
                raise TypeError(target)
            return TCPBinder(host, port)

        elif isinstance(target, Binder):
            return DupBinder(target)

        else:
            raise TypeError(target)


class DupBinder(Binder):

    def __init__(self, target: Binder) -> None:
        super().__init__()

        self._target = target

    @property
    def address_family(self) -> int:
        return self._target.address_family

    @property
    def name(self) -> str:
        return self._target.name

    @property
    def port(self) -> int:
        return self._target.port

    def _init_socket(self) -> None:
        log.info(f'Duplicating {self._target} as {ADDRESS_FAMILY_NAMES[self._target.address_family]}')
        self._socket = sock.fromfd(self._target.fileno(), self.address_family, sock.SOCK_STREAM)

    def accept(self, socket: ta.Optional[sock.socket] = None) -> ta.Tuple[sock.socket, ClientAddress]:
        if socket is None:
            socket = self.socket
        return self._target.accept(socket)


class BindBinder(Binder):

    _address: ta.Any = None

    allow_reuse_address = True

    def _init_socket(self) -> None:
        self._socket = sock.socket(self.address_family, sock.SOCK_STREAM)

        if self.allow_reuse_address:
            self.socket.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)

        # if hasattr(socket, 'SO_REUSEPORT'):
        #     try:
        #         self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        #     except socket.error as err:
        #         if err.errno not in (errno.ENOPROTOOPT, errno.EINVAL):
        #             raise

        # if hasattr(self.socket, 'set_inheritable'):
        #     self.socket.set_inheritable(True)

        log.info(f'Binding {self._address} as {ADDRESS_FAMILY_NAMES[self.address_family]}')
        self.socket.bind(self._address)
        self._post_bind()

    @abc.abstractmethod
    def _post_bind(self) -> None:
        raise NotImplementedError


class TCPBinder(BindBinder):

    address_family = sock.AF_INET

    def __init__(self, host: str, port: int) -> None:
        super().__init__()

        self._address = (host, port)

    def _post_bind(self) -> None:
        host, port, *_ = self.socket.getsockname()
        self._name = sock.getfqdn(host)
        self._port = port

    def accept(self, socket: ta.Optional[sock.socket] = None) -> ta.Tuple[sock.socket, ClientAddress]:
        if socket is None:
            socket = self.socket
        conn, client_address = socket.accept()
        return conn, client_address


class UnixBinder(BindBinder):

    address_family = sock.AF_UNIX

    def __init__(self, address: str) -> None:
        super().__init__()

        self._address = address

    def _post_bind(self) -> None:
        name = self.socket.getsockname()
        os.chmod(name, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        self._name = name
        self._port = 0

    def accept(self, socket: ta.Optional[sock.socket] = None) -> ta.Tuple[sock.socket, ClientAddress]:
        if socket is None:
            socket = self.socket
        conn, _ = socket.accept()
        client_address = ('', 0)
        return conn, client_address


class WSGIRefProtocol(lang.Protocol):

    @property
    def server_name(self) -> str:
        raise NotImplementedError

    @property
    def server_port(self) -> int:
        raise NotImplementedError

    @property
    def base_environ(self) -> App:
        raise NotImplementedError

    def get_app(self) -> App:
        raise NotImplementedError

    def handle_error(self, request: sock.socket, client_address: ClientAddress) -> None:
        raise NotImplementedError


@WSGIRefProtocol
class WSGIServer:

    Handler = ta.Callable[[sock.socket, ClientAddress, 'WSGIServer'], None]

    if hasattr(selectors, 'PollSelector'):
        ServerSelector = selectors.PollSelector
    else:
        ServerSelector = selectors.SelectSelector

    base_environ: ta.Dict[str, ta.Any] = None

    def __init__(
            self,
            binder: Binder,
            app,
            *,
            handler: Handler = wsgiref.simple_server.WSGIRequestHandler,
            poll_interval: float = 0.5,
            exit_timeout: float = 10.0,
            **kwargs
    ) -> None:
        super().__init__(**kwargs)

        self._binder = binder
        self._app = app
        self._handler = handler
        self._poll_interval = poll_interval
        self._exit_timeout = exit_timeout

        self._lock = threading.RLock()
        self._shutdown_event = threading.Event()
        self._should_shutdown = False

    def __enter__(self: Self) -> Self:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        acquired = self._lock.acquire(False)
        if not acquired:
            try:
                if not self._shutdown_event.is_set():
                    self.shutdown(True, self._exit_timeout)
            finally:
                self._lock.release()

    def get_app(self) -> App:
        return self._app

    @property
    def server_name(self) -> str:
        return self._binder.name

    @property
    def server_port(self) -> int:
        return self._binder.port

    def run(self, poll_interval=None) -> None:
        if poll_interval is None:
            poll_interval = self._poll_interval

        with contextlib.ExitStack() as exit_stack:
            exit_stack.enter_context(self._lock)
            exit_stack.enter_context(self._binder)

            env = self.base_environ = {}
            env['SERVER_NAME'] = self.server_name
            env['GATEWAY_INTERFACE'] = 'CGI/1.1'
            env['SERVER_PORT'] = str(self.server_port)
            env['REMOTE_HOST'] = ''
            env['CONTENT_LENGTH'] = ''
            env['SCRIPT_NAME'] = ''

            self._binder.listen()

            self._shutdown_event.clear()
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
                self._shutdown_event.set()

    def handle_error(self, request: sock.socket, client_address: ClientAddress) -> None:
        log.exception(f'Server error request={request!r} client_address={client_address!r}')

    def process_request(self, request: sock.socket, client_address: ClientAddress) -> None:
        try:
            self._handler(request, client_address, self)
            self.shutdown_request(request)

        except Exception:
            self.handle_error(request, client_address)
            self.shutdown_request(request)

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
            self._shutdown_event.wait(timeout=timeout)


class SerialWSGIServer(WSGIServer):
    pass


class ThreadedWSGIServer(WSGIServer):

    def process_request(self, request: sock.socket, client_address: ClientAddress) -> None:
        thread = threading.Thread(target=super().process_request, args=(request, client_address))
        thread.start()


def read_input(environ):
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except ValueError:
        request_body_size = 0

    return environ['wsgi.input'].read(request_body_size)


class SimpleDictApp(App):

    class _BadRequestHandledException(Exception):
        pass

    Target = ta.Callable[[ta.Dict[str, ta.Any]], ta.Dict[str, ta.Any]]

    def __init__(
            self,
            target: Target,
            encode: ta.Callable[[ta.Any], ta.Any],
            decode: ta.Callable[[ta.Any], ta.Any],
            content_type: str,
            *,
            stream: bool = False,
            stream_separator: bytes = b'\n',
            stream_terminator: bytes = b'\0',
            handle_bad_requests: bool = False,
            on_bad_request: ta.Callable[[ta.Type[BadRequestExceptionT], BadRequestExceptionT, types.TracebackType], None] = None,  # noqa
            **kwargs
    ) -> None:
        super().__init__(**kwargs)

        self._target = target
        self._encode = encode
        self._decode = decode
        self._content_type = content_type

        self._stream = stream
        self._stream_separator = stream_separator
        self._stream_terminator = stream_terminator

        self._handle_bad_requests = handle_bad_requests
        self._on_bad_request = on_bad_request

    def __call__(self, environ: Environ, start_response: StartResponse) -> ta.Iterable[bytes]:
        request_body = read_input(environ)

        if request_body:
            input = self._decode(request_body)
        else:
            input = None

        @contextlib.contextmanager
        def bad_request_manager():
            if not self._handle_bad_requests:
                yield
                return

            try:
                yield
            except BadRequestException:
                exc_info = sys.exc_info()
                if self._on_bad_request is not None:
                    self._on_bad_request(*exc_info)
                write = start_response(STATUS_BAD_REQUEST, [CONTENT_TEXT], exc_info=exc_info)
                write('\n'.join(traceback.TracebackException(*exc_info).format()).encode('utf-8'))
                raise self._BadRequestHandledException

        try:
            with bad_request_manager():
                output = self._target(input)
        except self._BadRequestHandledException:
            return []

        start_response(STATUS_OK, [(CONTENT_TYPE, self._content_type)])

        if output is None:
            return []

        elif isinstance(output, collections.Iterator):
            if not self._stream:
                raise TypeError(output)

            def inner():
                try:
                    with bad_request_manager():
                        for item in output:
                            yield self._encode(item)
                            yield self._stream_separator
                        yield self._stream_terminator
                except self._BadRequestHandledException:
                    pass

            return inner()

        else:
            return [self._encode(output)]


def simple_json_app(target: SimpleDictApp.Target) -> App:
    return SimpleDictApp(
        target,
        lambda request_body: json.loads(request_body.decode('utf-8')),
        lambda output: json.dumps(output).encode('utf-8'),
        CONTENT_JSON,
    )


def format_date(when: datetime.datetime = None) -> str:
    if when is None:
        when = datetime.datetime.now()
    return wsgiref.handlers.format_date_time(time.mktime(when.timetuple()))


def read_scgi_headers(socket: sock.socket) -> ta.Dict[bytes, bytes]:
    header_size = 0
    while True:
        char = socket.recv(1)
        if char == b':':
            break
        header_size = (header_size * 10) + int(char)
    check.state(header_size > 0)
    header_buf = socket.recv(header_size + 1)
    check.state(header_buf[-2:] == b'\0,')
    header_items = header_buf[:-2].split(b'\0')
    check.state(len(header_items) % 2 == 0)
    return dict(zip(header_items[::2], header_items[1::2]))
