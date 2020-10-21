import os.path
import socket
import tempfile


socket.SO_PASSCRED = 16
socket.SO_PEERCRED = 17


def test_unixsocket():
    fp = os.path.join(tempfile.mkdtemp(), 't.sock')
    srv = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    srv.bind(fp)
    srv.listen(1)

    cli = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    cli.setsockopt(socket.SOL_SOCKET, socket.SO_PASSCRED, 1)
    cli.connect(fp)

    conn, _ = srv.accept()
    cli.send(b'hi')
    buf = conn.recv(1024)
    assert buf == b'hi'

    cli.close()
    srv.close()
