#@omnibus
import dataclasses as dc
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
import typing as ta

import setuptools.command.build_ext
import setuptools.command.build_py
import setuptools.command.sdist

import distutils.ccompiler
import distutils.cmd
import distutils.command.build
import distutils.command.build_ext
import distutils.core
import distutils.errors
import distutils.log
import distutils.sysconfig


PROJECT = 'omnibus'


__dist__ = None


# region Dists


@dc.dataclass(frozen=True)
class DistType:
    name: ta.Optional[str]
    deps: ta.Sequence[ta.Optional[str]]


DISTS_BY_NAME: ta.Mapping[ta.Optional[str], DistType] = {d.name: d for d in [
    DistType(None, []),
    DistType('dev', [None]),
]}

DIST = DISTS_BY_NAME[__dist__]


# endregion


# region Env


def _read_about() -> ta.Mapping[str, ta.Any]:
    dct = {}
    with open(os.path.join(os.path.dirname(__file__), PROJECT, '__about__.py'), 'rb') as f:
        src = f.read()
        if sys.version_info[0] > 2:
            src = src.decode('UTF-8')
        exec(src, ta.cast(ta.Dict, dct))
    return dct


ABOUT = _read_about()


APPLE = sys.platform == 'darwin'


DEBUG = os.environ.get('DEBUG')
TRACE = os.environ.get('TRACE')


# endregion


# region Config


STATIC_FILES: ta.AbstractSet[str] = set()


