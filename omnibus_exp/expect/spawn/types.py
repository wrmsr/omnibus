import abc
import typing as ta

from ... import lang


class Spawn(lang.Abstract):

    @abc.abstractmethod
    def write(self, buf: ta.Optional[bytes]) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def read(self, size: int, timeout: ta.Union[int, float, None] = None) -> bytes:
        raise NotImplementedError

    def close(self) -> None:
        pass
