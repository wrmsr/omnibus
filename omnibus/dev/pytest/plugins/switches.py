import pytest

from .... import check
from ._registry import register_plugin


SWITCHES = [
    'docker',
    'online',
    'slow',
    'spark',
]


def is_disabled(request, name: str) -> bool:
    check.isinstance(name, str)
    check.in_(name, SWITCHES)
    return request is not None and request.config.getoption(f'--no-{name}')


def skip_if_disabled(request, name: str) -> None:
    if is_disabled(request, name):
        pytest.skip(f'{name} disabled')


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
