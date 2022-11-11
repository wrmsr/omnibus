import typing as ta

from .. import msgs


def test_msgs():
    disp = msgs.Dispatcher()

    class A(msgs.Telegraph):
        def handle_message(self, msg: msgs.Telegram) -> bool:
            print(f'a: {msg}')
            return True

    class B(msgs.Telegraph):
        def handle_message(self, msg: msgs.Telegram) -> bool:
            print(f'b: {msg}')
            return True

    class C(msgs.TelegramProvider):
        def provide_message(self, receiver: msgs.Telegraph, message_type: int) -> ta.Optional[int]:
            return 5

    a = A()
    b = B()
    c = C()

    disp.dispatch(a, b, 1)

    disp.providers.add(c, int)
    disp.listeners.add(b, int)
