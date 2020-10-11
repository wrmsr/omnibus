"""
TODO:
 - pkgutil.walk_packages?
 - importutil._util._LazyModule
"""
import functools
import importlib
import sys
import types
import typing as ta
import warnings

from .functions import cached_nullary
from .functions import staticfunction


class UnstableWarning(Warning):
    pass


def warn_unstable() -> None:
    warnings.warn(f'{__package__.split(".")[0]} module is marked as unstable', category=UnstableWarning, stacklevel=2)


def ignore_unstable_warn() -> None:
    warnings.filterwarnings('ignore', category=UnstableWarning)


def lazy_import(name: str, package: str = None) -> ta.Callable[[], ta.Any]:
    return staticfunction(cached_nullary(functools.partial(importlib.import_module, name, package=package)))  # noqa


def proxy_import(name: str, package: str = None) -> types.ModuleType:
    def __getattr__(att):
        nonlocal omod
        if omod is None:
            omod = importlib.import_module(name, package=package)
        return getattr(omod, att)
    omod = None
    lmod = types.ModuleType(name)
    lmod.__getattr__ = __getattr__  # type: ignore
    return lmod


_pkg_resources = lazy_import('pkg_resources')


def import_module(dotted_path: str) -> types.ModuleType:
    if not dotted_path:
        raise ImportError(dotted_path)
    mod = __import__(dotted_path, globals(), locals(), [])
    for name in dotted_path.split('.')[1:]:
        try:
            mod = getattr(mod, name)
        except AttributeError:
            raise AttributeError('Module %r has no attribute %r' % (mod, name))
    return mod


def import_module_attr(dotted_path: str) -> ta.Any:
    module_name, _, class_name = dotted_path.rpartition('.')
    mod = import_module(module_name)
    try:
        return getattr(mod, class_name)
    except AttributeError:
        raise AttributeError('Module %r has no attr %r' % (module_name, class_name))


def yield_importable(package_root: str, *, recursive: bool = False) -> ta.Iterator[str]:
    def rec(dir):
        if dir.split('.')[-1] == '__pycache__':
            return

        try:
            module = sys.modules[dir]
        except KeyError:
            try:
                __import__(dir)
            except ImportError:
                return
            module = sys.modules[dir]
        # FIXME: pyox
        if getattr(module, '__file__', None) is None:
            return

        for file in _pkg_resources().resource_listdir(dir, '.'):
            if file.endswith('.py') and not file.startswith('_'):
                yield dir + '.' + file[:-3]
            elif recursive and '.' not in file:
                try:
                    yield from rec(dir + '.' + file)
                except (ImportError, NotImplementedError):
                    pass

    yield from rec(package_root)


def yield_import_all(
        package_root: str,
        *,
        globals: ta.Dict[str, ta.Any] = None,
        locals: ta.Dict[str, ta.Any] = None,
        recursive: bool = False,
) -> ta.Iterator[str]:
    for import_path in yield_importable(package_root, recursive=recursive):
        __import__(import_path, globals=globals, locals=locals)
        yield import_path


def import_all(package_root: str, *, recursive: bool = False) -> None:
    for _ in yield_import_all(package_root, recursive=recursive):
        pass
