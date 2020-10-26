"""
TODO:
 - external Encoding[T], [str], [bytes]
 - switchable err+out fusing
 - close/wait timeout
"""
import io
import os
import queue
import subprocess
import threading
import time
import typing as ta

from ... import check
from ..exceptions import EofException
from .base import BaseSpawn


class PopenSpawn(BaseSpawn):

    def __init__(
            self,
            command: ta.Sequence[str],
            *,
            read_chunk_size: int = 0xFFFF,
    ) -> None:
        super().__init__(command)

        read_chunk_size = int(read_chunk_size)
        check.arg(read_chunk_size > 0)
        self._read_chunk_size = read_chunk_size

        self._proc = subprocess.Popen(
            self._command,
            bufsize=0,
            stdin=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
        )

        self._read_buf = io.BytesIO()
        self._read_eof = False

        self._read_queue = queue.Queue()
        self._read_thread = threading.Thread(target=self._read_proc, daemon=True)
        self._read_thread.start()

    def write(self, buf: ta.Optional[bytes]) -> int:
        if buf is None:
            self._proc.stdin.close()
        else:
            return self._proc.stdin.write(buf)

    def read(self, size: int, timeout: ta.Union[int, float, None] = None) -> bytes:
        if size < 1:
            raise ValueError(size)

        if self._read_eof:
            ret = self._read_buf.read(size)
            if ret:
                return ret
            raise EofException

        chunk = self._read_buf.read(size)
        if chunk:
            if len(chunk) > size:
                raise ValueError
            elif len(chunk) == size:
                return chunk
        if self._read_buf.tell():
            self._read_buf = io.BytesIO()
        buf = io.BytesIO()
        buf.write(chunk)

        start = time.time()
        while (timeout is None or (time.time() - start) < timeout) and buf.tell() < size:
            try:
                chunk = self._read_queue.get_nowait()
            except queue.Empty:
                break
            else:
                if not chunk:
                    self._read_eof = True
                    break
                buf.write(chunk)

        buf.seek(0)
        chunk = buf.read(size)
        self._read_buf.write(buf.read())
        self._read_buf.seek(0)
        return chunk

    def _read_proc(self) -> None:
        fd = self._proc.stdout.fileno()
        while True:
            try:
                chunk = os.read(fd, self._read_chunk_size)
            except OSError:
                continue
            self._read_queue.put(chunk)
            if not chunk:
                return

    def close(self) -> None:
        if self._proc.poll() is None:
            self._proc.kill()
            self._proc.wait()

        if self._read_thread.is_alive():
            self._read_thread.join()

        super().close()
