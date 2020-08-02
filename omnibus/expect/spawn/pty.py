import typing as ta

from .base import BaseSpawn


class PtySpawn(BaseSpawn):

    def __init__(
            self,
            command: ta.Sequence[str],
    ) -> None:
        super().__init__(command)
