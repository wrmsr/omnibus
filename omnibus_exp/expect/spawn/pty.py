import typing as ta

from ... import lang
from .base import BaseSpawn


class PtySpawn(BaseSpawn, lang.Abstract):

    def __init__(
            self,
            command: ta.Sequence[str],
    ) -> None:
        super().__init__(command)

    def write(self, buf: ta.Optional[bytes]) -> int:
        raise NotImplementedError

    def read(self, size: int, timeout: ta.Union[int, float, None] = None) -> bytes:
        raise NotImplementedError
