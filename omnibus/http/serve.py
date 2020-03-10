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
import contextlib
import logging
import selectors
import socket as sock
import threading
import typing as ta
import wsgiref.simple_server

from .. import lang
from .apps import App
from .bind import Binder


log = logging.getLogger(__name__)


Self = ta.TypeVar('Self')
ClientAddress = ta.Tuple[str, int]


"""
FIXME: jettison wsgiref?

try:
    import httptools

except ImportError:
    pass

else:
    class HttpToolsRequestParserListener:

        def on_message_begin(self):
            pass

        def on_url(self, url: bytes):
            pass

        def on_header(self, name: bytes, value: bytes):
            pass

        def on_headers_complete(self):
            pass

        def on_body(self, body: bytes):
            pass

        def on_message_complete(self):
            pass

        def on_chunk_header(self):
            pass

        def on_chunk_complete(self):
            pass

        def on_status(self, status: bytes):
            pass

    # self.headers = http.client.parse_headers(self.rfile, _class=self.MessageClass)

    def httptools_parse_headers(fp, _class=http.client.HTTPMessage):
        l = HttpToolsRequestParserListener()
        p = httptools.HttpResponseParser(l)
        # p.feed_data(b'POST /test HTTP/1.1\r\n')
        while True:
            line = fp.readline()
            if not line:
                break
            p.feed_data(line)
        raise NotImplementedError

    http.client.parse_headers = httptools_parse_headers


====


import asyncio

from httptools import HttpRequestParser


class Request:

    def __init__(self):
        self.EOF = False

    def on_url(self, url: bytes):
        self.on_url_called = True

    def on_message_complete(self):
        self.EOF = True


async def serve(reader, writer):
    chunks = 2 ** 16
    req = Request()
    parser = HttpRequestParser(req)
    while True:
        data = await reader.read(chunks)
        parser.feed_data(data)
        if not data or req.EOF:
            break
    assert req.on_url_called
    writer.write(b'HTTP/1.1 200 OK\r\nContent-Length: 2\r\n\r\nOK')
    writer.write_eof()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    coro = loop.create_task(asyncio.start_server(serve, '127.0.0.1', 8080))
    server = loop.run_until_complete(coro)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print('Bye.')
    finally:
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()
"""


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

    class RequestHandler(wsgiref.simple_server.WSGIRequestHandler):

        def parse_request(self) -> bool:
            return super().parse_request()

    def __init__(
            self,
            binder: Binder,
            app,
            *,
            handler: Handler = RequestHandler,
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
        self._is_shutdown = threading.Event()
        self._should_shutdown = False

    def __enter__(self: Self) -> Self:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        acquired = self._lock.acquire(False)
        if not acquired:
            try:
                if not self._is_shutdown.is_set():
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
            self._handler(request, client_address, self)
            self.shutdown_request(request)

        except Exception as e:  # noqa
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
            self._is_shutdown.wait(timeout=timeout)


class SerialWSGIServer(WSGIServer):
    pass


class ThreadSpawningWSGIServer(WSGIServer):

    def process_request(self, request: sock.socket, client_address: ClientAddress) -> None:
        thread = threading.Thread(target=super().process_request, args=(request, client_address))
        thread.start()
