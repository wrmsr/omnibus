import typing as ta

from .. import check
from .. import defs
from .. import lang
from .. import properties


class Value(lang.Abstract):

    defs.repr()

    stream = properties.set_once()


class Unknown(Value, lang.Final):
    pass


class Const(Value, lang.Final):

    def __init__(self, value: ta.Any) -> None:
        super().__init__()

        self._value = value

    defs.repr('value')

    @property
    def value(self) -> ta.Any:
        return self._value


class NamedValue(Value, lang.Abstract):

    def __init__(self, name: str) -> None:
        super().__init__()

        self._name = check.non_empty_str(name)

    defs.repr('name')

    @property
    def name(self) -> str:
        return self._name


class Global(NamedValue, lang.Final):
    pass


class Local(NamedValue, lang.Final):
    pass


class Name(NamedValue, lang.Final):
    pass


class InstanceValue(Value, lang.Abstract):

    def __init__(self, object: Value, name: str) -> None:
        super().__init__()

        self._object = object
        self._name = check.non_empty_str(name)

    defs.repr('object', 'name')

    @property
    def object(self) -> Value:
        return self._object

    @property
    def name(self) -> str:
        return self._name


class Attr(InstanceValue, lang.Final):
    pass


class MethodInstance(InstanceValue, lang.Final):
    pass


class MethodCallable(InstanceValue, lang.Final):
    pass


class SyntheticValue(Value, lang.Abstract):
    pass


class Call(SyntheticValue):

    def __init__(self, fn: Value, args: ta.Sequence[Value]) -> None:
        super().__init__()

        self._fn = fn
        self._args = args

    defs.repr('fn', 'args')

    @property
    def fn(self) -> Value:
        return self._fn

    @property
    def args(self) -> ta.Sequence[Value]:
        return self._args


class BinaryOp(SyntheticValue):

    def __init__(self, left: Value, op: str, right: Value) -> None:
        super().__init__()

        self._left = left
        self._op = op
        self._right = right

    defs.repr('left', 'op', 'right')

    @property
    def left(self) -> Value:
        return self._left

    @property
    def op(self) -> str:
        return self._op

    @property
    def right(self) -> Value:
        return self._right


def render(val: Value) -> str:
    if isinstance(val, Const):
        return repr(val.value)

    elif isinstance(val, NamedValue):
        return val.name

    elif isinstance(val, Attr):
        return f'{render(val.object)}.{val.name}'

    elif isinstance(val, Call):
        return f'{render(val.fn)}({", ".join(map(render, val.args))})'

    elif isinstance(val, BinaryOp):
        return f'({render(val.left)} {val.op} {render(val.right)})'

    # elif isinstance(val, UnaryOp):
    #     return f'{val.op}{render(val.value)}'

    else:
        raise TypeError(val)
