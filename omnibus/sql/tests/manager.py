import sqlalchemy as sa

from ... import lang
from ... import lifecycles as lc
from ... import properties
from ...docker.dev.pytest.manager import DockerManager
from ...inject.dev.pytest import harness as har


@har.bind(har.Function)
class DbManager(lc.ContextManageableLifecycle):

    def __init__(self, dm: DockerManager) -> None:
        super().__init__()

        self._dm = dm

    @properties.stateful_cached  # type: ignore
    @property
    def pg_url(self) -> str:
        [(host, port)] = self._dm.get_container_tcp_endpoints([('postgres-master', 5432)]).values()
        env = self._dm.compose_config['postgres-master']['environment']
        url = f"postgresql+psycopg2://{env['POSTGRES_USER']}:{env['POSTGRES_PASSWORD']}@{host}:{port}"
        return url

    @properties.stateful_cached  # type: ignore
    @property
    def pg_engine(self) -> sa.engine.Engine:
        return self._lifecycle_exit_stack.enter_context(lang.disposing(sa.engine.create_engine(self.pg_url)))

    @properties.stateful_cached  # type: ignore
    @property
    def mysql_url(self) -> str:
        [(host, port)] = self._dm.get_container_tcp_endpoints([('mysql-master', 3306)]).values()
        env = self._dm.compose_config['mysql-master']['environment']
        url = f"mysql+mysqlconnector://{env['MYSQL_USER']}:{env['MYSQL_PASSWORD']}@{host}:{port}"
        return url

    @properties.stateful_cached  # type: ignore
    @property
    def mysql_engine(self) -> sa.engine.Engine:
        return self._lifecycle_exit_stack.enter_context(lang.disposing(sa.engine.create_engine(self.mysql_url)))
