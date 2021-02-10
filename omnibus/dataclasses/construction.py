import dataclasses as dc
import typing as ta

from .. import code
from .. import lang


@dc.dataclass(frozen=True)
class Spec:
    attrs: 'Attr'


class Action(lang.Abstract):
    pass


@dc.dataclass(frozen=True)
class Attr(Action):
    name: str
    value: 'Value'


class Value(lang.Abstract):
    pass


@dc.dataclass(frozen=True)
class Code(Value):
    name: str
    arg_spec: code.ArgSpec
    body: str
    locals: ta.Mapping[str, Value]


@dc.dataclass(frozen=True)
class ClassParam(Value):
    name: str


@dc.dataclass(frozen=True)
class FieldParam(Value):
    field: str
    name: str
