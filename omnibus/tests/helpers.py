import contextlib
import os
import threading
import time
import typing as ta

import pytest


DEFAULT_TIMEOUT_S = 30


def run_with_timeout(
        *fns: ta.Callable[[], None],
        timeout_s: int = None,
        timeout_exception: Exception = RuntimeError('Thread timeout')
) -> None:
    if timeout_s is None:
        timeout_s = DEFAULT_TIMEOUT_S

    thread_exception: Exception = None

    def inner(fn):
        try:
            fn()
        except Exception as e:
            nonlocal thread_exception
            thread_exception = e
            raise

    threads = [threading.Thread(target=inner, args=(fn,)) for fn in fns]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout_s)
    for thread in threads:
        if thread.is_alive():
            raise timeout_exception

    if thread_exception is not None:
        raise thread_exception


def waitpid_with_timeout(
        pid: int,
        timeout_s: int = None,
        timeout_exception: Exception = RuntimeError('waitpid timeout')
) -> int:
    if timeout_s is None:
        timeout_s = DEFAULT_TIMEOUT_S

    start_time = time.time()

    while True:
        wait_pid, status = os.waitpid(pid, os.WNOHANG)
        if wait_pid != 0:
            if wait_pid != pid:
                raise ValueError(f'{wait_pid} != {pid}')
            return status

        elapsed_time = time.time() - start_time
        if elapsed_time >= timeout_s:
            raise timeout_exception


@contextlib.contextmanager
def with_env(**env):
    prev = {}

    for k, v in env.items():
        prev[k] = os.environ.get(k)
        if v is None:
            if k in os.environ:
                del os.environ[k]
        else:
            os.environ[k] = str(v)

    yield

    for k, v in prev.items():
        if v is None:
            if k in os.environ:
                del os.environ[k]
        else:
            os.environ[k] = prev[k]


def can_import(*args, **kwargs) -> bool:
    try:
        __import__(*args, **kwargs)
    except ImportError:
        return False
    else:
        return True


def skip_if_cant_import(module: str):
    return pytest.mark.skipif(not can_import(module), reason=f'requires import {module}')
