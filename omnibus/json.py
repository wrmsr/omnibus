import typing as ta

try:
    import ujson as json_
except ImportError:
    import json as json_

from . import codecs
from . import defs
from . import lang


F = ta.TypeVar('F')


dumps = json_.dumps
loads = json_.loads


@codecs.register_extension('json')
@codecs.register_mime_type('application/json')
class JsonCodec(codecs.Codec[F, str], lang.Final):

    def __init__(
            self,
            *,
            dumps_kwargs: ta.Mapping[str, ta.Any] = None,
            loads_kwargs: ta.Mapping[str, ta.Any] = None,
    ) -> None:
        super().__init__()

        self._dumps_kwargs = dumps_kwargs or {}
        self._loads_kwargs = loads_kwargs or {}

    defs.repr()

    def encode(self, o: F) -> str:
        return dumps(o, **self._dumps_kwargs)

    def decode(self, o: str) -> F:
        return loads(o, **self._loads_kwargs)


codec = JsonCodec
