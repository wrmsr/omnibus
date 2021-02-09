"""
TODO:
 - load (file-like)
"""
import dataclasses as dc
import functools
import typing as ta

from .... import codecs
from .... import defs
from .... import properties


F = ta.TypeVar('F')
T = ta.TypeVar('T')
StrMap = ta.Mapping[str, ta.Any]


ENCODING = 'utf-8'
PRETTY_INDENT = 2
COMPACT_SEPARATORS = (',', ':')


Dumps = ta.Callable[[ta.Any], str]
Dumpb = ta.Callable[[ta.Any], bytes]
Loads = ta.Callable[[ta.Union[str, bytes, bytearray]], ta.Any]


@dc.dataclass(frozen=True)
class _Provider:
    pretty_kwargs: StrMap = dc.field(default_factory=dict)
    compact_kwargs: StrMap = dc.field(default_factory=dict)


class Provider:

    def __init__(self, json: ta.Any) -> None:
        super().__init__()
        self._json = json

    @property
    def json(self) -> ta.Any:
        return self._json

    @properties.cached
    def dumps(self) -> Dumps:
        return self.json.dumps

    @properties.cached
    def dumpb(self) -> Dumpb:
        def dumpb(*args, **kwargs):
            return fn(*args, **kwargs).encode(ENCODING)
        fn = self.json.dumps
        return functools.wraps(fn)(dumpb)

    @properties.cached
    def loads(self) -> Loads:
        return self.json.loads

    @properties.cached
    def pretty_kwargs(self) -> StrMap:
        return {}

    @properties.cached
    def compact_kwargs(self) -> StrMap:
        return {}


class OrjsonProvider(Provider):

    def __init__(self) -> None:
        import orjson
        super().__init__(orjson)

    @properties.cached
    def pretty_kwargs(self) -> StrMap:
        return {
            'option': self.json.OPT_INDENT_2,
        }

    @properties.cached
    def dumps(self) -> Dumps:
        def dumps(*args, **kwargs):
            return fn(*args, **kwargs).decode(ENCODING)
        fn = self.json.dumps
        return functools.wraps(fn)(dumps)

    @properties.cached
    def dumpb(self) -> Dumpb:
        return self.json.dumps


class UjsonProvider(Provider):

    def __init__(self) -> None:
        import ujson
        super().__init__(ujson)

    @properties.cached
    def pretty_kwargs(self) -> StrMap:
        return {
            'indent': PRETTY_INDENT,
        }

    @properties.cached
    def loads(self) -> Loads:
        def loads(arg, *args, **kwargs):
            if isinstance(arg, (bytes, bytearray)):
                arg = arg.decode(ENCODING)
            return fn(arg, *args, **kwargs)
        fn = self.json.loads
        return functools.wraps(fn)(loads)


class BuiltinProvider(Provider):

    def __init__(self) -> None:
        import json
        super().__init__(json)

    @properties.cached
    def pretty_kwargs(self) -> StrMap:
        return {
            'indent': PRETTY_INDENT,
        }

    @properties.cached
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


PROVIDER: Provider = _select_provider([
    OrjsonProvider,
    UjsonProvider,
    BuiltinProvider,
])


dumps: Dumps = PROVIDER.dumps
dumpb: Dumpb = PROVIDER.dumpb
loads: Loads = PROVIDER.loads

dumps_compact: Dumps = functools.partial(dumps, **PROVIDER.compact_kwargs)
dumpb_compact: Dumpb = functools.partial(dumpb, **PROVIDER.compact_kwargs)

dumps_pretty: Dumps = functools.partial(dumps, **PROVIDER.pretty_kwargs)
dumpb_pretty: Dumpb = functools.partial(dumpb, **PROVIDER.pretty_kwargs)


class AbstractCodec(codecs.Codec[F, T]):

    def __init__(
            self,
            *,
            dump_kwargs: ta.Optional[StrMap] = None,
            load_kwargs: ta.Optional[StrMap] = None,
    ) -> None:
        super().__init__()

        self._dump_kwargs = dump_kwargs or {}
        self._load_kwargs = load_kwargs or {}

    defs.repr()


@codecs.EXTENSION_REGISTRY.registering('json')
@codecs.MIME_TYPE_REGISTRY.registering('application/json')
class JsonCodec(AbstractCodec[F, str]):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.encode = functools.partial(dumps, **self._dump_kwargs)  # type: ignore
        self.decode = functools.partial(loads, **self._load_kwargs)  # type: ignore

    def encode(self, o: F) -> str:
        return dumps(o, **self._dump_kwargs)  # noqa

    def decode(self, o: str) -> F:
        return loads(o, **self._load_kwargs)


codec = JsonCodec


class CompactCodec(JsonCodec[F]):

    def __init__(
            self,
            *,
            dump_kwargs: ta.Optional[StrMap] = None,
    ) -> None:
        super().__init__(
            dump_kwargs={**PROVIDER.compact_kwargs, **(dump_kwargs or {})},
        )


compact_codec = CompactCodec


class PrettyCodec(JsonCodec[F]):

    def __init__(
            self,
            *,
            dump_kwargs: ta.Optional[StrMap] = None,
    ) -> None:
        super().__init__(
            dump_kwargs={**PROVIDER.pretty_kwargs, **(dump_kwargs or {})},
        )


pretty_codec = PrettyCodec


class JsonBytesCodec(AbstractCodec[F, bytes]):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.encode = functools.partial(dumpb, **self._dump_kwargs)  # type: ignore
        self.decode = functools.partial(loads, **self._load_kwargs)  # type: ignore

    def encode(self, o: F) -> bytes:
        return dumpb(o, **self._dump_kwargs)  # noqa

    def decode(self, o: bytes) -> F:
        return loads(o, **self._load_kwargs)


bytes_codec = JsonBytesCodec


class CompactBytesCodec(JsonBytesCodec[F]):

    def __init__(
            self,
            *,
            dump_kwargs: ta.Optional[StrMap] = None,
    ) -> None:
        super().__init__(
            dump_kwargs={**PROVIDER.compact_kwargs, **(dump_kwargs or {})},
        )


compact_bytes_codec = CompactBytesCodec


class PrettyBytesCodec(JsonBytesCodec[F]):

    def __init__(
            self,
            *,
            dump_kwargs: ta.Optional[StrMap] = None,
    ) -> None:
        super().__init__(
            dump_kwargs={**PROVIDER.pretty_kwargs, **(dump_kwargs or {})},
        )


pretty_bytes_codec = PrettyBytesCodec
