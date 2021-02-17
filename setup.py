#@omnibus
"""
TODO:
 - ** oof, support '.venv/bin/python ../omnibus/setup.py install --force'
 - pyox support w/ exts
 - pipx awareness? all was used for in IW was sysdeps lol
  - https://github.com/indygreg/PyOxidizer/blob/300cde219dbda0cb37dd90822f230b2514ed116b/docs/packaging_extension_modules.rst#building-with-a-custom-distutils
 - test import * (via lang), at least in all+None
 - make_archive hook?
  - .revision
  - replace __dist__ = in build
 - .egg dirs in build/
  - build process = make all sdist first, build off that in build/ ?
 - do something sensible when running setup.py in dev/exp - even if just raise EnvironmentError
  - all can build any, None can build None, others can't build anything
 - codify all this in om.dev.pkg? even if '__dists__' not reusable still hygienic to decouple
  - also gen piecewise py-file, blocked on asts, same machinery for lambduhs etc
 - lint:
  - valid dist name
  - valid nesting
 - fix om/conftest.py
 - reduce makefile usage *without* fsu
  - audit relevant litecli cmd bullshit
 - stick authoritative __dist__ on Distribution? need ref in all hooks
"""
import dataclasses as dc
import functools
import glob
import os.path
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
import traceback
import typing as ta

import setuptools as st
import setuptools.command.build_ext  # noqa
import setuptools.command.build_py  # noqa
import setuptools.command.sdist  # noqa

import distutils as du
import distutils.ccompiler
import distutils.cmd
import distutils.command.build  # noqa
import distutils.command.build_ext  # noqa
import distutils.core
import distutils.errors
import distutils.log
import distutils.sysconfig


PROJECT = 'omnibus'


__dist__ = None


if f'__{PROJECT.upper()}_DIST' in os.environ:
    __dist__ = os.environ[f'__{PROJECT.upper()}_DIST'] or None


# region Dists


@dc.dataclass(frozen=True)
class DistType:
    name: ta.Optional[str]
    deps: ta.Sequence[ta.Optional[str]] = None
    pkg_names: ta.Optional[ta.Collection[str]] = None
    mod_names: ta.Optional[ta.Collection[str]] = None
    included_file_pats: ta.Optional[ta.Sequence[str]] = None
    excluded_file_pats: ta.Optional[ta.Sequence[str]] = None

    @property
    def rname(self) -> str:
        return PROJECT + (('-' + self.name) if self.name is not None else '')


DISTS_BY_NAME: ta.Mapping[ta.Optional[str], DistType] = {d.name: d for d in [
    DistType('all', pkg_names=['tests'], mod_names=['conftest'], included_file_pats=[r'requirements.*\.txt']),
    DistType(None),
    DistType('dev', deps=[None], pkg_names=['dev']),
    DistType('exp', deps=['dev']),
]}

DIST = DISTS_BY_NAME[__dist__]


# endregion


# region Env


def _read_about(fp: ta.Optional[str] = None) -> ta.Mapping[str, ta.Any]:
    if not fp:
        fp = os.path.join(PROJECT, '__about__.py')
    dct = {}
    with open(fp, 'rb') as f:
        src = f.read()
        if sys.version_info[0] > 2:
            src = src.decode('UTF-8')
        exec(src, ta.cast(ta.Dict, dct))
    return dct


DIR = os.path.realpath(os.path.dirname(__file__))


ABOUT = _read_about(os.path.join(DIR, PROJECT, '__about__.py'))


APPLE = sys.platform == 'darwin'


DEBUG = os.environ.get('DEBUG')
TRACE = os.environ.get('TRACE')


# endregion


# region Config


INCLUDED_FILE_PATS: ta.AbstractSet[str] = {
    rf'{PROJECT}/.*',
    'LICENSE.*',
}


EXCLUDED_FILE_NAMES: ta.AbstractSet[str] = {
    '.DS_Store',
    '.gitignore',
    'Makefile',
}


EXCLUDED_FILE_EXTS: ta.AbstractSet[str] = {
    'so',
}


