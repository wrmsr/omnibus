import fnmatch
import glob
import os
import sys

import setuptools.command.build_ext


APPLE = sys.platform == 'darwin'


BASE_DIR = os.path.dirname(__file__)
ABOUT = {}


def _read_about():
    with open(os.path.join(BASE_DIR, 'omnibus', '__about__.py'), 'rb') as f:
        src = f.read()
        if sys.version_info[0] > 2:
            src = src.decode('UTF-8')
        exec(src, ABOUT)


_read_about()


INCLUDED_STATIC_FILE_PATHS = {
    '*.cc',
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
] + _get_static_files('omnibus')


INSTALL_REQUIRES = [
]

EXTRAS_REQUIRE = {
}


DEBUG = os.environ.get('DEBUG')
TRACE = os.environ.get('TRACE')


EXT_MODULES = [
    *[
        setuptools.Extension(
            fpath.rpartition('.')[0].replace('/', '.'),
            sources=[fpath],
            extra_compile_args=['-std=c++14'],
            optional=True,
        )
        for fpath in glob.glob('omnibus/_ext/cc/*.cc')
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
                )
                for fpath in glob.glob('omnibus/_ext/cy/**/*.pyx', recursive=True)
            ],
            language_level=3,
            gdb_debug=DEBUG,
            compiler_directives={
                **Cython.Compiler.Options.get_directive_defaults(),
                'linetrace': TRACE,
                'embedsignature': True,
                'binding': True,
            },
            # FIXME: nthreads=os.cpu_count(),
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
        )
        for fpath in glob.glob('omnibus/_ext/m/*.m')
    ])


def new_build_ext_init_opts(self, *args, **kwargs):
    old_build_ext_init_opts(self, *args, **kwargs)
    self.parallel = os.cpu_count()

import distutils.command.build_ext  # noqa
old_build_ext_init_opts = distutils.command.build_ext.build_ext.initialize_options  # noqa
distutils.command.build_ext.build_ext.initialize_options = new_build_ext_init_opts  # noqa


if __name__ == '__main__':
    setuptools.setup(
        name=ABOUT['__title__'],
        version=ABOUT['__version__'],
        description=ABOUT['__description__'],
        author=ABOUT['__author__'],
        url=ABOUT['__url__'],

        python_requires=ABOUT['__python_requires__'],
        classifiers=ABOUT['__classifiers__'],

        setup_requires=['setuptools'],

        packages=setuptools.find_packages(
            include=['omnibus', 'omnibus.*'],
            exclude=['tests', '*.tests', '*.tests.*'],
        ),
        py_modules=['omnibus'],

        package_data={'omnibus': PACKAGE_DATA},
        include_package_data=True,

        entry_points={},

        install_requires=INSTALL_REQUIRES,
        extras_require=EXTRAS_REQUIRE,

        ext_modules=EXT_MODULES,
    )
