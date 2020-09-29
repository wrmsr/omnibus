import typing as ta

import yaml

from .... import check
from .... import docker
from .... import lifecycles as lc
from .... import properties
from ....dev.pytest.plugins import switches
from ....inject.dev.pytest import harness as har


class Prefix(ta.NamedTuple):
    value: str


class ComposePath(ta.NamedTuple):
    value: str


@har.bind(har.Session)
class DockerManager(lc.ContextManageableLifecycle):

    def __init__(
            self,
            prefix: Prefix,
            *,
            compose_path: ta.Optional[ComposePath] = None,
            request: ta.Optional[har.FixtureRequest] = None,
    ) -> None:
        super().__init__()

        self._prefix = check.isinstance(prefix, Prefix).value
        self._compose_path = check.isinstance(compose_path, ComposePath).value if compose_path is not None else None
        self._request = check.isinstance(request, (har.FixtureRequest, None))

    @property
    def prefix(self) -> str:
        return self._prefix

    @properties.stateful_cached
    def client(self):
        return self._lifecycle_exit_stack.enter_context(docker.client_context())

    _container_tcp_endpoints = properties.cached(lambda self: {})

    def get_container_tcp_endpoints(
            self,
            name_port_pairs: ta.Iterable[ta.Tuple[str, int]],
    ) -> ta.Dict[ta.Tuple[str, int], ta.Tuple[str, int]]:
        switches.skip_if_disabled(self._request, 'docker')
        if docker.is_in_docker():
            return {(h, p): (self._prefix + h, p) for h, p in name_port_pairs}
        ret = {}
        lut = {}
        for h, p in name_port_pairs:
            try:
                ret[(h, p)] = self._container_tcp_endpoints[(h, p)]
            except KeyError:
                lut[(f'docker_{self._prefix}{h}_1', p)] = (h, p)
        if lut:
            dct = docker.get_container_tcp_endpoints(self.client, lut)
            res = {lut[k]: v for k, v in dct.items()}
            ret.update(res)
            self._container_tcp_endpoints.update(res)
        return ret

    @properties.cached
    @property
    def compose_config(self) -> ta.Mapping[str, ta.Any]:
        with open(check.not_none(self._compose_path), 'r') as f:
            buf = f.read()
        dct = yaml.safe_load(buf)
        ret = {}
        for n, c in dct['services'].items():
            check.state(n.startswith(self._prefix))
            ret[n[len(self._prefix):]] = c
        return ret
