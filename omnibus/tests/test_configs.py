import typing as ta

from .. import check
from .. import configs
from .. import lang


K = ta.TypeVar('K')
V = ta.TypeVar('V')
StrMap = ta.Mapping[str, ta.Any]


class NOT_SET(lang.Marker):
    pass


def flatten(unflattened: StrMap) -> StrMap:
    def rec(prefix: ta.List[str], value: ta.Any) -> None:
        if isinstance(value, dict):
            for k, v in value.items():
                rec(prefix + [k], v)
        elif isinstance(value, list):
            for i, v in enumerate(value):
                rec(prefix + [f'({i})'], v)
        else:
            k = '.'.join(prefix)
            if k in ret:
                raise KeyError(k)
            ret[k] = value

    ret = {}
    rec([], unflattened)
    return ret


class UnflattenNode(lang.Abstract, ta.Generic[K]):

    @lang.abstract
    def get(self) -> ta.Any:
        raise NotImplementedError

    @lang.abstract
    def put(self, key: K, value: ta.Any) -> None:
        raise NotImplementedError

    """
        default <V> V setDefault(K key, Supplier<V> supplier)
        {
            V ret = (V) get(key);
            if (ret == null) {
                ret = supplier.get();
                put(key, ret);
            }
            return ret;
        }

        Object build();

        static Object build(Object value)
        {
            checkNotNull(value);
            return value instanceof UnflattenNode ? ((UnflattenNode) value).build() : value;
        }
    """

    def setdefault(self, key: K, supplier: ta.Callable[[], V]) -> V:
        ret = self.get()


def unflatten(flattened: StrMap) -> StrMap:
    for k, f in flattened.items():
        pass


class DbConfig(configs.Config):
    url: str


def test_configs():
    pass
