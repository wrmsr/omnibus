import functools
import importlib
import sys
import types
import typing as ta
import warnings

import pkg_resources

from .lang import cached_nullary


class UnstableWarning(Warning):
    pass


def warn_unstable():
    warnings.warn('unstable', category=UnstableWarning, stacklevel=2)


def lazy_import(name: str, package: str = None) -> ta.Callable[[], ta.Any]:
    return cached_nullary(functools.partial(importlib.import_module, name, package=package))


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
        if module.__file__ is None:
            return

        for file in pkg_resources.resource_listdir(dir, '.'):
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
) -> ta.Iterator[types.ModuleType]:
    for import_path in yield_importable(package_root, recursive=recursive):
        yield __import__(import_path, globals=globals, locals=locals)


def import_all(package_root: str, *, recursive: bool = False) -> None:
    for _ in yield_import_all(package_root, recursive=recursive):
        pass
