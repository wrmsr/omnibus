import contextlib
import os.path
import tempfile
import threading
import time
import typing as ta

import requests

from ... import check
from ... import collections as ocol
from ... import http
from ... import inject
from ... import lifecycles
from ... import replserver


def bind_contextmanager_lifecycle(binder: inject.Binder, target: ta.Union[inject.Key, ta.Type]) -> None:
    binder.bind_callable(
        lifecycles.ContextManagerLifecycle,
        key=inject.Key(lifecycles.ContextManagerLifecycle, target),
        kwargs={'obj': target},
        as_eager_singleton=True)


class LifecycleRegistrar:

    def __init__(self) -> None:
        super().__init__()
        self._seen = ocol.IdentitySet()

    def __call__(self, injector: inject.Injector, key, instance) -> None:
        if (
                isinstance(instance, lifecycles.Lifecycle) and
                not isinstance(instance, lifecycles.LifecycleManager) and
                instance not in self._seen
        ):
            man = injector.get_instance(lifecycles.LifecycleManager)
            man.add(instance)
            self._seen.add(instance)


class ReplServerThread(lifecycles.ContextManageableLifecycle):

    def __init__(self, server: replserver.ReplServer) -> None:
        super().__init__()

        self._server = server
        self._thread = threading.Thread(target=server.run)

    def _do_lifecycle_start(self) -> None:
        self._thread.start()

    def _do_lifecycle_stop(self) -> None:
        self._server.shutdown()
        self._thread.join(5)
        check.state(not self._thread.is_alive())


def provide_binder(config: http.bind.Binder.Config) -> http.bind.Binder:
    if isinstance(config, http.bind.TcpBinder.Config):
        return http.bind.TcpBinder(config)
    elif isinstance(config, http.bind.UnixBinder.Config):
        return http.bind.UnixBinder(config)
    else:
        raise TypeError(config)


def test_app():
    server: http.servers.WsgiServer = None

    port = 8181

    def fn1():
        time.sleep(0.5)
        while True:
            try:
                response: requests.Response
                with contextlib.closing(requests.post(f'http://localhost:{port}/test', timeout=0.1)) as response:
                    if response.status_code == 200:
                        return
            except requests.RequestException:
                pass
            time.sleep(0.1)

    thread = threading.Thread(target=fn1)
    thread.start()

    def app(environ, start_response):
        assert environ['PATH_INFO'] == '/test'
        start_response(http.consts.STATUS_OK, [])
        server.shutdown()
        return [b'hi']

    binder = inject.create_binder()

    binder.bind(lifecycles.LifecycleManager, as_eager_singleton=True)
    binder.bind_provision_listener(LifecycleRegistrar())

    binder.bind(replserver.ReplServer.Config(os.path.join(tempfile.mkdtemp(), 'sock')))
    binder.bind(replserver.ReplServer, as_eager_singleton=True)
    bind_contextmanager_lifecycle(binder, replserver.ReplServer)
    binder.bind(ReplServerThread, as_eager_singleton=True)

    binder.bind(http.bind.TcpBinder.Config('0.0.0.0', port))
    binder.bind(http.bind.Binder.Config, to=http.bind.TcpBinder.Config)
    binder.bind_callable(provide_binder)

    binder.bind(http.wsgiref.ThreadSpawningWsgiRefServer, as_eager_singleton=True)
    binder.bind(http.servers.WsgiServer, to=http.wsgiref.ThreadSpawningWsgiRefServer)
    bind_contextmanager_lifecycle(binder, http.servers.WsgiServer)

    binder.bind(http.App, to_instance=app)

    injector = inject.create_injector(binder)

    lm = injector.get_instance(lifecycles.LifecycleManager)
    with lifecycles.context_manage(lm):
        server = injector.get_instance(http.servers.WsgiServer)
        with server.loop_context() as loop:
            for _ in loop:
                pass

    thread.join()


if __name__ == '__main__':
    import logging
    from ... import logs
    logs.configure_standard_logging(logging.INFO)
    test_app()
