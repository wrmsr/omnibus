"""
TODO:
 - posonly
"""
import contextlib
import dataclasses as dc
import inspect
import io
import string
import textwrap
import typing as ta

from omnibus import check


NameGenerator = ta.Callable[..., str]


class NameGeneratorImpl:

    DEFAULT_PREFIX = '_'

    def __init__(
            self,
            *,
            unavailable_names: ta.Iterable[str] = None,
            global_prefix: str = None,
            use_global_prefix_if_present: bool = False,
            add_global_prefix_before_number: bool = False,
    ) -> None:
        super().__init__()

        self._names = set(unavailable_names or [])
        self._global_prefix = global_prefix if global_prefix is not None else self.DEFAULT_PREFIX
        self._use_global_prefix_if_present = bool(use_global_prefix_if_present)
        self._add_global_prefix_before_number = bool(add_global_prefix_before_number)

        self._name_counts: ta.Dict[str, int] = {}

    def __call__(self, prefix: str = '') -> str:
        if self._use_global_prefix_if_present and prefix.startswith(self._global_prefix):
            base_name = prefix
        else:
            base_name = self._global_prefix + prefix

        base_count = -1
        if base_name[-1] in string.digits:
            i = len(base_name) - 2
            while i >= 0 and base_name[i] in string.digits:
                i -= 1
            i += 1
            base_count = int(base_name[i:])
            base_name = base_name[:i]

        if self._add_global_prefix_before_number:
            if not (self._use_global_prefix_if_present and base_name.endswith(self._global_prefix)):
                base_name += self._global_prefix

        if base_count >= 0:
            count = self._name_counts.setdefault(base_name, 0)
            if base_count > count:
                self._name_counts[base_name] = base_count

        while True:
            count = self._name_counts.get(base_name, 0)
            self._name_counts[base_name] = count + 1
            name = base_name + str(count)
            if name not in self._names:
                return name


name_generator = NameGeneratorImpl


class NamespaceBuilder(ta.Mapping[str, ta.Any]):

    def __init__(self, name_generator: NameGenerator = None) -> None:
        super().__init__()

        self._name_generator = check.callable(name_generator) if name_generator is not None else NameGeneratorImpl()

        self._dct = {}

    def __getitem__(self, k: str) -> ta.Any:
        return self._dct[k]

    def __len__(self):
        return len(self._dct)

    def __iter__(self) -> ta.Iterable[str]:
        return iter(self._dct)

    def items(self) -> ta.Iterable[ta.Tuple[str, ta.Any]]:
        return self._dct.items()

    def put(self, *args) -> str:
        if len(args) == 1:
            k, v = self._name_generator(), *args
        elif len(args) == 2:
            k, v = args
        else:
            raise ValueError(args)
        check.isinstance(k, str)
        check.not_in(k, self._dct)
        self._dct[k] = v
        return k


@dc.dataclass(frozen=True)
class ArgSpec:
    args: ta.Sequence[str] = dc.field(default_factory=list)
    varargs: str = None
    varkw: str = None
    defaults: ta.Sequence[ta.Any] = dc.field(default_factory=list)
    kwonlyargs: ta.Sequence[str] = dc.field(default_factory=list)
    kwonlydefaults: ta.Mapping[str, ta.Any] = dc.field(default_factory=dict)
    annotations: ta.Mapping[str, ta.Any] = dc.field(default_factory=dict)

    @classmethod
    def from_inspect(cls, arg_spec: inspect.FullArgSpec) -> 'ArgSpec':
        check.isinstance(arg_spec, inspect.FullArgSpec)
        return cls(
            args=list(arg_spec.args or []),
            varargs=arg_spec.varargs,
            varkw=arg_spec.varkw,
            defaults=list(arg_spec.defaults or []),
            kwonlyargs=list(arg_spec.kwonlyargs or []),
            kwonlydefaults=dict(arg_spec.kwonlydefaults or {}),
            annotations=dict(arg_spec.annotations or {}),
        )


def render_arg_spec(arg_spec: ta.Union[ArgSpec, inspect.FullArgSpec], ns_builder: NamespaceBuilder) -> str:
    if isinstance(arg_spec, inspect.FullArgSpec):
        arg_spec = ArgSpec.from_inspect(arg_spec)
    else:
        check.isinstance(arg_spec, ArgSpec)

    anns = {}

    def ann(n):
        if not arg_spec.annotations or n not in arg_spec.annotations:
            return ''
        anns[n] = ns_builder.put(arg_spec.annotations[n])
        return ': ' + anns[n]

    args: ta.List[str] = []

    if arg_spec.args:
        nd = len(arg_spec.args) - len(arg_spec.defaults or [])
        args.extend(f"{a}{ann(a)}" for a in arg_spec.args[:nd])
        for a in arg_spec.args[nd:]:
            args.append(f"{a}{ann(a)}{' = ' if a in arg_spec.annotations else '='}{ns_builder.put(a)}")

    if arg_spec.varargs:
        args.append(f'*{arg_spec.varargs}' + ann(arg_spec.varargs))
    elif arg_spec.kwonlyargs:
        args.append('*')

    for kw, d in zip(arg_spec.kwonlyargs, arg_spec.kwonlydefaults):
        args.append(f"{kw}{ann(kw)}{' = ' if kw in arg_spec.annotations else '='}{ns_builder.put(d)}")

    if arg_spec.varkw:
        args.append(f'**{arg_spec.varkw}' + ann(arg_spec.varkw))

    line = f"{', '.join(args)})"
    if arg_spec.annotations and 'return' in arg_spec.annotations:
        line += f" -> {arg_spec.annotations['return']}"

    return line


class Codegen:

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

    def __call__(self, s: str) -> None:
        i = self._indent * self._level
        s = '\n'.join([(i + l) if l else '' for l in textwrap.dedent(s).split('\n')])
        self._buf.write(s)

    def __str__(self) -> str:
        return self._buf.getvalue()
