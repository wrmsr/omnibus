"""
TODO:
 - novirtual for cppclass:
  - monkeypatch in setup.py
  - hot comment? decorator?
"""
import contextlib

import Cython.Compiler.ModuleNode

from .. import lang


@contextlib.contextmanager
def patch_no_virtual_context():
    class CodeProxy(lang.SimpleProxy):
        def put(self, s):
            if s == 'virtual ':
                return
            self.__wrapped__.put(s)

    def generate_cpp_class_definition(self, entry, code):
        return orig_generate_cpp_class_definition(self, entry, CodeProxy(code))

    with lang.setattr_context(
            Cython.Compiler.ModuleNode.ModuleNode,
            'generate_cpp_class_definition',
            generate_cpp_class_definition,
    ) as orig_generate_cpp_class_definition:
        yield
