#!/usr/bin/env python3
"""
TODO:
 - ensure (test) deplessness
 - replace shell shit
 - symlink as interp in omnibus repo root so can url github.com/wrmsr/omnibus/blob/master/interp.py
 - test vers better (lowest usable?)
 - tox?
 - install pyenv?
 - move this shit to dev somewhere
  - /scaffold? /project?
 - symlink $ROOT/project as ./python -m omnibus.dev.project ?
 - include python bins? is this scaffold? -momnibus.dev.project new barf?
 - pipx?
"""
import argparse
import os.path
import pprint
import shutil
import subprocess
import sys
import typing as ta

import pytest


REQUIRED_PYTHON_VERSION = (3, 7)


DEFAULT_CMD_TRY_EXCEPTIONS: ta.AbstractSet[ta.Type[Exception]] = frozenset([
    FileNotFoundError,
])


def _cmd(
        cmd: ta.Union[str, ta.Sequence[str]],
        *,
        try_: ta.Union[bool, ta.Iterable[ta.Type[Exception]]] = False,
        env: ta.Optional[ta.Mapping[str, str]] = None,
        **kwargs,
) -> ta.Optional[str]:
    pprint.pprint(cmd)
    if env:
        pprint.pprint(env)

    env = {**os.environ, **(env or {})}

    es = (Exception,)
    if isinstance(try_, bool):
        if try_:
            es = tuple(DEFAULT_CMD_TRY_EXCEPTIONS)
    elif try_:
        es = tuple(try_)
        try_ = True

    try:
        buf = subprocess.check_output(cmd, env=env, **kwargs)
    except es as e:
        if try_:
            print(e)
            return None
        else:
            raise

    out = buf.decode('utf-8').strip()
    print(out)
    return out


def install(args) -> None:
    python_version = '3.8.5'

    # PYENV_ROOT :=$(shell if [-z "$${PYENV_ROOT}"]; then echo "$${HOME}/.pyenv"; else echo "$${PYENV_ROOT%/}"; fi)
    # PYENV_BIN :=$(shell if [-f "$${HOME}/.pyenv/bin/pyenv"] ; then echo "$${HOME}/.pyenv/bin/pyenv"; else echo pyenv; fi)  # noqa
    pyenv_root = os.path.expanduser('~/.pyenv')
    pyenv_bin = os.path.join(pyenv_root, 'bin/pyenv')

    pyenv_install_dir = python_version
    pyenv_install_flags = ['-s', '-v']

    debug = False
    if debug:
        pyenv_install_dir += '-debug'
        pyenv_install_flags.append('-g')

    if sys.platform == 'darwin' and shutil.which('brew'):
        pyenv_cflags = []
        pyenv_ldflags = []

        pyenv_brew_deps = [
            'openssl',
            'readline',
            'sqlite3',
            'zlib',
        ]

        for dep in pyenv_brew_deps:
            dep_prefix = _cmd(['brew', '--prefix', dep])
            pyenv_cflags.append(f'-I{dep_prefix}/include')
            pyenv_ldflags.append(f'-L{dep_prefix}/lib')

        python_configure_opts = ['--enable-framework']
        if _cmd(['brew', '--prefix', 'tcl-tk'], try_=True) is not None:
            tcl_tk_prefix = _cmd(['brew', '--prefix', 'tcl-tk'])
            tcl_tk_ver = _cmd(r"brew ls --versions tcl-tk | head -n1 | egrep -o '[0-9]+\.[0-9]+'", shell=True)
            python_configure_opts.extend([
                f"--with-tcltk-includes='-I{tcl_tk_prefix}/include'",
                f"--with-tcltk-libs='-L{tcl_tk_prefix}/lib -ltcl{tcl_tk_ver} -ltk{tcl_tk_ver}'",
            ])

        pkg_config_path = _cmd(['brew', '--prefix', 'openssl'])
        if 'PKG_CONFIG_PATH' in os.environ:
            pkg_config_path += ':' + os.environ['PKG_CONFIG_PATH']

        env = {
            'CFLAGS': ' '.join(pyenv_cflags),
            'LDFLAGS': ' '.join(pyenv_ldflags),
            'PKG_CONFIG_PATH': pkg_config_path,
            'PYTHON_CONFIGURE_OPTS': ' '.join(python_configure_opts),
        }

        _cmd([pyenv_bin, 'install', *pyenv_install_flags, python_version], env=env)


@pytest.mark.skip
def test_interp():
    argv = []

    if sys.version_info < REQUIRED_PYTHON_VERSION:
        raise EnvironmentError(f'Requires python {REQUIRED_PYTHON_VERSION}, got {sys.version_info} from {sys.executable}')  # noqa

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser_install = subparsers.add_parser('install')
    parser_install.add_argument('ver')
    parser_install.set_defaults(func=install)

    args = parser.parse_args(argv)
    if not getattr(args, 'func', None):
        parser.print_help()
    else:
        args.func(args)
