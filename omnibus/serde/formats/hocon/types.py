import abc
import typing as ta

from .... import dataclasses as dc


T = ta.TypeVar('T')


class Value(dc.Data, ta.Generic[T], frozen=True, sealed=True, abstract=True):
    @abc.abstractproperty
    def value(self) -> T:
        raise NotImplementedError


class CompoundableValue(Value[T], abstract=True, frozen=True):
    pass


class StringValue(CompoundableValue[str], frozen=True, final=True):
    value: str


class NumberValue(Value[str], frozen=True, final=True):
    value: str


class ReferenceValue(CompoundableValue[str], frozen=True, final=True):
    value: str


class CompoundValue(Value[ta.Sequence[CompoundableValue]], frozen=True, final=True):
    value: ta.Sequence[CompoundableValue]


class ObjectValue(Value[ta.Mapping[str, ta.Any]], frozen=True, final=True):
    value: ta.Mapping[str, ta.Any]


class ArrayValue(Value[ta.Sequence[Value]], frozen=True, final=True):
    value: ta.Sequence[Value]
