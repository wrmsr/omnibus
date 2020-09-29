import os.path

with open(os.path.join(os.path.dirname(__file__), '../setup.py'), 'r') as f:
    _setup_header = f.readline()
if _setup_header.strip() != '#@omnibus':
    raise EnvironmentError('Should not be present')


from omnibus.lang.imports import ignore_unstable_warn

ignore_unstable_warn()


from .dev.pytest import plugins  # noqa
from .inject.dev import pytest as _  # noqa


def pytest_addhooks(pluginmanager):
    for plugin in plugins.ALL:
        pluginmanager.register(plugin())


def pytest_configure(config):
    config.addinivalue_line('filterwarnings', 'ignore:omnibus module is marked as unstable::omnibus.*:')
