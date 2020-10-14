import typing as ta

import mypy.errors as me
import mypy.nodes as mn
import mypy.plugin as mp

from .... import collections as col


_HAS_INSTALLED_TYPEIGNOREREGIONPLUGIN_ERROR_HOOK = False  # noqa


def _install_TypeIgnoreRegionPlugin_error_hook(ignored_line_by_file: ta.Mapping[str, ta.AbstractSet[int]]) -> None:  # noqa
    global _HAS_INSTALLED_TYPEIGNOREREGIONPLUGIN_ERROR_HOOK  # noqa
    if _HAS_INSTALLED_TYPEIGNOREREGIONPLUGIN_ERROR_HOOK:
        return

    from mypy.util import is_typeshed_file

    def new_guie(self: me.Errors, file: str) -> None:
        ignored_lines = self.ignored_lines[file]
        if not is_typeshed_file(file) and file not in self.ignored_files:
            if file in ignored_line_by_file:
                ignored = ignored_line_by_file[file]
                for line in set(ignored_lines) & (set(ignored) - self.used_ignored_lines[file]):
                    del ignored_lines[line]
        return old_guie(self, file)

    try:
        old_guie = me.Errors.generate_unused_ignore_errors
        me.Errors.generate_unused_ignore_errors = new_guie
    except Exception:  # noqa
        pass

    _HAS_INSTALLED_TYPEIGNOREREGIONPLUGIN_ERROR_HOOK = True  # noqa


class TypeIgnoreRegionPlugin(mp.Plugin):

    def __init__(self, options: mp.Options) -> None:
        super().__init__(options)

        self._ignored_lines_by_mod: ta.MutableMapping[mn.MypyFile, ta.Set[int]] = col.IdentityKeyDict()
        self._ignored_lines_by_file: ta.MutableMapping[str, ta.Set[int]] = {}

        _install_TypeIgnoreRegionPlugin_error_hook(self._ignored_lines_by_file)

    def set_modules(self, modules: ta.Dict[str, mn.MypyFile]) -> None:
        for mod in modules.values():
            # TODO: use manager.fscache? :/
            with open(mod.path, 'r') as f:
                lines = f.readlines()
            b = False
            for i, l in enumerate(lines):
                if '#' in l:
                    p = l.rpartition('#')[-1].strip()
                    if p == 'begintypeignore':
                        b = True
                    elif p == 'endtypeignore':
                        b = False
                if b:
                    if i not in mod.ignored_lines:
                        mod.ignored_lines[i] = []
                        self._ignored_lines_by_mod.setdefault(mod, set()).add(i)
                        self._ignored_lines_by_file.setdefault(mod.path, set()).add(i)
