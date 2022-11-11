"""
TODO:
 - sql
 - redis
 - zk

https://curator.apache.org/
https://github.com/obsidiandynamics/goneli
https://www.micahlerner.com/2020/05/08/understanding-raft-consensus.html
"""
import abc
import typing as ta

from .. import lang


class Lease(lang.ContextManaged, lang.Abstract):
    pass


class TimeoutException(Exception):
    pass


class Object(lang.Abstract):

    @abc.abstractproperty
    def name(self) -> str:
        raise NotImplementedError


class Acquirable(lang.ContextManaged, lang.Abstract):

    @abc.abstractmethod
    def acquire(self, *, timeout: ta.Optional[float] = None) -> Lease:
        raise NotImplementedError


class Lock(Object, Acquirable, lang.Abstract):
    pass


class Semaphore(Object, Acquirable, lang.Abstract):
    pass


class Event(Object, lang.ContextManaged, lang.Abstract):

    @abc.abstractmethod
    def is_set(self) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def set(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def clear(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def wait(self, timeout: ta.Optional[float] = None) -> None:
        raise NotImplementedError


class Coordination(lang.ContextManaged, lang.Abstract):

    @abc.abstractmethod
    def lock(self, name: str) -> Lock:
        raise NotImplementedError

    @abc.abstractmethod
    def semaphore(self, name: str, value: int) -> Semaphore:
        raise NotImplementedError

    @abc.abstractmethod
    def event(self, name: str) -> Event:
        raise NotImplementedError
