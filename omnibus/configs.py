import abc
import typing as ta

from . import c3
from . import check
from . import lang


lang.warn_unstable()


T = ta.TypeVar('T')
K = ta.TypeVar('K')
V = ta.TypeVar('V')
StrMap = ta.Mapping[str, ta.Any]
ConfigT = ta.TypeVar('ConfigT', bound='Config')


IGNORED_NAMESPACE_KEYS: ta.Set[str] = {
    '_abc_impl',
}


class NOT_SET(lang.Marker):
    pass


class FieldMetadata(lang.Final, ta.Generic[T]):

    def __init__(
            self,
            name: str,
            type: type = None,
            *,
            default: ta.Any = NOT_SET,
            doc: str = None,
    ) -> None:
        super().__init__()

        self._name = check.not_empty(check.isinstance(name, str))
        self._type = type
        self._default = default
        self._doc = doc

    @property
    def name(self) -> str:
        return self._name

    @property
    def type(self) -> type:
        return self._type

    @property
    def default(self) -> ta.Any:
        return self._default

    @property
    def doc(self) -> ta.Optional[str]:
        return self._doc


class ConfigMetadata(lang.Final):

    def __init__(
            self,
            fields: ta.Iterable[FieldMetadata],
    ) -> None:
        super().__init__()

        self._fields = list(fields)
        check.unique(f.name for f in self._fields)
        self._fields_by_name = {f.name: f for f in self._fields}

    @property
    def fields(self) -> ta.Iterable[FieldMetadata]:
        return self._fields

    @property
    def fields_by_name(self) -> ta.Mapping[str, FieldMetadata]:
        return self._fields_by_name


class FieldSource(lang.Abstract):

    @abc.abstractmethod
    def get(self, name: str) -> ta.Any:
        raise NotImplementedError


class ConfigSource(lang.Abstract):

    @abc.abstractmethod
    def get(self, cls: ta.Type[ConfigT]) -> ConfigT:
        raise NotImplementedError


class DictFieldSource(FieldSource):

    def __init__(self, dct: ta.Mapping[str, ta.Any]) -> None:
        super().__init__()

        self._dct = check.not_none(dct)

    def get(self, name: str) -> ta.Any:
        return self._dct.get(name, NOT_SET)


class _FieldDescriptor:

    def __get__(self, instance, owner):
        raise NotImplementedError


class FieldArgs(lang.Final):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()

        self._args = args
        self._kwargs = kwargs


def field(*args, **kwargs):
    return FieldArgs(*args, **kwargs)


class _ConfigMeta(abc.ABCMeta):

    class FieldInfo(ta.NamedTuple):
        name: str
        annotation: ta.Any
        value: ta.Any

    def build_field_info(mcls, ns, name) -> FieldInfo:
        annotation = ns.get('__annotations__', {}).get(name)
        value = ns.get(name, NOT_SET)
        return _ConfigMeta.FieldInfo(name, annotation, value)

    def build_field_metadata(mcls, fi: FieldInfo) -> FieldMetadata:
        type_ = None
        default = NOT_SET
        kwargs = {}

        return FieldMetadata(
            fi.name,
            type_,
            default=default,
            **kwargs
        )

    def __new__(mcls, name, bases, namespace):
        base_mro = c3.merge([list(b.__mro__) for b in bases])
        field_infos = {
            fi.name: fi
            for ns in [b.__dict__ for b in reversed(base_mro)] + [namespace]
            for name in {*ns, *ns.get('__annotations__', [])}
            if not lang.is_dunder(name) and name not in IGNORED_NAMESPACE_KEYS
            for fi in [mcls.build_field_info(mcls, ns, name)]
        }

        return super().__new__(mcls, name, bases, namespace)


class Config(metaclass=_ConfigMeta):

    def __init__(self, field_source: FieldSource) -> None:
        super().__init__()

        self._field_source = check.isinstance(field_source, FieldSource)