EXCLUDED_FILE_PATS: ta.AbstractSet[str] = {
    *[rf'.*/{re.escape(f)}' for f in EXCLUDED_FILE_NAMES],
    *[rf'.*\.{re.escape(x)}' for x in EXCLUDED_FILE_EXTS],

    r'.*/\.benchmarks/.*',
    r'.*/\.mypy_cache/.*',
    r'.*/\.pytest_cache/.*',
    r'.*/__pycache__/.*',

}


EXTRAS_REQUIRE: ta.Mapping[str, ta.Sequence[str]] = {
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
    def __init__(self, fn, *, name=None, ignore_if=lambda _: False, clear_on_init=False):
        super().__init__()
        if isinstance(fn, property):
            fn = fn.fget
        self._fn = fn
        self._ignore_if = ignore_if
        self._name = name
        self._clear_on_init = clear_on_init

    def __set_name__(self, owner, name):
        if self._name is None:
            self._name = name

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        if self._name is None:
            raise TypeError(self)
        try:
            return instance.__dict__[self._name]
        except KeyError:
            pass
        value = self._fn.__get__(instance, owner)()
        if value is _IGNORE:
            return None
        instance.__dict__[self._name] = value
        return value

    def __set__(self, instance, value):
        if self._ignore_if(value):
            return
        if instance.__dict__[self._name] == value:
            return
        raise TypeError(self._name)


none_ignoring_cached_property = functools.partial(cached_property, ignore_if=lambda v: v is None, clear_on_init=True)
falsey_ignoring_cached_property = functools.partial(cached_property, ignore_if=lambda v: not v, clear_on_init=True)


class cached_nullary:  # noqa
    def __init__(self, fn, *, name=None):
        super().__init__()
        self._fn = fn
        self._name = name
        self._value = _IGNORE

    def __set_name__(self, owner, name):
        if self._name is None:
            self._name = name

    def __get__(self, instance, owner=None):
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

    def __get__(self, instance, owner=None):
        return type(self)(self._wrapper, self._wrapped, instance=instance)

    def __call__(self, *args, **kwargs):
        return self._wrapper(self._wrapped, *([self._instance] if self._instance is not None else []), *args, **kwargs)


def _strip_dir_prefix(pth: str) -> str:
    pth = os.path.realpath(pth)
    pfx = DIR + os.path.sep
    if not pth.startswith(pfx):
        raise ValueError(pth)
    return pth[len(pfx):]


# endregion


# region Extension Utils


def try_compile(
        name: str,
        src: str,
        *,
        errors: ta.Collection[ta.Type[BaseException]] = (
                du.errors.CompileError,
                du.errors.LinkError,
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

        compiler = du.ccompiler.new_compiler()
        du.sysconfig.customize_compiler(compiler)

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
            du.log.debug(traceback.format_exc())
            if name:
                du.log.warn(f'{name} not found')
            return False
        else:
            if name:
                du.log.info(f'{name} found')
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


@_hook(du.command.build_ext.build_ext, 'initialize_options')  # noqa
def _new_build_ext_init_opts(old, self, *args, **kwargs):
    old(self, *args, **kwargs)
    self.parallel = os.cpu_count()


@_hook(st.dist._Distribution, '__init__')  # noqa
def _new_dist_distribution_init(old, self, *args, **kwargs):
    for b in type(self).__mro__:
        for k, v in b.__dict__.items():
            if isinstance(v, cached_property) and v._clear_on_init and v._name in self.__dict__:  # noqa
                del self.__dict__[v._name]  # noqa

    old(self, *args, **kwargs)


def _dump_zip_file(fp: str) -> None:
    import zipfile
    du.log.info(fp)
    with zipfile.ZipFile(fp) as zf:
        for zfe in sorted(zf.namelist()):
            du.log.info(f'  {zfe}')


def _clean_egg_info_dir(ei_cmd):
    ei = ei_cmd.egg_info
    if ei and os.path.isdir(ei):
        if os.path.isfile(os.path.join(ei, 'SOURCES.txt')):
            shutil.rmtree(ei)


_CLEAN_WORK_DIR_OPT = ('clean-work-dir', None, 'cleans working directory before building')

st.command.sdist.sdist.user_options.append(_CLEAN_WORK_DIR_OPT)
st.command.sdist.sdist.clean_work_dir = False


@_hook(st.command.sdist.sdist, 'run')
def _new_sdist_run(old, self):
    if self.clean_work_dir:
        ei_cmd = self.get_finalized_command('egg_info')
        _clean_egg_info_dir(ei_cmd)

    oafs = set(self.archive_files or [])

    old(self)

    for af in self.archive_files:
        if af in oafs or not af.endswith('.zip'):
            continue
        _dump_zip_file(af)


@_hook(st.command.sdist.sdist, 'add_defaults')
def _new_sdist_add_defaults(old, self):
    # Opted for a patch over subclasses as sdist itself has numerous subclasses, and the old-style linkage between them
    # makes trying to override 'properly' even more brittle than this. Oh the joys of python packaging.
    fl = self.filelist
    fl.distribution = self.distribution

    # The least invasive approach seems to be to construct a real manifest on demand. It'd be preferable to call
    # manifest_maker methods directly but the odds of version breakage seem too high.
    out_lines = [f'include {fn}' for fn in self.distribution.package_data[PROJECT]]
    out_lines.extend(self.distribution.manifest_lines)

    tmp_dir = tempfile.mkdtemp()
    out_template = os.path.join(tmp_dir, os.path.basename(self.template))
    with open(out_template, 'w') as f:
        f.write('\n'.join(out_lines))
    self.template = out_template

    @_hook(fl, 'sort')
    def _new_sort(old):
        # manifest_maker puts the manifest in its outputs, but it points to a temp file (and as an abspath). As this
        # script itself doesn't need the file the produced sdist is still self-sufficient.
        for i in range(len(fl.files) - 1, -1, -1):
            if fl.files[i].endswith('/MANIFEST.in'):
                del fl.files[i]

        old()

    old(self)


@_hook(st.command.build_py.build_py, 'find_package_modules')
def _new_build_py_find_package_modules(old, self, package, package_dir):
    modules = old(self, package, package_dir)

    dists_by_mod_name = {}
    for d in DISTS_BY_NAME.values():
        for dn in (d.mod_names or []):
            if dn in dists_by_mod_name:
                raise KeyError(dn)
            dists_by_mod_name[dn] = d.name

    exclude = {m for m, d in dists_by_mod_name.items() if d != __dist__}
    modules = [t for t in modules if t[1] not in exclude]

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
                        du.log.warn(f'Failed to resolve {ep!r} from {ep.dist!r}: {e!r}')
                        continue
                    good_eps.append(ep)
            eps = good_eps
        return eps


try:
    import wheel.bdist_wheel
except ImportError:
    pass
else:
    wheel.bdist_wheel.bdist_wheel.user_options.append(_CLEAN_WORK_DIR_OPT)
    wheel.bdist_wheel.bdist_wheel.clean_work_dir = False

    @_hook(wheel.bdist_wheel.bdist_wheel, 'run')
    def _new_bdist_wheel_run(old, self):
        odfs = set(getattr(self.distribution, 'dist_files', []))

        if self.clean_work_dir and not self.skip_build:
            ei_cmd = self.get_finalized_command('egg_info')
            _clean_egg_info_dir(ei_cmd)

            b_cmd = self.get_finalized_command('build')
            bl = os.path.dirname(b_cmd.build_lib) if b_cmd.build_lib else None
            if bl and os.path.isdir(bl):
                es = list(os.scandir(bl))
                if all(e.is_dir() and any(e.name.startswith(p) for p in ['bdist.', 'lib.', 'temp.']) for e in es):
                    shutil.rmtree(bl)

        old(self)

        for df in getattr(self.distribution, 'dist_files', []):
            if df in odfs:
                continue
            dfn = df[2]
            if not dfn.endswith('.whl'):
                continue

            _dump_zip_file(dfn)


# endregion


# region Main Class


class Distribution(du.core.Distribution):

    @cached_property  # noqa
    @property
    def git_revision(self) -> ta.Optional[str]:
        if not os.path.isdir('.git'):
            return None
        try:
            buf = subprocess.check_output('git config --get remote.origin.url', shell=True)
        except Exception:  # noqa
            return None
        url = (buf or b'').decode('utf-8')
        if not url or url.strip() != ABOUT['__url__']:
            return None
        buf = subprocess.check_output('git describe --match=NeVeRmAtCh --always --abbrev=40 --dirty', shell=True)
        rev = buf.decode('utf-8')
        du.log.info(f'.revision = {rev}')
        return rev

    # region Packages

    @dc.dataclass()
    class PkgNode:
        name: str
        dir_path: str
        full_name: str
        file_names: ta.AbstractSet[str]
        dist: ta.Optional[str] = None
        children: ta.Mapping[str, 'Distribution.PkgNode'] = dc.field(default_factory=dict)

    @cached_property  # noqa
    @property
    def root_pkg_node(self) -> PkgNode:
        dists_by_pkg_name = {}
        for d in DISTS_BY_NAME.values():
            for dn in (d.pkg_names or []):
                if dn in dists_by_pkg_name:
                    raise KeyError(dn)
                dists_by_pkg_name[dn] = d.name

        def rec(
                dir_prefix: str,
                dir_name: str,
                parent_dist: ta.Optional[str] = None,
        ) -> ta.Optional[Distribution.PkgNode]:
            dir_path = os.path.join(dir_prefix, dir_name)

            dns = []
            fns = set()
            for e in os.scandir(os.path.join(DIR, dir_path)):
                if e.is_dir():  # noqa
                    dns.append(e.name)  # noqa
                else:
                    fns.add(e.name)  # noqa

            if '__init__.py' not in fns:
                return None

            dist = parent_dist
            ddist = dists_by_pkg_name.get(dir_name)
            if ddist is not None:
                dist = ddist
            if '__about__.py' in fns:
                abt = _read_about(os.path.join(DIR, dir_path, '__about__.py'))
                abt_dist = abt.get('__dist__')
                if abt_dist is not None:
                    if not isinstance(abt_dist, str) or not abt_dist:
                        raise ValueError(dir_prefix, dir_name, abt_dist)
                    dist = abt_dist

            children = {}
            for dn in dns:
                c = rec(dir_path, dn, dist)
                if c is not None:
                    children[dn] = c

            return Distribution.PkgNode(
                name=dir_name,
                dir_path=dir_path,
                full_name='.'.join([*(dir_prefix.split(os.path.sep) if dir_prefix else []), dir_name]),
                file_names=fns,
                dist=dist,
                children=children,
            )

        return rec('', PROJECT, None)

    @cached_property  # noqa
    @property
    def pkg_nodes(self) -> ta.Sequence[PkgNode]:
        def rec(n):
            lst.append(n)
            for c in n.children.values():
                rec(c)
        lst = []
        rec(self.root_pkg_node)
        return lst

    @cached_property  # noqa
    @property
    def pkg_nodes_by_dir_path(self) -> ta.Mapping[str, PkgNode]:
        return {n.dir_path: n for n in self.pkg_nodes}

    @none_ignoring_cached_property  # noqa
    @property
    def packages(self):
        include = {n.full_name for n in self.pkg_nodes if n.dist == __dist__ or __dist__ == 'all'}
        return st.find_packages(include=sorted(include))

    def get_path_pkg_node(self, path: str) -> ta.Optional[PkgNode]:
        fdps = path.split(os.path.sep)
        for i in range(len(fdps) - 1, -1, -1):
            cp = os.path.sep.join(fdps[:i + 1])
            n = self.pkg_nodes_by_dir_path.get(cp)
            if n is not None:
                return n
        return None

    # endregion

    # region Data

    @falsey_ignoring_cached_property  # noqa
    @property
    def package_data(self) -> ta.Mapping[str, ta.Sequence[str]]:
        afns = {
            _strip_dir_prefix(os.path.join(dp, fn))
            for dp, dns, fns in os.walk(os.path.join(DIR, PROJECT), followlinks=True)
            for fn in fns
        }

        afns.update(e.name for e in os.scandir(DIR) if not e.is_dir())  # noqa

        ips = [re.compile(p) for p in {*INCLUDED_FILE_PATS, *(DIST.included_file_pats or [])}]
        eps = [re.compile(p) for p in {*EXCLUDED_FILE_PATS, *(DIST.excluded_file_pats or [])}]

        ffns = {
            fn for fn in afns
            if any(p.match(fn) is not None for p in ips) and
            all(p.match(fn) is None for p in eps)
        }

        afns = set()
        for fn in ffns:
            n = self.get_path_pkg_node(fn)
            nd = n.dist if n is not None else None
            if nd == __dist__ or __dist__ == 'all':
                afns.add(fn)

        return {PROJECT: sorted(afns)}

    @cached_property  # noqa
    @property
    def manifest_lines(self) -> ta.Sequence[str]:
        return [f'exclude {f}' for e in self._cy_ext_modules for f in e.sources]

    # endregion

    # region Requires

    @falsey_ignoring_cached_property  # noqa
    @property
    def install_requires(self) -> ta.Sequence[str]:
        return [
            *[
                d.rname + '==' + ABOUT['__version__']
                for dn in (DIST.deps or [])
                for d in [DISTS_BY_NAME[dn]]
            ],
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
        if __dist__ not in [None, 'all']:
            return []
        return [
            *self._cc_ext_modules,
            *self._cy_ext_modules,
            *self._m_ext_modules,
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
        for fpath in glob.glob(f'{DIR}/{PROJECT}/_ext/{pat}', recursive=True):
            fpath = _strip_dir_prefix(fpath)
            e = self._exts_by_fname.get(os.path.basename(fpath))
            if e is not None and not e.cond():
                continue
            yield fpath, e

    @cached_property  # noqa
    @property
    def _cc_ext_modules(self) -> ta.Sequence[st.Extension]:
        lst = []
        for fpath, e in self._yield_ext_fpaths('cc/*.cc'):
            lst.append(st.Extension(
                fpath.rpartition('.')[0].replace('/', '.'),
                sources=[fpath],
                extra_compile_args=['-std=c++14'],
                optional=True,
                **self._exts_by_fname.get(os.path.basename(fpath), {}),
            ))
        return lst

    @cached_property  # noqa
    @property
    def _cy_ext_modules(self) -> ta.Sequence[st.Extension]:
        try:
            import Cython
        except ImportError:
            du.log.info('Cython not found, not building cython modules')
            return []

        import Cython.Build
        import Cython.Compiler.Options

        raw = []
        for fpath, e in self._yield_ext_fpaths('cy/**/*.pyx'):
            raw.append(st.Extension(
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

        lst = Cython.Build.cythonize(
            raw,
            language_level=3,
            gdb_debug=DEBUG,
            compiler_directives={
                **Cython.Compiler.Options.get_directive_defaults(),
                'linetrace': TRACE,
                'embedsignature': True,
                'binding': True,
            },
        )

        return lst

    @cached_property  # noqa
    @property
    def _m_ext_modules(self) -> ta.Sequence[st.Extension]:
        if not APPLE:
            return []

        lst = []
        for fpath, e in self._yield_ext_fpaths('m/*.m'):
            lst.append(st.Extension(
                fpath.rpartition('.')[0].replace('/', '.'),
                sources=[fpath],
                extra_link_args=[
                    '-framework', 'AppKit',
                    '-framework', 'CoreFoundation',
                ],
                optional=True,
                **self._exts_by_fname.get(os.path.basename(fpath), {}),
            ))
        return lst

    # endregion


# endregion


# region Commands


CMDCLASS: ta.MutableMapping[str, ta.Type[du.cmd.Command]] = {}


def _cmdclass(name):
    def inner(cls):
        if name in CMDCLASS:
            raise KeyError(name)
        CMDCLASS[name] = cls
        return cls
    return inner


@_cmdclass('cyaml')
class CyamlCommand(du.cmd.Command):
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
    st.setup(
        name=DIST.rname,
        version=ABOUT['__version__'],
        description=ABOUT['__description__'],
        author=ABOUT['__author__'],
        url=ABOUT['__url__'],
        license=ABOUT['__license__'],

        distclass=Distribution,
        cmdclass=CMDCLASS,

        python_requires=ABOUT['__python_requires__'],
        classifiers=ABOUT['__classifiers__'],

        setup_requires=['setuptools'],

        include_package_data=True,

        entry_points={
            'console_scripts': [
                f'{PROJECT} = {PROJECT}.cli:main',
            ] if __dist__ == 'dev' else [],
        },
    )
