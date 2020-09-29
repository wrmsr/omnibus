#@omnibus
import fnmatch
import functools
import glob
import os
import shutil
import subprocess
import sys
import tempfile
import textwrap
import traceback

import setuptools.command.build_ext
import setuptools.command.build_py
import setuptools.command.sdist

import distutils.ccompiler
import distutils.command.build
import distutils.command.build_ext
import distutils.core
import distutils.errors
import distutils.log
import distutils.sysconfig


# region About


PROJECT = 'omnibus'

BASE_DIR = os.path.dirname(__file__)
ABOUT = {}


def _read_about():
    with open(os.path.join(BASE_DIR, PROJECT, '__about__.py'), 'rb') as f:
        src = f.read()
        if sys.version_info[0] > 2:
            src = src.decode('UTF-8')
        exec(src, ABOUT)


_read_about()


# endregion


# region Data


INCLUDED_STATIC_FILE_PATHS = {
    '*.cc',
    '*.dss',
    '*.g4',
    '*.h',
    '*.interp',
    '*.m',
    '*.pxd',
    '*.pyi',
    '*.pyx',
    '*.tokens',
}

EXCLUDED_STATIC_FILE_PATHS = {
    '*.py',
    '*.so',
    '*/__pycache__/*',
    '*/_ext/cy/*.cpp',
    '*/tests/*',
}


def _get_static_files(path):
    ret = []
    for (dirpath, dirnames, filenames) in os.walk(path, followlinks=True):
        for filename in filenames:
            for filepath in [os.path.join(dirpath, filename)]:
                if (
                        any(fnmatch.fnmatch(filepath, pat) for pat in INCLUDED_STATIC_FILE_PATHS) and
                        not any(fnmatch.fnmatch(filepath, pat) for pat in EXCLUDED_STATIC_FILE_PATHS)
                ):
                    ret.append(filepath)
    return ret


PACKAGE_DATA = [
] + _get_static_files(PROJECT)


# endregion


# region Requires


INSTALL_REQUIRES = [
]

EXTRAS_REQUIRE = {
}


# endregion


# region Extensions


APPLE = sys.platform == 'darwin'


DEBUG = os.environ.get('DEBUG')
TRACE = os.environ.get('TRACE')


EXT_TOGGLES_BY_FNAME = {
}

EXT_KWARGS_BY_FNAME = {
}


def try_compile(
        src: str,
        *,
        name=None,
        errors=(
            distutils.errors.CompileError,
            distutils.errors.LinkError,
            subprocess.CalledProcessError,
        ),
        **kwargs
) -> bool:
    tmp_dir = tempfile.mkdtemp()
    try:
        bin_file_name = os.path.join(tmp_dir, 'test')
        file_name = bin_file_name + '.c'
        with open(file_name, 'w') as fp:
            fp.write(src)

        compiler = distutils.ccompiler.new_compiler()
        distutils.sysconfig.customize_compiler(compiler)

        def new_exec(old, *args, **kwargs):
            os.close(sys.stderr.fileno())
            null = os.open('/dev/null', os.O_WRONLY)
            os.dup2(null, sys.stderr.fileno())
            return old(*args, **kwargs)
        old_os_atts = {}
        for att in {'execv', 'execve', 'execvp', 'execvpe'}:
            old = old_os_atts[att] = getattr(os, att)
            setattr(os, att, functools.partial(new_exec, old))

        try:
            compiler.link_executable(
                compiler.compile(
                    [file_name],
                    output_dir=tmp_dir,
                ),
                bin_file_name,
                output_dir=tmp_dir,
                **kwargs
            )
            subprocess.check_call(bin_file_name)
        except errors:
            distutils.log.debug(traceback.format_exc())
            if name:
                distutils.log.warn(f'{name} not found')
            return False
        else:
            if name:
                distutils.log.info(f'{name} found')
            return True
        finally:
            for att, old in old_os_atts.items():
                setattr(os, att, old)

    finally:
        shutil.rmtree(tmp_dir)


HAS_PCRE2 = lambda: try_compile(
    textwrap.dedent("""
#define PCRE2_CODE_UNIT_WIDTH 8
#include <pcre2.h>

int main(int argc, char *argv[]) {
  int errornumber;
  PCRE2_SIZE erroroffset;
  pcre2_code *re;
  re = pcre2_compile((PCRE2_SPTR) ".*", PCRE2_ZERO_TERMINATED, 0, &errornumber, &erroroffset, NULL);
  if (re == NULL)
    return 1;
  return 0;
}
"""),
    libraries=['pcre2-8'],
    name='pcre2',
)

EXT_TOGGLES_BY_FNAME['pcre2.pyx'] = HAS_PCRE2
EXT_KWARGS_BY_FNAME['pcre2.pyx'] = {'libraries': ['pcre2-8']}


EXT_MODULES = [
    *[
        setuptools.Extension(
            fpath.rpartition('.')[0].replace('/', '.'),
            sources=[fpath],
            extra_compile_args=['-std=c++14'],
            optional=True,
            **EXT_KWARGS_BY_FNAME.get(os.path.basename(fpath), {}),
        )
        for fpath in glob.glob(f'{PROJECT}/_ext/cc/*.cc')
        if EXT_TOGGLES_BY_FNAME.get(os.path.basename(fpath), lambda: True)()
    ]
]


