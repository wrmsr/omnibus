"""
socat - UNIX-CONNECT:repl.sock


import sys, threading, pdb, functools
def _attach(repl):
    frame = sys._current_frames()[threading.enumerate()[0].ident]
    debugger = pdb.Pdb(
        stdin=repl.conn.makefile('r'),
        stdout=repl.conn.makefile('w'),
    )
    debugger.reset()
    while frame:
        frame.f_trace = debugger.trace_dispatch
        debugger.botframe = frame
        frame = frame.f_back
    debugger.set_step()
    frame.f_trace = debugger.trace_dispatch
"""
import ast
import codeop
import contextlib
import errno
import functools
import logging
import os
import socket as sock
import sys
import threading
import traceback
import types
import typing as ta
import weakref

from . import check


log = logging.getLogger(__name__)


class DisconnectException(Exception):
    pass


class InteractiveSocketConsole:
    """code.InteractiveConsole but just different enough to not be worth subclassing."""

    ENCODING = 'utf-8'

    def __init__(
            self,
            conn: sock.socket,
            locals: ta.MutableMapping = None,
            filename: str = '<console>'
    ) -> None:
        super().__init__()

        if locals is None:
            locals = {
                '__name__': '__console__',
                '__doc__': None,
                '__console__': self,
            }

        self._conn = conn
        self._locals = locals
        self._filename = filename

        self._compiler = codeop.CommandCompiler()
        self._buffer: ta.List[str] = []
        self._count = 0
        self._write_count = -1

    def reset_buffer(self) -> None:
        self._buffer = []

    @property
    def conn(self) -> sock.socket:
        return self._conn

    CPRT = 'Type "help", "copyright", "credits" or "license" for more information.'

    def interact(self, banner: str = None, exitmsg: str = None) -> None:
        log.info(f'Console {id(self)} on thread {threading.current_thread().ident} interacting')

        try:
            ps1 = getattr(sys, 'ps1', '>>> ')
            ps2 = getattr(sys, 'ps2', '... ')

            if banner is None:
                self.write(
                    'Python %s on %s\n%s\n(%s)\n' %
                    (sys.version, sys.platform, self.CPRT, self.__class__.__name__))
            elif banner:
                self.write('%s\n' % (str(banner),))

            more = False
            while True:
                try:
                    try:
                        line = self.raw_input(ps2 if more else ps1)
                    except EOFError:
                        self.write('\n')
                        break
                    else:
                        more = self.push_line(line)

                except KeyboardInterrupt:
                    self.write('\nKeyboardInterrupt\n')
                    self.reset_buffer()
                    more = False

            if exitmsg is None:
                self.write('now exiting %s...\n' % self.__class__.__name__)

            elif exitmsg != '':
                self.write('%s\n' % exitmsg)

        except DisconnectException:
            pass

        except OSError as oe:
            if oe.errno == errno.EBADF:
                pass

        finally:
            log.info(f'Console {id(self)} on thread {threading.current_thread().ident} finished')

    def push_line(self, line: str) -> bool:
        self._buffer.append(line)
        source = '\n'.join(self._buffer)
        more = self.run_source(source, self._filename)
        if not more:
            self.reset_buffer()
        return more

    def raw_input(self, prompt: str = '') -> str:
        self.write(prompt)
        buf = b''
        while True:
            b = self._conn.recv(1)
            if not b:
                raise DisconnectException
            if b == b'\n':
                break
            buf += b
        return buf.decode(self.ENCODING)

    def write(self, data: str) -> None:
        self._conn.send(data.encode(self.ENCODING))

    def compile(
            self,
            source: ta.Union[str, ast.AST],
            filename: str = '<input>',
            symbol: str = 'single'
    ) -> ta.Optional[types.CodeType]:
        if isinstance(source, ast.AST):
            return self._compiler.compiler(source, filename, symbol)
        else:
            return self._compiler(source, filename, symbol)

    def run_source(
            self,
            source: ta.Union[str, ast.AST],
            filename: str = '<input>',
            symbol: str = 'single',
    ) -> bool:
        try:
            code = self.compile(source, filename, symbol)
        except (OverflowError, SyntaxError, ValueError):
            # Case 1 (incorrect)
            self.show_syntax_error(filename)
            return False

        if code is None:
            # Case 2 (incomplete)
            return True

        # Case 3 (complete)
        try:
            node = ast.parse(source)
        except (OverflowError, SyntaxError, ValueError):
            return True

        if isinstance(node, ast.Module) and node.body and isinstance(node.body[-1], ast.Expr):
            expr = node.body[-1]
            source = ast.Interactive(
                [
                    *node.body[:-1],
                    ast.Assign(
                        [ast.Name(
                            f'_{self._count}',
                            ast.Store(),
                            lineno=expr.lineno,
                            col_offset=expr.col_offset,
                        )],
                        expr.value,
                        lineno=expr.lineno,
                        col_offset=expr.col_offset,
                    )
                ],
            )
            ast.fix_missing_locations(source)
            self._write_count = self._count

        code = self.compile(source, filename, symbol)
        self.run_code(code)
        return False

    def run_code(self, code: types.CodeType) -> None:
        try:
            exec(code, self._locals)
        except SystemExit:
            raise
        except Exception:
            self.show_traceback()
        else:
            if self._count == self._write_count:
                self.write(repr(self._locals[f'_{self._count}']))
                self.write('\n')
                self._count += 1

    def show_traceback(self) -> None:
        sys.last_type, sys.last_value, last_tb = ei = sys.exc_info()
        sys.last_traceback = last_tb
        try:
            lines = traceback.format_exception(ei[0], ei[1], last_tb.tb_next)
            self.write(''.join(lines))
        finally:
            last_tb = ei = None

    def show_syntax_error(self, filename: str = None) -> None:
        type, value, tb = sys.exc_info()
        sys.last_type = type
        sys.last_value = value
        sys.last_traceback = tb
        if filename and type is SyntaxError:
            # Work hard to stuff the correct filename in the exception
            try:
                msg, (dummy_filename, lineno, offset, line) = value.args
            except ValueError:
                # Not the format we expect; leave it alone
                pass
            else:
                # Stuff in the right filename
                value = SyntaxError(msg, (filename, lineno, offset, line))
                sys.last_value = value
        lines = traceback.format_exception_only(type, value)
        self.write(''.join(lines))


class ReplServer:

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

    def __enter__(self):
        check.state(not self._is_running)
        check.state(not self._is_shutdown.is_set())

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
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


def _main():
    with ReplServer('repl.sock') as repl_server:
        repl_server.run()


if __name__ == '__main__':
    _main()
