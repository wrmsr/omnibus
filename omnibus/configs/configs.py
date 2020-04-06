"""
TODO:
 - *YES* - dataclass interop - bidirectional for injection
  - akin to inj not being required
  - honor frozen
  - full on merge with dataclasses? configs just a special storage backend?
 - polled sources: file (+url), sql, redis
  - atomicity - class UsernameAndPassword etc
 - pushed sources: zk
 - callbacks only on 'winning' value change
 - dc stuff - validate, coerce, etc
 - config_cls->cls registry pattern?
 - yaml forest
  - search_path (registry?), pkg:// prefix, origin tracking
  - yamls pointing at other yamls..
  - https://github.com/facebookresearch/hydra
 - pyo3 adapter (serde?)
 - newable-style object graphs, refs
 - cmdline overrides (env-var? dict?)
"""
import abc
import types
import typing as ta

from .. import c3
from .. import check
from .. import defs
from .. import lang
from .. import properties
from .fields import DictFieldSource
from .fields import EmptyFieldSource
from .fields import FieldKwargs
from .fields import FieldSource
from .fields import FieldSpec
from .types import MISSING


ConfigT = ta.TypeVar('ConfigT', bound='Config')


IGNORED_NAMESPACE_KEYS: ta.Set[str] = {
    '_abc_impl',
}


class ConfigSpec(lang.Final):

    def __init__(
            self,
            fields: ta.Iterable[FieldSpec],
    ) -> None:
        super().__init__()

        self._fields = list(fields)
        check.unique(f.name for f in self._fields)
        self._fields_by_name = {f.name: f for f in self._fields}

    cls = properties.set_once()

    @property
    def fields(self) -> ta.Iterable[FieldSpec]:
        return self._fields

    @property
    def fields_by_name(self) -> ta.Mapping[str, FieldSpec]:
        return self._fields_by_name


class ConfigSource(lang.Abstract):

    @abc.abstractmethod
    def get(self, cls: ta.Type[ConfigT]) -> ConfigT:
        raise NotImplementedError


class _FieldDescriptor:

    def __init__(self, spec: FieldSpec) -> None:
        super().__init__()

        self._spec = check.isinstance(spec, FieldSpec)

    defs.repr('name')

    @property
    def name(self) -> str:
        return self._spec.name

    def __set_name__(self, owner, name):
        check.state(name == self.name)

    def __get__(self, instance: 'Config', owner: ta.Type['Config']):
        if not isinstance(instance, Config):
            raise TypeError(instance)
        try:
            return instance._values_by_field[self._spec]
        except KeyError:
            value = instance._field_source.get(self._spec)
            if value is MISSING:
                value = self._spec.default
            if value is MISSING:
                raise KeyError(self._spec)
            instance._values_by_field[self._spec] = value
            return value


def is_field_name(name: str) -> bool:
    return not lang.is_dunder(name) and name not in IGNORED_NAMESPACE_KEYS


def is_field_value(name: str, ns: ta.Mapping[str, ta.Any]) -> bool:
    if name not in ns:
        return True
    value = ns[name]
    if isinstance(value, (types.FunctionType, staticmethod, classmethod, property)):
        return False
    return True


def get_namespace_field_names(ns: ta.Mapping[str, ta.Any]) -> ta.List[str]:
    return [
        name
        for name in {**ns.get('__annotations__', {}), **ns}.keys()
        if is_field_name(name) and is_field_value(name, ns)
    ]


class _ConfigMeta(abc.ABCMeta):

    class Field(ta.NamedTuple):
        name: str
        annotation: ta.Any
        value: ta.Any

    def build_field(mcls, ns, name) -> Field:
        annotation = ns.get('__annotations__', {}).get(name, MISSING)
        value = ns.get(name, MISSING)
        return _ConfigMeta.Field(name, annotation, value)

    def build_field_spec(mcls, fi: Field) -> FieldSpec:
        if isinstance(fi.value, _FieldDescriptor):
            return fi.value._spec

        type_ = MISSING
        default = MISSING
        kwargs = {}

        if isinstance(fi.value, FieldKwargs):
            fkx = dict(fi.value._kwargs)
            type_ = fkx.pop('type')
            if type_ is not MISSING:
                type_ = fi.annotation
            default = fkx.pop('default')
            kwargs.update(fkx)

        else:
            if fi.annotation is not MISSING:
                type_ = fi.annotation
            default = fi.value
            if default is not MISSING and type_ is MISSING:
                type_ = type(default)

        return FieldSpec(
            fi.name,
            type_,
            default=default,
            **kwargs
        )

    def __new__(mcls, name, bases, namespace):
        base_mro = c3.merge([list(b.__mro__) for b in bases])

        fields = {
            f.name: f
            for ns in [b.__dict__ for b in reversed(base_mro)] + [namespace]
            for name in reversed(get_namespace_field_names(ns))
            for f in [mcls.build_field(mcls, ns, name)]
        }

        field_specs = {
            fs.name: fs
            for f in reversed(list(fields.values()))
            for fs in [mcls.build_field_spec(mcls, f)]
        }

        config_spec = ConfigSpec(
            field_specs.values()
        )

        newns = {
            **{
                name: v
                for name, v in namespace.items()
                if not is_field_name(name) or not is_field_value(name, namespace)
            },
            **{
                name: _FieldDescriptor(field_specs[name])
                for name in get_namespace_field_names(namespace)
            },
            '__spec__': config_spec,
        }

        cls = super().__new__(mcls, name, bases, newns)
        config_spec.cls = cls
        return cls


class Config(metaclass=_ConfigMeta):

    def __init__(self, field_source: FieldSource = EmptyFieldSource()) -> None:
        super().__init__()

        self._field_source = check.isinstance(field_source, FieldSource)

        self._values_by_field: ta.Dict[FieldSpec, ta.Any] = {}

    def __new__(cls, field_source: FieldSource = EmptyFieldSource(), **kwargs):
        if cls is Config:
            raise TypeError
        return super().__new__(cls, **kwargs)

    @classmethod
    def of(cls: ta.Type[ConfigT], **kwargs) -> ConfigT:
        return cls(DictFieldSource(kwargs))
