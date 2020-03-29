"""
socat - UNIX-CONNECT:repl.sock
"""
import contextlib
import functools
import logging
import os
import socket as sock
import threading
import typing as ta
import weakref

from .. import check
from .. import lifecycles
from .console import InteractiveSocketConsole


log = logging.getLogger(__name__)


class ReplServer(lifecycles.ContextManageableLifecycle):

    CONNECTION_THREAD_NAME = 'ReplServerConnection'

    def __init__(
            self,
            path: str,
            *,
            file_mode: int = None,
            poll_interval: float = 0.5,
            exit_timeout: float = 10.0,
    ) -> None:
        super().__init__()

        self._path = path
        self._file_mode = file_mode
        self._poll_interval = poll_interval
        self._exit_timeout = exit_timeout

        self._socket: sock.socket = None
        self._is_running = False
        self._consoles_by_threads: ta.MutableMapping[threading.Thread, InteractiveSocketConsole] = weakref.WeakKeyDictionary()  # noqa
        self._is_shutdown = threading.Event()
        self._should_shutdown = False

    def _do_lifecycle_start(self) -> None:
        check.state(not self._is_running)
        check.state(not self._is_shutdown.is_set())

    def _do_lifecycle_stop(self) -> None:
        if not self._is_shutdown.is_set():
            self.shutdown(True, self._exit_timeout)

    def run(self) -> None:
        check.state(not self._is_running)
        check.state(not self._is_shutdown.is_set())

        if os.path.exists(self._path):
            os.unlink(self._path)

        self._socket = sock.socket(sock.AF_UNIX, sock.SOCK_STREAM)
        self._socket.settimeout(self._poll_interval)
        self._socket.bind(self._path)
        with contextlib.closing(self._socket):
            self._socket.listen(1)

            log.info(f'Repl server listening on file {self._path}')

            self._is_running = True
            try:
                while not self._should_shutdown:
                    try:
                        conn, _ = self._socket.accept()
                    except sock.timeout:
                        continue

                    log.info(f'Got repl server connection on file {self._path}')

                    def run(conn):
                        with contextlib.closing(conn):
                            variables = globals().copy()

                            console = InteractiveSocketConsole(conn, variables)
                            variables['__console__'] = console

                            log.info(
                                f'Starting console {id(console)} repl server connection '
                                f'on file {self._path} '
                                f'on thread {threading.current_thread().ident}'
                            )
                            self._consoles_by_threads[threading.current_thread()] = console
                            console.interact()

                    thread = threading.Thread(
                        target=functools.partial(run, conn),
                        daemon=True,
                        name=self.CONNECTION_THREAD_NAME)
                    thread.start()

                for thread, console in self._consoles_by_threads.items():
                    try:
                        console.conn.close()
                    except Exception:
                        log.exception('Error shutting down')

                for thread in self._consoles_by_threads.keys():
                    try:
                        thread.join(self._exit_timeout)
                    except Exception:
                        log.exception('Error shutting down')

                os.unlink(self._path)

            finally:
                self._is_shutdown.set()
                self._is_running = False

    def shutdown(self, block: bool = False, timeout: float = None) -> None:
        self._should_shutdown = True
        if block:
            self._is_shutdown.wait(timeout=timeout)


def run():
    with ReplServer('repl.sock') as repl_server:
        repl_server.run()
