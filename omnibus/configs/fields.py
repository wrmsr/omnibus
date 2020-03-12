import abc
import typing as ta

from .. import check
from .. import defs
from .. import lang


T = ta.TypeVar('T')


class NOT_SET(lang.Marker):
    pass


class FieldMetadata(lang.Final, ta.Generic[T]):

    def __init__(
            self,
            name: str,
            type: type = NOT_SET,
            *,
            default: ta.Any = NOT_SET,
            doc: str = None,
    ) -> None:
        super().__init__()

        self._name = check.not_empty(check.isinstance(name, str))
        self._type = type
        self._default = default
        self._doc = doc

    defs.repr('name', 'type', 'default')

    @property
    def name(self) -> str:
        return self._name

    @property
    def type(self) -> type:
        return self._type

    @property
    def default(self) -> ta.Any:
        return self._default

    @property
    def doc(self) -> ta.Optional[str]:
        return self._doc


class FieldKwargs(lang.Final):

    def __init__(self, **kwargs) -> None:
        super().__init__()

        self._kwargs = kwargs


def field(
        default: ta.Any = NOT_SET,
        type: type = NOT_SET,
        *,
        doc: str = None,
):
    return FieldKwargs(
        default=default,
        type=type,
        doc=doc,
    )


class FieldSource(lang.Abstract):

    @abc.abstractmethod
    def get(self, field: FieldMetadata) -> ta.Any:
        raise NotImplementedError


class CompositeFieldSource(FieldSource):

    def __init__(self, *children: FieldSource) -> None:
        super().__init__()

        self._children = children

    def get(self, field: FieldMetadata) -> ta.Any:
        for child in self._children:
            value = child.get(field)
            if value is not NOT_SET:
                return value
        return NOT_SET


class DictFieldSource(FieldSource):

    def __init__(self, dct: ta.Mapping[str, ta.Any]) -> None:
        super().__init__()

        self._dct = check.not_none(dct)

    def get(self, field: FieldMetadata) -> ta.Any:
        return self._dct.get(field.name, NOT_SET)
