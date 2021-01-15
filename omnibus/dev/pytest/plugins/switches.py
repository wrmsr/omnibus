import typing as ta

import pytest

from .... import check
from .... import collections as col
from ._registry import register_plugin
from _pytest.config import Config  # noqa
from _pytest.fixtures import FixtureRequest  # noqa


Configable = ta.Union[FixtureRequest, Config]


SWITCHES = col.OrderedSet([
    'docker',
    'ext',
    'online',
    'slow',
    'spark',
])


def _get_obj_config(obj: Configable) -> Config:
    if isinstance(obj, Config):
        return obj
    elif isinstance(obj, FixtureRequest):
        return obj.config
    else:
        raise TypeError(obj)


def is_disabled(obj: ta.Optional[Configable], name: str) -> bool:
    check.isinstance(name, str)
    check.in_(name, SWITCHES)
    return obj is not None and _get_obj_config(obj).getoption(f'--no-{name}')


def skip_if_disabled(obj: ta.Optional[Configable], name: str) -> None:
    if is_disabled(obj, name):
        pytest.skip(f'{name} disabled')


def get_switches(obj: Configable) -> ta.Mapping[str, bool]:
    return {
        sw: _get_obj_config(obj).getoption(f'--no-{sw}')
        for sw in SWITCHES
    }


@register_plugin
class SwitchesPlugin:

    def pytest_addoption(self, parser):
        for sw in SWITCHES:
            parser.addoption(f'--no-{sw}', action='store_true', default=False, help=f'disable {sw} tests')

    def pytest_collection_modifyitems(self, config, items):
        for sw in SWITCHES:
            if not config.getoption(f'--no-{sw}'):
                continue
            skip = pytest.mark.skip(reason=f'omit --no-{sw} to run')
            for item in items:
                if sw in item.keywords:
                    item.add_marker(skip)

    def pytest_configure(self, config):
        for sw in SWITCHES:
            config.addinivalue_line('markers', f'{sw}: mark test as {sw}')
