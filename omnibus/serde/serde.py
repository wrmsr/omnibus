"""
TODO:
 - ** really might wanna get typelevel+injecty with this asap..**
 - union, per dataclasses validation
 - dumb coercers
  - verdict: presto-guice-jackson-style Encoders/Decoders + injectable registries w global dumb default
 - combo Serde - codecify?
  - dedupe symmetric generic Serde sides?
 - heavy overlap w dc validation - omnibus/validate?
 - camel/snake(/kebab/pascal/dot)
 - enums

builtins:
    Decimal
    dsn.DSN
    email.Email
    ipaddress.IPv4Address
    ipaddress.IPv6Address
    path.DirectoryPath
    path.FilePath
    path.PathType
    pathlib.Path
    re.Pattern
    secret.SecretBytes
    secret.SecretStr
    timedelta
    url.AbsoluteURL
    url.HostName
    url.NetworkAddress
    url.RelativeURL
    url.URL
    uuid.UUID

typical
https://github.com/marshmallow-code/marshmallow/wiki/Ecosystem
https://github.com/lidatong/dataclasses-json
https://github.com/lyft/toasted-marshmallow/blob/master/toastedmarshmallow/jit.py

https://github.com/ijl/orjson

https://serde.rs/data-model.html
https://serde.rs/examples.html

https://github.com/FasterXML/jackson-databind/wiki/Deserialization-Features
https://github.com/FasterXML/jackson-databind/wiki/Serialization-features
https://github.com/FasterXML/jackson-databind/wiki/Databind-annotations
https://github.com/FasterXML/jackson-databind/wiki/Mapper-Features

subtype reg:
@JsonTypeInfo(use = JsonTypeInfo.Id.NAME, include = JsonTypeInfo.As.PROPERTY, property = "@type")
@JsonSubTypes({@JsonSubTypes.Type(value = OutputNode.class, name = "output"), ...
"""
import collections.abc
import datetime
import typing as ta

from .. import check
from .. import dispatch
from .. import lang
from .. import reflect


lang.warn_unstable()


F = ta.TypeVar('F')
T = ta.TypeVar('T')

K = ta.TypeVar('K')
V = ta.TypeVar('V')


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


class Serde(ta.Generic[F, T], lang.Abstract):

    def __init__(self, *, manifest: dispatch.Manifest) -> None:
        super().__init__()

        self._manifest = check.isinstance(manifest, dispatch.Manifest) if manifest is not None else None

    @property
    def manifest(self) -> ta.Optional[dispatch.Manifest]:
        return self._manifest

    def serialization(self) -> Serializer[F, T]:
        return self.serialize

    def deserialization(self) -> Deserializer[T, F]:
        return self.deserialize

    def serialize(self, value: F) -> T:
        raise TypeError

    def deserialize(self, value: T) -> F:
        raise TypeError


def registering_serde(*keys):
    def inner(cls):
        check.issubclass(cls, Serde)

        @SERIALIZATION_DISPATCHER.registering(*keys)
        def serialization(*, manifest: dispatch.Manifest):
            return cls(manifest=manifest).serialization()

        @DESERIALIZATION_DISPATCHER.registering(*keys)
        def deserialization(*, manifest: dispatch.Manifest):
            return cls(manifest=manifest).deserialization()

        return cls

    return inner


DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%H:%M:%S.%f'
DATETIME_FORMAT_SEPARATOR = 'T'
DATETIME_FORMAT = DATETIME_FORMAT_SEPARATOR.join([
    DATE_FORMAT,
    TIME_FORMAT,
])


@registering_serde(datetime.date)
class DateSerde(Serde[datetime.date, str]):

    def serialize(self, value: datetime.date) -> str:
        return value.strftime(DATE_FORMAT)

    def deserialize(self, value: str) -> datetime.date:
        return datetime.datetime.strptime(value, DATE_FORMAT).date()


@registering_serde(datetime.time)
class TimeSerde(Serde[datetime.time, str]):

    def serialize(self, value: datetime.time) -> str:
        return value.strftime(TIME_FORMAT)

    def deserialize(self, value: str) -> datetime.time:
        return datetime.datetime.strptime(value, TIME_FORMAT).time()


@registering_serde(datetime.datetime)
class DatetimeSerde(Serde[datetime.datetime, str]):

    def serialize(self, value: datetime.datetime) -> str:
        return value.strftime(DATETIME_FORMAT)

    def deserialize(self, value: str) -> datetime.datetime:
        return datetime.datetime.strptime(value, DATETIME_FORMAT)


@registering_serde(collections.abc.Mapping)
class MappingSerde(Serde[ta.Mapping[K, V], ta.Mapping]):

    def serialization(self) -> Serializer[ta.Mapping[K, V], ta.Mapping]:
        if isinstance(self.manifest.spec, reflect.NonGenericTypeSpec):
            return lambda value: value

        elif isinstance(self.manifest.spec, reflect.ParameterizedGenericTypeSpec):
            kj, vj = map(build_serializer, self.manifest.spec.args)
            return lambda value: {kj(k): vj(v) for k, v in value.items()}

        else:
            raise TypeError(self.manifest.spec)

    def deserialization(self) -> Deserializer[ta.Mapping, ta.Mapping[K, V]]:
        if isinstance(self.manifest.spec, reflect.NonGenericTypeSpec):
            return lambda value: value

        elif isinstance(self.manifest.spec, reflect.ParameterizedGenericTypeSpec):
            kj, vj = map(build_deserializer, self.manifest.spec.args)
            return lambda value: {kj(k): vj(v) for k, v in value.items()}

        else:
            raise TypeError(self.manifest.spec)


@registering_serde(collections.abc.Set)
class SetSerde(Serde[ta.AbstractSet[V], ta.Sequence]):

    def serialization(self) -> Serializer[ta.AbstractSet[V], ta.Sequence]:
        if isinstance(self.manifest.spec, reflect.NonGenericTypeSpec):
            return lambda value: value

        elif isinstance(self.manifest.spec, reflect.ParameterizedGenericTypeSpec):
            [vj] = map(build_serializer, self.manifest.spec.args)
            return lambda value: [vj(v) for v in value]

        else:
            raise TypeError(self.manifest.spec)

    def deserialization(self) -> Deserializer[ta.Sequence, ta.AbstractSet[V]]:
        if isinstance(self.manifest.spec, reflect.NonGenericTypeSpec):
            return lambda value: value

        elif isinstance(self.manifest.spec, reflect.ParameterizedGenericTypeSpec):
            [vj] = map(build_deserializer, self.manifest.spec.args)
            return lambda value: {vj(v) for v in value}

        else:
            raise TypeError(self.manifest.spec)


@registering_serde(lang.Redacted)
class RedactedSerde(Serde[lang.Redacted[V], V]):

    def serialization(self) -> Serializer[lang.Redacted[V], V]:
        if isinstance(self.manifest.spec, reflect.NonGenericTypeSpec):
            return lambda value: value

        elif isinstance(self.manifest.spec, reflect.ParameterizedGenericTypeSpec):
            [vj] = map(build_serializer, self.manifest.spec.args)
            return lambda value: vj(value.value)

        else:
            raise TypeError(self.manifest.spec)

    def deserialization(self) -> Deserializer[V, lang.Redacted[V]]:
        if isinstance(self.manifest.spec, reflect.NonGenericTypeSpec):
            return lambda value: value

        elif isinstance(self.manifest.spec, reflect.ParameterizedGenericTypeSpec):
            [vj] = map(build_deserializer, self.manifest.spec.args)
            return lambda value: lang.redact(vj(value))

        else:
            raise TypeError(self.manifest.spec)
