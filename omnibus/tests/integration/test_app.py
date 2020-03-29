import contextlib
import threading
import time

import requests

from ... import http
from ... import inject
from ... import lifecycles


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

        def __init__(self, lm: lifecycles.LifecycleManager) -> None:
            super().__init__()

            self._lm = lm

        def __call__(self, key, instance) -> None:
            if isinstance(instance, lifecycles.Lifecycle) and instance is not self._lm:
                self._lm.add(instance)

    binder = inject.create_binder()

    binder.bind(http.App, to_instance=app)

    binder.bind(http.bind.Binder, to_instance=http.bind.TCPBinder('0.0.0.0', port))
    binder.bind(http.wsgiref.ThreadSpawningWsgiRefServer, as_eager_singleton=True)
    binder.bind(http.servers.WsgiServer, to=http.wsgiref.ThreadSpawningWsgiRefServer)

    binder.bind(lifecycles.LifecycleManager, as_eager_singleton=True)

    binder.bind(LifecycleRegistrar)
    binder.bind_provision_listener(LifecycleRegistrar)

    injector = inject.create_injector(binder)

    lm = injector.get_instance(lifecycles.LifecycleManager)
    with lifecycles.context_manage(lm):
        with injector.get_instance(http.servers.WsgiServer) as server:
            with server.loop_context() as loop:
                for _ in loop:
                    pass

    thread.join()
