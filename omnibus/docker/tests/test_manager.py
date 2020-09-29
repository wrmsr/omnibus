from ...inject.dev.pytest import harness as har
from ..dev.pytest import DockerManager


def test_manager(harness: har.Harness):
    man = harness[DockerManager]
    cli = man.client
    assert cli is not None