INCLUDED_STATIC_FILE_PATHS: ta.AbstractSet[str] = {
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


EXCLUDED_STATIC_FILE_PATHS: ta.AbstractSet[str] = {
    '*.py',
    '*.so',
    '*/__pycache__/*',
    '*/_ext/cy/*.cpp',
    '*/tests/*',
}


EXTRAS_REQUIRE: ta.Mapping[str, ta.Sequence[str]] = {
}


IGNORED_PACKAGE_MODULES: ta.AbstractSet[str] = {
    'conftest',
}


# endregion


# region Extension Config


@dc.dataclass(frozen=True)
class Ext:
    fnames: ta.Collection[str]
    cond: ta.Optional[ta.Callable[[], bool]] = None
    kwargs: ta.Optional[ta.Mapping[str, ta.Any]] = None

    def __post_init__(self):
        if isinstance(self.fnames, str):
            raise TypeError(self.fnames)


@dc.dataclass(frozen=True)
class TryCompile:
    name: str
    src: str
    kwargs: ta.Optional[ta.Mapping[str, ta.Any]] = None

    _value: ta.Optional[bool] = None

    def __call__(self) -> bool:
        if self._value is None:
            self.__dict__['_value'] = try_compile(self.name, self.src, **self.kwargs)
        return self._value


HAS_PCRE2 = TryCompile(
    'pcre2',
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
    kwargs={'libraries': ['pcre2-8']},
)


EXTS: ta.Sequence[Ext] = [
    Ext(['pcre2.pyx'], cond=HAS_PCRE2, kwargs={'libraries': ['pcre2-8']}),
]


# endregion


# region Utils


_IGNORE = object()


class cached_property:  # noqa
    def __init__(self, fn, *, name=None, ignore_if=lambda _: False):
        super().__init__()
        if isinstance(fn, property):
            fn = fn.fget
        self._fn = fn
        self._ignore_if = ignore_if
        self._name = name

    def __set_name__(self, owner, name):
        if self._name is None:
            self._name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if self._name is None:
            raise TypeError(self)
        value = self._fn.__get__(instance, owner)()
        if value is _IGNORE:
            return None
        instance.__dict__[self._name] = value
        return value

    def __set__(self, instance, value):
        if self._ignore_if(value):
            return
        raise TypeError(self._name)


none_ignoring_cached_property = functools.partial(cached_property, ignore_if=lambda v: v is None)
falsey_ignoring_cached_property = functools.partial(cached_property, ignore_if=lambda v: not v)


class cached_nullary:  # noqa
    def __init__(self, fn, *, name=None):
        super().__init__()
        self._fn = fn
        self._name = name
        self._value = _IGNORE

    def __set_name__(self, owner, name):
        if self._name is None:
            self._name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if self._name is None:
            raise TypeError(self)
        ret = instance.__dict__[self._name] = type(self)(self._fn.__get__(instance, owner), name=self._name)
        return ret

    def __call__(self, *args, **kwargs):
        if self._value is not _IGNORE:
            return self._value
        val = self._fn(*args, **kwargs)
        if val is _IGNORE:
            return None
        self._value = val
        return val


class wrapper:  # noqa
    def __init__(self, wrapper, wrapped, *, instance=None):
        super().__init__()
        self._wrapper = wrapper
        self._wrapped = wrapped
        self._instance = instance
        functools.update_wrapper(self, wrapped)

    def __get__(self, instance, owner):
        return type(self)(self._wrapper, self._wrapped, instance=instance)

    def __call__(self, *args, **kwargs):
        return self._wrapper(self._wrapped, *([self._instance] if self._instance is not None else []), *args, **kwargs)


# endregion


# region Extension Utils


def try_compile(
        name: str,
        src: str,
        *,
        errors: ta.Collection[ta.Type[BaseException]] = (
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
        except tuple(errors):
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


# endregion


# region Hooks


def _hook(obj, att):
    def inner(fn):
        old = getattr(obj, att)
        setattr(obj, att, wrapper(fn, old))
        return fn
    return inner


@_hook(distutils.command.build_ext.build_ext, 'initialize_options')  # noqa
def _new_build_ext_init_opts(old, self, *args, **kwargs):
    old(self, *args, **kwargs)
    self.parallel = os.cpu_count()


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


@_hook(setuptools.command.sdist.sdist, 'read_template')
def _new_sdist_read_template(old, self):
    self.filelist.distribution = self.distribution
    self.template = _rewrite_sdist_template(self.template, self.distribution)
    old(self)


@_hook(setuptools.command.build_py.build_py, 'find_package_modules')
def _new_build_py_find_package_modules(old, self, package, package_dir):
    modules = old(self, package, package_dir)
    if package == PROJECT:
        modules = [t for t in modules if t[1] not in IGNORED_PACKAGE_MODULES]
    return modules


try:
    import pkg_resources
except ImportError:
    pass
else:
    @_hook(pkg_resources, 'iter_entry_points')
    def _new_pkg_resources_iter_entry_points(old, group, name=None):
        # Bad deps break --help-commands :
        #   https://github.com/dbcli/litecli/blob/a1a01c11d6154b6f841b81fbdeb6b8b887b697d3/setup.py#L52
        # Opted for patch not overriding Distribution.print_commands to prefer reduced coupling over requiring this to
        # always work.
        eps = old(group, name=name)
        if group == 'distutils.commands':
            good_eps = []
            for ep in eps:
                if ep.name not in CMDCLASS:
                    try:
                        ep.resolve()
                    except Exception as e:
                        distutils.log.warn(f'Failed to resolve {ep!r} from {ep.dist!r}: {e!r}')
                        continue
                    good_eps.append(ep)
            eps = good_eps
        return eps


# endregion


# region Main Class


class Distribution(distutils.core.Distribution):
    global_options = distutils.core.Distribution.global_options + [  # noqa
        ('dev', None, 'install dev'),
    ]

    dev = 0

    _has_finalized_options = False

    def finalize_options(self):
        super().finalize_options()  # noqa
        self._has_finalized_options = True

    @cached_property  # noqa
    @property
    def is_dev(self):
        return self.dev or int(os.environ.get(f'__{PROJECT.upper()}_DEV', '0'))

    @none_ignoring_cached_property  # noqa
    @property
    def packages(self):
        return setuptools.find_packages(
            include=[PROJECT, PROJECT + '.*'],
            exclude=[
                'tests', '*.tests', '*.tests.*',
                'conftest', '*.conftest',
                *([] if self.is_dev else ['dev', '*.dev', '*.dev.*'])
            ],
        )

    # region Data

    def _get_static_files(self, path: str) -> ta.Sequence[str]:
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

    @falsey_ignoring_cached_property  # noqa
    @property
    def package_data(self) -> ta.Mapping[str, ta.Sequence[str]]:
        return {PROJECT: [
            *STATIC_FILES,
            *self._get_static_files(PROJECT),
        ]}

    # endregion

    # region Requires

    @falsey_ignoring_cached_property  # noqa
    @property
    def install_requires(self) -> ta.Sequence[str]:
        return [
            *[
                PROJECT + (('-' + d.name) if d.name is not None else '') + '==' + ABOUT['__version__']
                for dn in DIST.deps
                for d in [DISTS_BY_NAME[dn]]],
        ]

    @falsey_ignoring_cached_property  # noqa
    @property
    def extras_require(self) -> ta.Mapping[str, ta.Sequence[str]]:
        return EXTRAS_REQUIRE

    # endregion

    # region Extensions

    @none_ignoring_cached_property  # noqa
    @property
    def ext_modules(self):
        if not self._has_finalized_options:
            return _IGNORE
        return [
            *self._yield_cc_ext_modules(),
            *self._yield_cy_ext_modules(),
            *self._yield_m_ext_modules(),
        ]

    @cached_property  # noqa
    @property
    def _exts_by_fname(self) -> ta.Mapping[str, Ext]:
        dct = {}
        for ce in EXTS:
            for fn in ce.fnames:
                if fn in dct:
                    raise KeyError(fn)
                dct[fn] = ce
        return dct

    def _yield_ext_fpaths(self, pat: str) -> ta.Iterator[ta.Tuple[str, ta.Optional[Ext]]]:
        for fpath in glob.glob(f'{PROJECT}/_ext/{pat}', recursive=True):
            e = self._exts_by_fname.get(os.path.basename(fpath))
            if e is not None and not e.cond():
                continue
            yield fpath, e

    def _yield_cc_ext_modules(self) -> ta.Iterator[setuptools.Extension]:
        for fpath, e in self._yield_ext_fpaths('cc/*.cc'):
            yield setuptools.Extension(
                fpath.rpartition('.')[0].replace('/', '.'),
                sources=[fpath],
                extra_compile_args=['-std=c++14'],
                optional=True,
                **self._exts_by_fname.get(os.path.basename(fpath), {}),
            )

    def _yield_cy_ext_modules(self) -> ta.Iterator[setuptools.Extension]:
        try:
            import Cython
        except ImportError:
            return

        import Cython.Build
        import Cython.Compiler.Options

        lst = []
        for fpath, e in self._yield_ext_fpaths('cy/**/*.pyx'):
            lst.append(setuptools.Extension(
                fpath.rpartition('.')[0].replace('/', '.'),
                sources=[fpath],
                language='c++',
                extra_compile_args=[
                    '-std=c++14',
                    '-march=native',  # FIXME
                ],
                optional=True,
                define_macros=[
                    *([('CYTHON_TRACE', '1')] if TRACE else []),
                ],
                **(e.kwargs if e is not None else {}),
            ))

        yield from Cython.Build.cythonize(
            lst,
            language_level=3,
            gdb_debug=DEBUG,
            compiler_directives={
                **Cython.Compiler.Options.get_directive_defaults(),
                'linetrace': TRACE,
                'embedsignature': True,
                'binding': True,
            },
        )

    def _yield_m_ext_modules(self) -> ta.Iterator[setuptools.Extension]:
        if not APPLE:
            return

        for fpath, e in self._yield_ext_fpaths('m/*.m'):
            yield setuptools.Extension(
                fpath.rpartition('.')[0].replace('/', '.'),
                sources=[fpath],
                extra_link_args=[
                    '-framework', 'AppKit',
                    '-framework', 'CoreFoundation',
                ],
                optional=True,
                **self._exts_by_fname.get(os.path.basename(fpath), {}),
            )

    # endregion


# endregion


# region Commands


CMDCLASS: ta.MutableMapping[str, ta.Type[distutils.cmd.Command]] = {}


def _cmdclass(name):
    def inner(cls):
        if name in CMDCLASS:
            raise KeyError(name)
        CMDCLASS[name] = cls
        return cls
    return inner


@_cmdclass('cyaml')
class CyamlCommand(distutils.cmd.Command):
    description = 'install cyaml'
    user_options = []

    def run(self):
        self.announce('Installing cyaml')

        import tempfile
        dp = tempfile.mkdtemp()

        import os.path
        fp = os.path.join(dp, 'cyaml.tar.gz')

        import urllib.request
        urllib.request.urlretrieve('https://pyyaml.org/download/pyyaml/PyYAML-5.3.1.tar.gz', fp)

        import hashlib
        sha = hashlib.sha1()
        with open(fp, 'rb') as f:
            sha.update(f.read())
        digest = sha.hexdigest()
        if digest != '3b20272e119990b2bbeb03815a1dd3f3e48af07e':
            raise ValueError(f'Hash cyaml mismatch: {digest}')

        subprocess.check_call(
            f'cd {dp} && '
            f'{os.path.abspath(sys.executable)} -m pip install cyaml.tar.gz --global-option="--with-libyaml"'
        )


# endregion


if __name__ == '__main__':
    setuptools.setup(
        name=ABOUT['__title__'] + (('-' + __dist__) if __dist__ is not None else ''),  # noqa
        version=ABOUT['__version__'],
        description=ABOUT['__description__'],
        author=ABOUT['__author__'],
        url=ABOUT['__url__'],

        distclass=Distribution,
        cmdclass=CMDCLASS,

        python_requires=ABOUT['__python_requires__'],
        classifiers=ABOUT['__classifiers__'],

        setup_requires=['setuptools'],

        py_modules=[PROJECT],

        include_package_data=True,

        entry_points={
            'console_scripts': [
                f'{PROJECT} = {PROJECT}.cli:main',
            ] if __dist__ == 'dev' else [],
        },
    )
