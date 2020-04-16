"""
TODO:
 - streaming
 - interops
  - csvloader
"""
import abc
import typing as ta


F = ta.TypeVar('F')
T = ta.TypeVar('T')


class Encoder(ta.Generic[F, T]):

    @abc.abstractmethod
    def encode(self, obj: F) -> T:
        raise NotImplementedError


class Decoder(ta.Generic[F, T]):

    @abc.abstractmethod
    def decode(self, obj: T) -> F:
        raise NotImplementedError


class Codec(Encoder[F, T], Decoder[F, T]):
    pass
