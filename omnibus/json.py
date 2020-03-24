"""
TODO:
 - orjson
 - dumb coercers
  - verdict: presto-guice-jackson-style Encoders/Decoders + injectable registries w global dumb default
 - combo Ser+De - codecify?
  - json/__init__.py, base.py(?), serdes.py..

https://github.com/ijl/orjson

https://serde.rs/data-model.html
https://serde.rs/examples.html

https://github.com/FasterXML/jackson-databind/wiki/Deserialization-Features
https://github.com/FasterXML/jackson-databind/wiki/Serialization-features
https://github.com/FasterXML/jackson-databind/wiki/Databind-annotations
https://github.com/FasterXML/jackson-databind/wiki/Mapper-Features
"""
import collections.abc
import datetime
import typing as ta

from . import codecs
from . import defs
from . import dispatch
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
T = ta.TypeVar('T')


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


Serializer = ta.Callable[[F], T]
Deserializer = ta.Callable[[T], F]
Serialization = ta.Callable[[], Serializer[F, T]]
Deserialization = ta.Callable[[], Deserializer[T, F]]
SERIALIZATION_DISPATCHER: dispatch.Dispatcher[Serialization] = dispatch.CachingDispatcher(dispatch.ErasingDispatcher())
DESERIALIZATION_DISPATCHER: dispatch.Dispatcher[Deserialization] = dispatch.CachingDispatcher(dispatch.ErasingDispatcher())  # noqa


def build_serializer(cls) -> Serializer:
    impl, manifest = SERIALIZATION_DISPATCHER[cls]
    return dispatch.inject_manifest(impl, manifest)()


def build_deserializer(cls) -> Deserializer:
    impl, manifest = DESERIALIZATION_DISPATCHER[cls]
    return dispatch.inject_manifest(impl, manifest)()


@SERIALIZATION_DISPATCHER.registering(object)
def default_serialization():
    return lambda value: value


@DESERIALIZATION_DISPATCHER.registering(object)
def default_deserialization():
    return lambda value: value


DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%H:%M:%S.%f'
DATETIME_FORMAT_SEPARATOR = 'T'
DATETIME_FORMAT = DATETIME_FORMAT_SEPARATOR.join([
    DATE_FORMAT,
    TIME_FORMAT,
])


@SERIALIZATION_DISPATCHER.registering(datetime.date)
def date_serialization():
    return lambda value: value.strftime(DATE_FORMAT)


@DESERIALIZATION_DISPATCHER.registering(datetime.date)
def date_deserialization():
    return lambda value: datetime.datetime.strptime(value, DATE_FORMAT).date()


@SERIALIZATION_DISPATCHER.registering(datetime.time)
def time_serialization():
    return lambda value: value.strftime(TIME_FORMAT)


@DESERIALIZATION_DISPATCHER.registering(datetime.time)
def time_deserialization():
    return lambda value: datetime.datetime.strptime(value, TIME_FORMAT).time()


@SERIALIZATION_DISPATCHER.registering(datetime.datetime)
def datetime_serialization():
    return lambda value: value.strftime(DATETIME_FORMAT)


@DESERIALIZATION_DISPATCHER.registering(datetime.datetime)
def datetime_deserialization():
    return lambda value: datetime.datetime.strptime(value, DATETIME_FORMAT)


@SERIALIZATION_DISPATCHER.registering(collections.abc.Set)
def set_serialization(*, manifest: dispatch.Manifest):
    [t] = manifest.spec.args
    tj = build_serializer(t)
    return lambda st: {tj(t) for t in st}


@DESERIALIZATION_DISPATCHER.registering(collections.abc.Set)
def set_deserialization(*, manifest: dispatch.Manifest):
    [t] = manifest.spec.args
    tj = build_deserializer(t)
    return lambda st: {tj(t) for t in st}


@SERIALIZATION_DISPATCHER.registering(collections.abc.Mapping)
def mapping_serialization(*, manifest: dispatch.Manifest):
    k, v = manifest.spec.args
    kj = build_serializer(k)
    vj = build_serializer(v)
    return lambda dct: {kj(k): vj(v) for k, v in dct.items()}


@DESERIALIZATION_DISPATCHER.registering(collections.abc.Mapping)
def mapping_deserialization(*, manifest: dispatch.Manifest):
    k, v = manifest.spec.args
    kj = build_deserializer(k)
    vj = build_deserializer(v)
    return lambda dct: {kj(k): vj(v) for k, v in dct.items()}
