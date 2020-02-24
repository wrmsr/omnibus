import typing as ta

from .. import configs


StrMap = ta.Mapping[str, ta.Any]


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


def unflatten(flattened: StrMap) -> StrMap:
    raise NotImplementedError


def test_configs():
    class DbConfig(configs.Config):
        url: str
