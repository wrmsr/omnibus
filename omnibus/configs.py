import abc
import typing as ta

from . import lang


lang.warn_unstable()


ConfigT = ta.TypeVar('ConfigT', bound='Config')


class Config(lang.Abstract):
    pass


class Source(lang.Abstract):

    @abc.abstractmethod
    def get(self, cls: ta.Type[ConfigT]) -> ConfigT:
        raise NotImplementedError

    # @abc.abstractmethod
    # def get_child(self, cls: ta.Type[ConfigT]) -> ConfigT:
    #     raise NotImplementedError
