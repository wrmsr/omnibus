"""
TODO:
 - orjson
 - dumb coercers
  - verdict: presto-guice-jackson-style Encoders/Decoders + injectable registries w global dumb default

https://serde.rs/data-model.html
https://serde.rs/examples.html

https://github.com/FasterXML/jackson-databind/wiki/Deserialization-Features
https://github.com/FasterXML/jackson-databind/wiki/Serialization-features
https://github.com/FasterXML/jackson-databind/wiki/Databind-annotations
https://github.com/FasterXML/jackson-databind/wiki/Mapper-Features
"""
import typing as ta

from . import codecs
from . import defs
from . import lang

# try:
#     import orjson as json_
# except ImportError:
try:
    import ujson as json_
except ImportError:
    import json as json_


lang.warn_unstable()


F = ta.TypeVar('F')


dumps = json_.dumps
loads = json_.loads


@codecs.EXTENSION_REGISTRY.registering('json')
@codecs.MIME_TYPE_REGISTRY.registering('application/json')
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
