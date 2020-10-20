"""
TODO:
 - *both* orjson (default) and ujson
"""
import functools
import typing as ta

from .... import codecs
from .... import defs

# try:
#     import orjson as json_
# except ImportError:
try:
    import ujson as json_
except ImportError:
    import json as json_


F = ta.TypeVar('F')
T = ta.TypeVar('T')


dumps = json_.dumps
loads = json_.loads


@codecs.EXTENSION_REGISTRY.registering('json')
@codecs.MIME_TYPE_REGISTRY.registering('application/json')
class JsonCodec(codecs.Codec[F, str]):

    def __init__(
            self,
            *,
            dumps_kwargs: ta.Mapping[str, ta.Any] = None,
            loads_kwargs: ta.Mapping[str, ta.Any] = None,
    ) -> None:
        super().__init__()

        self._dumps_kwargs = dumps_kwargs or {}
        self._loads_kwargs = loads_kwargs or {}

        self.encode = functools.partial(dumps, **self._dumps_kwargs)
        self.decode = functools.partial(loads, **self._loads_kwargs)

    defs.repr()

    def encode(self, o: F) -> str:
        return dumps(o, **self._dumps_kwargs)

    def decode(self, o: str) -> F:
        return loads(o, **self._loads_kwargs)


codec = JsonCodec


COMPACT_SEPARATORS = (',', ':')

dumps_compact = functools.partial(dumps, separators=COMPACT_SEPARATORS)


class CompactCodec(JsonCodec[F, str]):

    def __init__(
            self,
            *,
            dumps_kwargs: ta.Mapping[str, ta.Any] = None,
            loads_kwargs: ta.Mapping[str, ta.Any] = None,
    ) -> None:
        super().__init__(
            dumps_kwargs={'separators': COMPACT_SEPARATORS, **(dumps_kwargs or {})},
            loads_kwargs=loads_kwargs,
        )


compact_codec = CompactCodec


PRETTY_INDENT = 2

dumps_pretty = functools.partial(dumps, indent=PRETTY_INDENT)


class PrettyCodec(JsonCodec[F, str]):

    def __init__(
            self,
            *,
            dumps_kwargs: ta.Mapping[str, ta.Any] = None,
            loads_kwargs: ta.Mapping[str, ta.Any] = None,
    ) -> None:
        super().__init__(
            dumps_kwargs={'indent': PRETTY_INDENT, **(dumps_kwargs or {})},
            loads_kwargs=loads_kwargs,
        )


pretty_codec = PrettyCodec
