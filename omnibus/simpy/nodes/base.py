"""
TODO:
 - terse serde likc iw
 - coercion
"""
import string
import typing as ta

from ... import check
from ... import dataclasses as dc
from ... import nodal


class Annotation(nodal.Annotation):
    pass


class Node(nodal.Nodal['Node', Annotation]):
    pass


_IDENT_START_CHARS: ta.AbstractSet[str] = {*string.ascii_letters, '_'}
_IDENT_CHARS: ta.AbstractSet[str] = {*_IDENT_START_CHARS, *map(str, range(10))}


def check_ident(s: str) -> str:
    check.non_empty_str(s)
    check.in_(s[0], _IDENT_START_CHARS)
    check.empty(set(s) - _IDENT_CHARS)
    return s


class Ident(Node):
    s: str = dc.field(check=check_ident)


class Expr(Node, abstract=True):
    pass


class Stmt(Node, abstract=True):
    pass


class Def(Node, abstract=True):
    pass


class Module(Node):
    defs: ta.Sequence[Def]