class Flattening:

    DEFAULT_DELIMITER = '.'
    DEFAULT_INDEX_OPEN = '('
    DEFAULT_INDEX_CLOSE = ')'

    def __init__(
            self,
            *,
            delimiter=DEFAULT_DELIMITER,
            index_open=DEFAULT_INDEX_OPEN,
            index_close=DEFAULT_INDEX_CLOSE,
    ) -> None:
        super().__init__()

        self._delimiter = check.not_empty(delimiter)
        self._index_open = check.not_empty(index_open)
        self._index_close = check.not_empty(index_close)

    def flatten(self, unflattened: StrMap) -> StrMap:
        def rec(prefix: ta.List[str], value: ta.Any) -> None:
            if isinstance(value, dict):
                for k, v in value.items():
                    rec(prefix + [k], v)
            elif isinstance(value, list):
                check.not_empty(prefix)
                for i, v in enumerate(value):
                    rec(prefix[:-1] + [f'{prefix[-1]}{self._index_open}{i}{self._index_close}'], v)
            else:
                k = self._delimiter.join(prefix)
                if k in ret:
                    raise KeyError(k)
                ret[k] = value

        ret = {}
        rec([], unflattened)
        return ret

    class UnflattenNode(lang.Abstract, ta.Generic[K]):

        @lang.abstract
        def get(self, key: K) -> ta.Any:
            raise NotImplementedError

        @lang.abstract
        def put(self, key: K, value: ta.Any) -> None:
            raise NotImplementedError

        def setdefault(self, key: K, supplier: ta.Callable[[], V]) -> V:
            ret = self.get(key)
            if ret is NOT_SET:
                ret = supplier()
                self.put(key, ret)
            return ret

        @lang.abstract
        def build(self) -> ta.Any:
            raise NotImplementedError

        @staticmethod
        def maybe_build(value: ta.Any) -> ta.Any:
            check.not_none(value)
            return value.build() if isinstance(value, Flattening.UnflattenNode) else value

    class UnflattenDict(UnflattenNode[str]):

        def __init__(self) -> None:
            super().__init__()

            self._dict = {}

        def get(self, key: str) -> ta.Any:
            return self._dict.get(key, NOT_SET)

        def put(self, key: str, value: ta.Any) -> None:
            check.arg(key not in self._dict)
            self._dict[key] = value

        def build(self) -> ta.Any:
            return {k: Flattening.UnflattenNode.maybe_build(v) for k, v in self._dict.items()}

    class UnflattenList(UnflattenNode[int]):

        def __init__(self) -> None:
            super().__init__()

            self._list = []

        def get(self, key: int) -> ta.Any:
            check.arg(key >= 0)
            return self._list[key] if key < len(self._list) else NOT_SET

        def put(self, key: int, value: ta.Any) -> None:
            check.arg(key >= 0)
            if key >= len(self._list):
                self._list.extend([NOT_SET] * (key - len(self._list) + 1))
            check.arg(self._list[key] is NOT_SET)
            self._list[key] = value

        def build(self) -> ta.Any:
            return [Flattening.UnflattenNode.maybe_build(e) for e in self._list]

    def unflatten(self, flattened: StrMap) -> StrMap:
        root = Flattening.UnflattenDict()

        def split_keys(fkey: str) -> ta.Iterable[ta.Union[str, int]]:
            for part in fkey.split(self._delimiter):
                if self._index_open in part:
                    check.state(part.endswith(self._index_close))
                    pos = part.index(self._index_open)
                    yield part[:pos]
                    for p in part[pos + len(self._index_open):-len(self._index_close)].split(self._index_close + self._index_open):  # noqa
                        yield int(p)
                else:
                    check.state(')' not in part)
                    yield part

        for fk, v in flattened.items():
            node = root
            fks = list(split_keys(fk))
            for key, nkey in zip(fks, fks[1:]):
                if isinstance(nkey, str):
                    node = node.setdefault(key, Flattening.UnflattenDict)
                elif isinstance(nkey, int):
                    node = node.setdefault(key, Flattening.UnflattenList)
                else:
                    raise TypeError(key)
            node.put(fks[-1], v)

        return root.build()
