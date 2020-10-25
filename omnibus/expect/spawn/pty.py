import typing as ta

from ... import lang
from .base import BaseSpawn


class PtySpawn(BaseSpawn, lang.Abstract):

    def __init__(
            self,
            command: ta.Sequence[str],
    ) -> None:
        super().__init__(command)

    def write(self, buf: bytes) -> int:
        raise NotImplementedError

    def write_eof(self) -> None:
        raise NotImplementedError

    def read_nb(self, size: int, timeout: ta.Union[int, float, None] = None) -> bytes:
        raise NotImplementedError
