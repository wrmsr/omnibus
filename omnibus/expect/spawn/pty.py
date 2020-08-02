import typing as ta

from ... import lang
from .base import BaseSpawn


class PtySpawn(BaseSpawn, lang.Abstract):

    def __init__(
            self,
            command: ta.Sequence[str],
    ) -> None:
        super().__init__(command)
