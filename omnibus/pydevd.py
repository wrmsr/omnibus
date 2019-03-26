import json
import os
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


def silence() -> None:
    def stderr_write(*args, **kwargs):
        pass
    pydev_log = __import__('pydevd._pydev_bundle.pydev_log')._pydev_bundle.pydev_log
    pydev_log.stderr_write = stderr_write


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


def maybe_reexec(file: str, *, silence: bool = False) -> None:
    if ARGS_ENV_VAR in os.environ:
        import pydevd

        if pydevd.SetupHolder.setup is None:
            args = [sys.executable]
            args.extend(json.loads(os.environ['PYDEVD_ARGS']))
            args.extend(['--file', file])
            args.extend(sys.argv[1:])

            if silence:
                tmpdir = tempfile.mkdtemp()
                bootstrap_path = os.path.join(tmpdir, 'bootstrap.py')
                with open(bootstrap_path, 'w') as f:
                    f.write(textwrap.dedent(f"""
                    import sys
                    old_paths = set(sys.path)
                    for new_path in {sys.path!r}:
                        if new_path not in old_paths:
                            sys.path.insert(0, new_path)
                    sys.argv = {args[1:]!r}
                    import runpy
                    runpy.run_path({args[1]!r}, run_name='__main__')
                    """))
                args = [args[0], bootstrap_path]

            os.execvp(sys.executable, args)


