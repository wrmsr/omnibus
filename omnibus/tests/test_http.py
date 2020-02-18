import contextlib
import time

import requests

from . import helpers
from .. import http
from .. import json


def test_http():
    server: http.WSGIServer = None

    def app(environ, start_response):
        assert environ['PATH_INFO'] == '/test'
        start_response(http.STATUS_OK, [])
        server.shutdown()
        return [b'hi']

    port = 8181

    def fn0():
        nonlocal server
        server = http.ThreadSpawningWSGIServer(http.TCPBinder('0.0.0.0', port), app)
        with server:
            server.run()

    def fn1():
        while True:
            try:
                response: requests.Response
                with contextlib.closing(requests.post(f'http://localhost:{port}/test', timeout=0.1)) as response:
                    if response.status_code == 200:
                        return
            except requests.RequestException:
                pass
            time.sleep(0.1)

    helpers.run_with_timeout(fn0, fn1)


def test_json_http():
    server: http.WSGIServer = None

    def json_app(obj):
        server.shutdown()
        return {'hi': True}

    port = 8181

    def fn0():
        nonlocal server
        server = http.ThreadSpawningWSGIServer(http.TCPBinder('0.0.0.0', port), http.simple_json_app(json_app))
        with server:
            server.run()

    def fn1():
        while True:
            try:
                response: requests.Response
                with contextlib.closing(requests.post(f'http://localhost:{port}/test', timeout=0.1)) as response:
                    if response.status_code == 200:
                        assert json.loads(response.content) == {'hi': True}
                        return
            except requests.RequestException:
                pass
            time.sleep(0.1)

    helpers.run_with_timeout(fn0, fn1)
