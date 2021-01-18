"""
TODO:
 - *both* orjson (default) and ujson
"""
import dataclasses as dc
import functools
import typing as ta

from .... import codecs
from .... import defs


F = ta.TypeVar('F')
T = ta.TypeVar('T')
StrMap = ta.Mapping[str, ta.Any]


PRETTY_INDENT = 2
COMPACT_SEPARATORS = (',', ':')


@dc.dataclass(frozen=True)
class _Provider:
    pretty_kwargs: ta.Mapping[str, ta.Any] = dc.field(default_factory=dict)
    compact_kwargs: ta.Mapping[str, ta.Any] = dc.field(default_factory=dict)


class Provider:

    def __init__(self, json: ta.Any) -> None:
        super().__init__()
        self._json = json

    @property
    def json(self) -> ta.Any:
        return self._json

    @property
    def pretty_kwargs(self) -> StrMap:
        return {}

    @property
    def compact_kwargs(self) -> StrMap:
        return {}


class OrjsonProvider(Provider):

    def __init__(self) -> None:
        import orjson
        super().__init__(orjson)

    @property
    def pretty_kwargs(self) -> StrMap:
        return {
            'option': self.json.OPT_INDENT_2,
        }


class UjsonProvider(Provider):

    def __init__(self) -> None:
        import ujson
        super().__init__(ujson)

    @property
    def pretty_kwargs(self) -> StrMap:
        return {
            'indent': PRETTY_INDENT,
        }


class BuiltinProvider(Provider):

    def __init__(self) -> None:
        import json
        super().__init__(json)

    @property
    def pretty_kwargs(self) -> StrMap:
        return {
            'indent': PRETTY_INDENT,
        }

    @property
    def compact_kwargs(self) -> StrMap:
        return {
            'indent': 0,
            'separators': COMPACT_SEPARATORS,
        }


def _select_provider(typs: ta.Iterable[ta.Callable[[], Provider]]) -> Provider:
    for typ in typs:
        try:
            return typ()
        except ImportError:
            pass
    raise TypeError('No suitable json providers')


_PROVIDER: Provider = _select_provider([
    OrjsonProvider,
    UjsonProvider,
    BuiltinProvider,
])


json_ = _PROVIDER.json


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


dumps_compact = functools.partial(dumps, **_PROVIDER.compact_kwargs)


class CompactCodec(JsonCodec[F]):

    def __init__(
            self,
            *,
            dumps_kwargs: ta.Mapping[str, ta.Any] = None,
            loads_kwargs: ta.Mapping[str, ta.Any] = None,
    ) -> None:
        super().__init__(
            dumps_kwargs={**_PROVIDER.compact_kwargs, **(dumps_kwargs or {})},
            loads_kwargs=loads_kwargs,
        )


compact_codec = CompactCodec


dumps_pretty = functools.partial(dumps, **_PROVIDER.pretty_kwargs)


class PrettyCodec(JsonCodec[F]):

    def __init__(
            self,
            *,
            dumps_kwargs: ta.Mapping[str, ta.Any] = None,
            loads_kwargs: ta.Mapping[str, ta.Any] = None,
    ) -> None:
        super().__init__(
            dumps_kwargs={**_PROVIDER.pretty_kwargs, **(dumps_kwargs or {})},
            loads_kwargs=loads_kwargs,
        )


pretty_codec = PrettyCodec
