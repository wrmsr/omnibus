"""
TODO:
 - posonly
"""
import contextlib
import io
import linecache
import textwrap
import types
import typing as ta
import uuid

from .. import check
from .argspecs import ArgSpec
from .argspecs import render_arg_spec
from .names import NamespaceBuilder


class IndentWriter:

    DEFAULT_INDENT = ' ' * 4

    def __init__(
            self,
            *,
            buf: io.StringIO = None,
            indent: str = None,
    ) -> None:
        super().__init__()

        self._buf = buf if buf is not None else io.StringIO()
        self._indent = check.isinstance(indent, str) if indent is not None else self.DEFAULT_INDENT
        self._level = 0

    @contextlib.contextmanager
    def indent(self, num: int = 1) -> ta.Generator[None, None, None]:
        self._level += num
        try:
            yield
        finally:
            self._level -= num

    def write(self, s: str) -> None:
        i = self._indent * self._level
        s = '\n'.join([(i + l) if l else '' for l in textwrap.dedent(s).split('\n')])
        self._buf.write(s)

    def getvalue(self) -> str:
        return self._buf.getvalue()


def reserve_filename(prefix: str) -> str:
    unique_id = uuid.uuid4()
    count = 0
    while True:
        unique_filename = f'<generated:{prefix}:{count}>'
        cache_line = (1, None, (str(unique_id),), unique_filename)
        if linecache.cache.setdefault(unique_filename, cache_line) == cache_line:
            return unique_filename
        count += 1


def create_fn(
        name: str,
        arg_spec: ArgSpec,
        body: str,
        *,
        globals: ta.Mapping[str, ta.Any] = None,
        locals: ta.Mapping[str, ta.Any] = None,
) -> types.FunctionType:
    check.isinstance(body, str)
    locals = dict(locals or {})

    nsb = NamespaceBuilder(unavailable_names=set(locals) | set(globals or []))
    sig = render_arg_spec(arg_spec, nsb)
    for k, v in nsb.items():
        check.not_in(k, locals)
        locals[k] = v

    body = textwrap.indent(textwrap.dedent(body.strip()), '  ')
    txt = f'def {name}{sig}:\n{body}'
    local_vars = ', '.join(locals.keys())
    exectxt = f'def __create_fn__({local_vars}):\n{textwrap.indent(txt, "  ")}\n  return {name}'

    ns = {}
    filename = reserve_filename(name)
    bytecode = compile(exectxt, filename, 'exec')
    eval(bytecode, globals, ns)

    fn = ns['__create_fn__'](**locals)
    fn.__source__ = txt
    linecache.cache[filename] = (len(exectxt), None, exectxt.splitlines(True), filename)
    return fn
