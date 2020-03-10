import abc
import logging
import os
import socket as sock
import stat
import typing as ta

from .. import lang


log = logging.getLogger(__name__)


Self = ta.TypeVar('Self')
ClientAddress = ta.Tuple[str, int]


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