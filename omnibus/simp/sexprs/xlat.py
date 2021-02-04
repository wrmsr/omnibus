import typing as ta

from .. import nodes as no
from ... import check
from .macros import DEFAULT_MACROS
from .macros import DynamicMacro
from .macros import NamedMacro
from .types import Macro


def c(o: ta.Any) -> no.Node:
    return no.Const(o)


class Xlator:

    def __init__(self, macros: ta.Iterable[Macro]) -> None:
        super().__init__()

        self._macros = list(macros)

        dynamic_macros: ta.List[DynamicMacro] = []
        named_macros: ta.Dict[str, NamedMacro] = {}
        default_macro: ta.Optional[DynamicMacro] = None
        for m in self._macros:
            if isinstance(m, DynamicMacro):
                if m.match is True:
                    default_macro = check.replacing_none(default_macro, m)
                else:
                    dynamic_macros.append(m)
            elif isinstance(m, NamedMacro):
                check.not_in(m.name, named_macros)
                named_macros[m.name] = m
            else:
                raise TypeError(m)

        self._dynamic_macros: ta.Sequence[DynamicMacro] = dynamic_macros
        self._named_macros: ta.Mapping[str, NamedMacro] = named_macros
        self._default_macro = default_macro

    def __call__(self, obj: ta.Any) -> no.Node:
        if isinstance(obj, no.Node):
            return obj

        if isinstance(obj, (int, float)):
            return no.Const(obj)

        if isinstance(obj, str):
            if obj and obj[0] == '~':
                return no.Const(obj[1:])
            else:
                return no.GetVar(no.Ident(obj))

        if isinstance(obj, list):
            args = list(obj)

            dm = None
            for cdm in self._dynamic_macros:
                if cdm.match(args):
                    dm = check.replacing_none(dm, cdm)
            if dm is not None:
                return dm(self, args)

            if args and isinstance(args[0], str) and args[0]:
                try:
                    nm = self._named_macros[args[0]]
                except KeyError:
                    pass
                else:
                    return nm(self, args[1:])

            if self._default_macro:
                return self._default_macro(self, args)
            else:
                raise ValueError(args)

        raise TypeError(obj)


DEFAULT_XLATOR = Xlator(DEFAULT_MACROS)


def xlat(obj: ta.Any) -> no.Node:
    return DEFAULT_XLATOR(obj)
