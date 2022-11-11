"""
TODO:
 - registry/dispatch
 - heapq
"""
import abc
import logging
import queue
import time
import typing as ta

from .. import check
from .. import collections as ocol
from .. import dataclasses as dc


log = logging.getLogger(__name__)

T = ta.TypeVar('T')
K = ta.TypeVar('K')
O = ta.TypeVar('O')


class Telegram(dc.Pure, ta.Generic[T]):
    sender: ta.Optional['Telegraph']
    receiver: ta.Optional['Telegraph']
    message: T
    needs_return_receipt: bool = False

    def __post_init__(self) -> None:
        if isinstance(self.message, type):
            raise TypeError(self.message)


class ReturnReceipt(dc.Pure):
    telegram: Telegram


class Telegraph(abc.ABC):

    @abc.abstractmethod
    def handle_message(self, telegram: Telegram) -> bool:
        raise NotImplementedError


class TelegramProvider(abc.ABC):

    @abc.abstractmethod
    def provide_message(self, receiver: Telegraph, message_type: ta.Type[T]) -> ta.Optional[T]:
        raise NotImplementedError


class Delayed(dc.Pure):
    telegram: Telegram
    timestamp: float


class SimpleRegistry(ta.Generic[K, O]):

    def __init__(self, *, add_callback: ta.Callable[[O, K], None] = None) -> None:
        super().__init__()

        self._sets_by_key: ta.Dict[K, ta.MutableSet[O]] = {}
        self._add_callback = add_callback

    def get(self, key: K) -> ta.AbstractSet[O]:
        check.not_none(key)
        return self._sets_by_key.get(key, set())

    def add(self, obj: O, key: K) -> None:
        self._sets_by_key.setdefault(key, ocol.IdentitySet()).add(obj)
        if self._add_callback is not None:
            self._add_callback(obj, key)

    def remove(self, obj: O, key: K = None) -> None:
        for key in ([key] if key is not None else list(self._sets_by_key.keys())):
            try:
                self._sets_by_key[key].remove(obj)
            except KeyError:
                pass

    def clear(self, key: K = None) -> None:
        if key is not None:
            self._sets_by_key.clear()
        else:
            try:
                del self._sets_by_key[key]
            except KeyError:
                pass


class Dispatcher(Telegraph):

    def __init__(self) -> None:
        super().__init__()

        self._queue = queue.PriorityQueue()
        self._listeners: SimpleRegistry[type, Telegraph] = SimpleRegistry(add_callback=self._on_add_listener)
        self._providers: SimpleRegistry[type, TelegramProvider] = SimpleRegistry()

    @property
    def listeners(self) -> SimpleRegistry[type, Telegraph]:
        return self._listeners

    @property
    def providers(self) -> SimpleRegistry[type, TelegramProvider]:
        return self._providers

    def _on_add_listener(self, receiver: Telegraph, message_type: type) -> None:
        for provider in self._providers.get(message_type):
            message = provider.provide_message(receiver, message_type)
            if message is not None:
                self.dispatch(
                    provider if isinstance(provider, Telegraph) else None,
                    receiver,
                    message,
                )

    def dispatch(
            self,
            sender: ta.Optional[Telegraph],
            receiver: ta.Optional[Telegraph],
            message: T,
            *,
            delay: float = None,
            needs_return_receipt: bool = False,
    ) -> None:
        if needs_return_receipt:
            check.not_none(sender)

        telegram = Telegram(
            sender,
            receiver,
            message,
            needs_return_receipt=needs_return_receipt,
        )

        if not delay or delay <= 0.:
            self._discharge(telegram)
        else:
            self._queue.put(Delayed(telegram, time.time() + delay))

    def _discharge(self, telegram: Telegram) -> None:
        if telegram.receiver is not None:
            if not telegram.receiver.handle_message(telegram):
                log.error(f'Message not handled: {telegram}')

        else:
            num_handled = 0
            for listener in self._listeners[type(telegram.message)]:
                if listener.handle_message(telegram):
                    num_handled += 1
            if not num_handled:
                log.error(f'Message not handled: {telegram}')

        if telegram.needs_return_receipt:
            receipt_telegram = Telegram(
                self,
                telegram.sender,
                telegram,
            )
            self._discharge(receipt_telegram)

    def handle_message(self, telegram: Telegram) -> bool:
        return False

    def update(self) -> None:
        while not self._queue.empty():
            cur: Delayed = self._queue.get(block=False)
            if cur.timestamp > time.time():
                self._queue.put(cur)
                break
            self._discharge(cur.telegram)
