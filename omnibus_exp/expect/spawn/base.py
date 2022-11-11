import typing as ta

from ... import check
from ... import lang
from .types import Spawn


class BaseSpawn(Spawn, lang.Abstract):

    def __init__(
            self,
            command: ta.Sequence[str],
    ) -> None:
        super().__init__()

        self._command = check.not_empty(list(check.not_isinstance(command, str)))
