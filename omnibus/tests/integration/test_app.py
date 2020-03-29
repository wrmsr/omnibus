import contextlib
import threading
import time

import requests

from ... import collections as ocol
from ... import dataclasses as dc
from ... import http
from ... import inject
from ... import lang
from ... import lifecycles
from ... import replserver


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

    @dc.dataclass(frozen=True)
    class BinderConfig(lang.Abstract):
        pass

    @dc.dataclass(frozen=True)
    class TcpBinderConfig(BinderConfig, lang.Final):
        host: str
        port: int

    @dc.dataclass(frozen=True)
    class UnixBinderConfig(BinderConfig, lang.Final):
        address: str

    def provide_binder(config: BinderConfig) -> http.bind.Binder:
        if isinstance(config, TcpBinderConfig):
            return http.bind.TcpBinder(config.host, config.port)
        elif isinstance(config, UnixBinderConfig):
            return http.bind.UnixBinder(config.address)
        else:
            raise TypeError(config)

    binder = inject.create_binder()

    binder.bind(http.App, to_instance=app)

    binder.bind(BinderConfig, to_instance=TcpBinderConfig('0.0.0.0', port))
    binder.bind_callable(provide_binder)

    binder.bind(http.wsgiref.ThreadSpawningWsgiRefServer, as_eager_singleton=True)
    binder.bind(http.servers.WsgiServer, to=http.wsgiref.ThreadSpawningWsgiRefServer)

    binder.bind(lifecycles.LifecycleManager, as_eager_singleton=True)
    binder.bind_provision_listener(LifecycleRegistrar())

    injector = inject.create_injector(binder)

    lm = injector.get_instance(lifecycles.LifecycleManager)
    with lifecycles.context_manage(lm):
        server = injector.get_instance(http.servers.WsgiServer)
        with server.loop_context() as loop:
            for _ in loop:
                pass

    thread.join()
