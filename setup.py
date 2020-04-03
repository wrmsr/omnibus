import fnmatch
import glob
import os
import os.path
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


EXCLUDED_STATIC_FILE_PATHS = [
    '*.py',
    '*/__pycache__/*',
    '*/tests/*',
    '*/_ext/cc/*',
    '*/_ext/cy/*',
    '*/_ext/rs/*',
]


def _get_static_files(path):
    return [
        filepath
        for (dirpath, dirnames, filenames) in os.walk(path, followlinks=True)
        for filename in filenames
        for filepath in [os.path.join(dirpath, filename)]
        if not any(fnmatch.fnmatch(filepath, pat) for pat in EXCLUDED_STATIC_FILE_PATHS)
    ]


PACKAGE_DATA = [
    '.revision',
] + _get_static_files('omnibus')


INSTALL_REQUIRES = [
    'toolz>=0.9.0',
]

EXTRAS_REQUIRE = {
    'cytoolz': ['cytoolz>=0.9.0'],
    'docker': ['docker>=3.7.0'],
    'sortedcontainers': ['sortedcontainers>=2.1.0'],
}


DEBUG = 'DEBUG' in os.environ


EXT_MODULES = []

try:
    import Cython

except ImportError:
    pass

else:
    import Cython.Build
    import Cython.Compiler.Options

    EXT_MODULES.extend([
        *[
            setuptools.Extension(
                'omnibus._ext.cc.' + os.path.basename(fpath).rpartition('.')[0],
                sources=[fpath]
            )
            for fpath in glob.glob('omnibus/_ext/cc/*.cc')
        ],
        *Cython.Build.cythonize(
            [
                setuptools.Extension(
                    'omnibus._ext.cy.' + os.path.basename(fpath).rpartition('.')[0],
                    sources=[fpath],
                    language='c++',
                )
                for fpath in glob.glob('omnibus/_ext/cy/**/*.pyx', recursive=True)
            ],
            language_level=3,
            gdb_debug=DEBUG,
            compiler_directives={
                **Cython.Compiler.Options.get_directive_defaults(),
                'embedsignature': True,
                'binding': True,
            },
        ),
    ])

    if APPLE:
        EXT_MODULES.extend([
            setuptools.Extension(
                'omnibus._ext.m.' + os.path.basename(fpath).rpartition('.')[0],
                sources=[fpath],
                extra_link_args=[
                    '-framework', 'AppKit',
                    '-framework', 'CoreFoundation',
                ]
            )
            for fpath in glob.glob('omnibus/_ext/m/*.m')
        ])


class Distribution(setuptools.dist.Distribution):

    dev = 0
    _omnibus_attrs_set = False

    def _get_toplevel_options(self):
        return super()._get_toplevel_options() + [
            ('dev', None, 'omnibus-dev'),
        ]

    def parse_command_line(self):
        ok = super().parse_command_line()

        if not self._omnibus_attrs_set:
            if self.dev:
                self.install_requires = [ABOUT['__title__'] + '==' + ABOUT['__version__']]
                self.extras_require = {}
                self.metadata.provides_extras = type(self.metadata.provides_extras)()

            self.metadata.name = ABOUT['__title__'] + ('-dev' if self.dev else '')

            self._omnibus_attrs_set = True

        return ok

    def get_command_obj(self, command, create=1):
        obj = super().get_command_obj(command, create)

        if command == 'egg_info':
            def obj_find_sources():
                from setuptools.command.egg_info import manifest_maker
                manifest_filename = os.path.join(obj.egg_info, "SOURCES.txt")
                mm = manifest_maker(obj.distribution)
                mm.manifest = manifest_filename

                def mm_write_manifest(*args, **kwargs):
                    if not self.dev:
                        mm.filelist.prune('omnibus/dev')
                    else:
                        for e in os.listdir('omnibus'):
                            if e == 'dev':
                                continue
                            e = 'omnibus/' + e
                            if os.path.isdir(e):
                                mm.filelist.prune(e)
                            elif os.path.isfile(e) and e.endswith('.py') and not e.startswith('_'):
                                mm.filelist.exclude(e)

                    orig_mm_write_manifest(*args, **kwargs)
                orig_mm_write_manifest, mm.write_manifest = mm.write_manifest, mm_write_manifest

                mm.run()
                obj.filelist = mm.filelist

            obj.find_sources = obj_find_sources

        return obj


if __name__ == '__main__':
    setuptools.setup(
        distclass=Distribution,

        name=ABOUT['__title__'],
        version=ABOUT['__version__'],
        description=ABOUT['__description__'],
        author=ABOUT['__author__'],
        url=ABOUT['__url__'],

        python_requires='>=3.7',

        classifiers=[
            'Intended Audience :: Developers',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: ' + '.'.join(map(str, sys.version_info[:2])),
            'Programming Language :: Python :: Implementation :: CPython',
            'Programming Language :: Python',
        ],

        # zip_safe=True,

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
