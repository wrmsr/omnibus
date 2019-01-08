import json
import os
import stat
import sys
import tempfile
import textwrap
import types
import typing as ta

from . import check
from . import lang


ARGS_ENV_VAR = 'PYDEVD_ARGS'


@lang.cached_nullary
def _pydevd() -> ta.Optional[types.ModuleType]:
    try:
        return __import__('pydevd')
    except ImportError:
        return None


def is_present() -> bool:
    return _pydevd() is not None


def get_setup() -> ta.Optional[ta.Dict]:
    if is_present():
        return _pydevd().SetupHolder.setup
    else:
        return None


def is_running() -> bool:
    return get_setup() is not None


def get_args() -> ta.List[str]:
    check.state(is_present())
    setup = get_setup()
    args = [_pydevd().__file__]

    for k in [
        'port',
        'vm_type',
        'client',
    ]:
        if setup[k]:
            args.extend(['--' + k, str(setup[k])])

    for k in [
        'server',
        'multiproc',
        'multiprocess',
        'save-signatures',
        'save-threading',
        'save-asyncio',
        'print-in-debugger-startup',
        'cmd-line',
    ]:
        if setup[k]:
            args.append('--' + k)

    if setup['qt-support']:
        args.append('--qt-support=' + setup['qt-support'])

    return args


def save_args() -> None:
    if is_present():
        os.environ[ARGS_ENV_VAR] = json.dumps(get_args())


def maybe_reexec(file: str) -> None:
    if ARGS_ENV_VAR in os.environ:
        import pydevd

        if pydevd.SetupHolder.setup is None:
            args = [sys.executable]
            args.extend(json.loads(os.environ['PYDEVD_ARGS']))
            args.extend(['--file', file])
            args.extend(sys.argv[1:])
            os.execvp(sys.executable, args)


def write_file_proxy() -> str:
    path = tempfile.mkdtemp()
    os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

    with open(path, 'w') as f:
        f.write(textwrap.dedent(f"""
        #!{os.path.abspath(sys.executable)}
        import runpy
        import sys

        import {__name__} as pydevd
        pydevd.maybe_reexec()

        runpy.run_file(sys.argv[0])
        """))

    return path
