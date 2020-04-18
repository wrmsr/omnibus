"""
TODO:
 - posonly
"""
import dataclasses as dc
import inspect
import typing as ta
import weakref

from .. import check
from .. import lang
from .names import NamespaceBuilder


FULL_ARG_SPECS_BY_FUNC = weakref.WeakKeyDictionary()


def get_full_arg_spec(func: ta.Callable) -> inspect.FullArgSpec:
    try:
        weakref.ref(func)
    except TypeError:
        return inspect.getfullargspec(func)
    else:
        try:
            return FULL_ARG_SPECS_BY_FUNC[func]
        except KeyError:
            fas = FULL_ARG_SPECS_BY_FUNC[func] = inspect.getfullargspec(func)
            return fas


@dc.dataclass(frozen=True)
class ArgSpec:
    args: ta.Sequence[str] = ()
    varargs: str = None
    varkw: str = None
    defaults: ta.Sequence[ta.Any] = ()
    kwonlyargs: ta.Sequence[str] = ()
    kwonlydefaults: ta.Mapping[str, ta.Any] = lang.empty_map()
    annotations: ta.Mapping[str, ta.Any] = lang.empty_map()

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
        anns[n] = ns_builder.put('_' + n + '_type', arg_spec.annotations[n], add=True)
        return ': ' + anns[n]

    args: ta.List[str] = []

    if arg_spec.args:
        nd = len(arg_spec.args) - len(arg_spec.defaults or [])
        args.extend(f"{a}{ann(a)}" for a in arg_spec.args[:nd])
        for a, d in zip(arg_spec.args[nd:], arg_spec.defaults):
            args.append(
                f"{a}{ann(a)}{' = ' if a in arg_spec.annotations else '='}"
                f"{ns_builder.put('_' + a + '_default', d, add=True)}")

    if arg_spec.varargs:
        args.append(f'*{arg_spec.varargs}' + ann(arg_spec.varargs))
    elif arg_spec.kwonlyargs:
        args.append('*')

    for kw, d in zip(arg_spec.kwonlyargs, arg_spec.kwonlydefaults):
        args.append(
            f"{kw}{ann(kw)}{' = ' if kw in arg_spec.annotations else '='}"
            f"{ns_builder.put('_' + kw + '_default', d, add=True)}")

    if arg_spec.varkw:
        args.append(f'**{arg_spec.varkw}' + ann(arg_spec.varkw))

    line = f"({', '.join(args)})"
    if arg_spec.annotations and 'return' in arg_spec.annotations:
        line += f" -> {arg_spec.annotations['return']}"

    return line