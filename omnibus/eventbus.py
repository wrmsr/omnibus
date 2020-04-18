"""
TODO:
 - just all-in on inj registrars and types?

https://github.com/bennidi/mbassador
--
https://guava.dev/releases/19.0/api/docs/com/google/common/eventbus/EventBus.html
https://github.com/greenrobot/EventBus
https://github.com/jek/blinker

@Handler
@Listener
@Enveloped
@Filter
"""
from . import lang


lang.warn_unstable()


class EventBus:

    def subscribe(self) -> None:
        raise NotImplementedError

    def post(self, event) -> None:
        raise NotImplementedError
