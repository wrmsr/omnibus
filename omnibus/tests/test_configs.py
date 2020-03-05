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
        return value.build() if isinstance(value, UnflattenNode) else value


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
        return {k: UnflattenNode.maybe_build(v) for k, v in self._dict.items()}


class UnflattenList(UnflattenNode[int]):

    def __init__(self) -> None:
        super().__init__()

        self._list = []

    def get(self, key: int) -> ta.Any:
        check.arg(key >= 0)
        return self._list[key] if key <= len(self._list) else NOT_SET

    def put(self, key: int, value: ta.Any) -> None:
        check.arg(key >= 0)
        if key >= len(self._list):
            self._list.extend([NOT_SET] * (key - len(self._list) + 1))
        check.arg(self._list[key] is NOT_SET)
        self._list[key] = value

    def build(self) -> ta.Any:
        return [UnflattenNode.maybe_build(e) for e in self._list]


def unflatten(flattened: StrMap) -> StrMap:
    root = UnflattenDict()
    for k, f in flattened.items():
        node = root


def test_flattening():
    m = {
        'a': 1,
        'b': {
            'c': 2
        },
        'd': [
            'e',
            {
                'f': 3
            }
        ],
        'g': [
            [
                'a',
                'b'
            ],
            [
                'c',
                'd'
            ]
        ]
    }
    fl = flatten(m)
    unflatten(fl)


class DbConfig(configs.Config):
    url: str


def test_configs():
    pass