try:
    import Cython
except ImportError:
    pass
else:
    import Cython.Build
    import Cython.Compiler.Options

    EXT_MODULES.extend([
        *Cython.Build.cythonize(
            [
                setuptools.Extension(
                    fpath.rpartition('.')[0].replace('/', '.'),
                    sources=[fpath],
                    language='c++',
                    extra_compile_args=['-std=c++14'],
                    optional=True,
                    define_macros=[
                        *([('CYTHON_TRACE', '1')] if TRACE else []),
                    ],
                    **EXT_KWARGS_BY_FNAME.get(os.path.basename(fpath), {}),
                )
                for fpath in glob.glob(f'{PROJECT}/_ext/cy/**/*.pyx', recursive=True)
                if EXT_TOGGLES_BY_FNAME.get(os.path.basename(fpath), lambda: True)()
            ],
            language_level=3,
            gdb_debug=DEBUG,
            compiler_directives={
                **Cython.Compiler.Options.get_directive_defaults(),
                'linetrace': TRACE,
                'embedsignature': True,
                'binding': True,
            },
        ),
    ])


if APPLE:
    EXT_MODULES.extend([
        setuptools.Extension(
            fpath.rpartition('.')[0].replace('/', '.'),
            sources=[fpath],
            extra_link_args=[
                '-framework', 'AppKit',
                '-framework', 'CoreFoundation',
            ],
            optional=True,
            **EXT_KWARGS_BY_FNAME.get(os.path.basename(fpath), {}),
        )
        for fpath in glob.glob(f'{PROJECT}/_ext/m/*.m')
        if EXT_TOGGLES_BY_FNAME.get(os.path.basename(fpath), lambda: True)()
    ])


def new_build_ext_init_opts(self, *args, **kwargs):
    old_build_ext_init_opts(self, *args, **kwargs)
    self.parallel = os.cpu_count()

old_build_ext_init_opts = distutils.command.build_ext.build_ext.initialize_options  # noqa
distutils.command.build_ext.build_ext.initialize_options = new_build_ext_init_opts  # noqa


# endregion


# region Hooks


def _rewrite_sdist_template(template, distribution):
    tmp_dir = tempfile.mkdtemp()
    with open(template, 'r') as f:
        lines = f.readlines()

    lines = [
        l
        for l in lines
        for l in [l.strip()]
        if not (distribution.is_dev and l.endswith('#@dev'))
    ]

    template = os.path.join(tmp_dir, os.path.basename(template))
    with open(template, 'w') as f:
        f.write('\n'.join(lines))

    return template


def new_sdist_read_template(self):
    self.filelist.distribution = self.distribution
    self.template = _rewrite_sdist_template(self.template, self.distribution)
    old_sdist_read_template(self)

old_sdist_read_template = setuptools.command.sdist.sdist.read_template  # noqa
setuptools.command.sdist.sdist.read_template = new_sdist_read_template  # noqa


def new_build_py_find_package_modules(self, package, package_dir):
    modules = old_build_py_find_package_modules(self, package, package_dir)
    if package == PROJECT:
        modules = [t for t in modules if t[1] != 'conftest']
    return modules

old_build_py_find_package_modules = setuptools.command.build_py.build_py.find_package_modules  # noqa
setuptools.command.build_py.build_py.find_package_modules = new_build_py_find_package_modules  # noqa


class Distribution(distutils.core.Distribution):

    global_options = distutils.core.Distribution.global_options + [  # noqa
        ('dev', None, 'install dev'),
    ]

    dev = 0

    def run_commands(self):
        self._packages = None
        super().run_commands()

    @property
    def is_dev(self):
        return self.dev or int(os.environ.get(f'__{PROJECT.upper()}_DEV', '0'))

    @property
    def packages(self):
        if self._packages is None:
            self._packages = setuptools.find_packages(
                include=[PROJECT, PROJECT + '.*'],
                exclude=[
                    'tests', '*.tests', '*.tests.*',
                    'conftest', '*.conftest',
                    *([] if self.is_dev else ['dev', '*.dev', '*.dev.*'])
                ],
            )
        return self._packages

    @packages.setter
    def packages(self, v):
        if v is not None:
            raise TypeError(v)


# endregion


if __name__ == '__main__':
    setuptools.setup(
        name=ABOUT['__title__'],
        version=ABOUT['__version__'],
        description=ABOUT['__description__'],
        author=ABOUT['__author__'],
        url=ABOUT['__url__'],

        distclass=Distribution,

        python_requires=ABOUT['__python_requires__'],
        classifiers=ABOUT['__classifiers__'],

        setup_requires=['setuptools'],

        py_modules=[PROJECT],

        package_data={PROJECT: PACKAGE_DATA},
        include_package_data=True,

        entry_points={},

        install_requires=INSTALL_REQUIRES,
        extras_require=EXTRAS_REQUIRE,

        ext_modules=EXT_MODULES,
    )
