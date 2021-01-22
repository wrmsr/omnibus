import abc
import functools
import sys
import typing as ta

from .. import lang


T = ta.TypeVar('T')

BoxT = ta.TypeVar('BoxT', bound='Box')


if sys.version_info < (3, 8):
    def _get_tp_args(tp):
        return getattr(tp, '__args__', None)

    def _get_tp_origin(tp):
        return getattr(tp, '__origin__', None)

else:
    _get_tp_args = ta.get_args
    _get_tp_origin = ta.get_origin


class _BoxMeta(abc.ABCMeta):

    def __new__(mcls, name, bases, namespace, **kwargs):
        if 'Box' not in globals():
            return super().__new__(mcls, name, bases, namespace, **kwargs)  # noqa

        # if Final not in bases and Abstract not in bases:
        #     bases = (*bases, Final)

        if '_value_cls' not in namespace:
            [base_arg] = {
                b._value_cls
                for b in bases
                if Box in b.__mro__
                and hasattr(b, '_value_cls')
            } or [None]
            [box_arg] = [
                a
                for b in namespace.get('__orig_bases__', [])
                if isinstance(b, ta._GenericAlias)  # noqa
                and _get_tp_origin(b) is Box
                for a in _get_tp_args(b)
            ] or [None]
            args = list(filter(None, [base_arg, box_arg]))
            if not args or not all(a is args[0] for a in args[1:]):
                raise TypeError(args)
            namespace['_value_cls'] = args[0]
        if not isinstance(namespace['_value_cls'], type):
            raise TypeError(namespace['_value_cls'])

        cls = super().__new__(mcls, name, bases, namespace, **kwargs)  # noqa
        if cls.value is not Box.value:
            raise lang.FinalException(cls)
        return cls


@functools.total_ordering
class Box(lang.Abstract, ta.Generic[T], metaclass=_BoxMeta):
    _value_cls: ta.ClassVar[ta.Type[T]]

    def __init__(self, value: T) -> None:
        super().__init__()
        if not isinstance(value, self._value_cls):
            raise TypeError(value)
        self._value = value

    def repr(self) -> str:
        return f'{self.__class__.__name__}({self._value!r})'

    def __hash__(self) -> int:
        return hash(self._value)

    def __eq__(self, other: ta.Any) -> bool:
        if not isinstance(other, type(self)):
            raise TypeError(other)
        return self._value == other._value

    def __lt__(self, other: ta.Any) -> bool:
        if not isinstance(other, type(self)):
            raise TypeError(other)
        return self._value < other._value  # type: ignore

    def __bool__(self) -> bool:
        return bool(self._value)

    @property
    def value(self) -> T:
        return self._value

    @classmethod
    def of(cls: BoxT, obj: ta.Union['BoxT', T]) -> BoxT:  # type: ignore
        if isinstance(obj, cls):  # type: ignore  # noqa
            return obj  # type: ignore
        elif isinstance(obj, cls._value_cls):
            return cls(obj)   # type: ignore  # noqa
        else:
            raise TypeError(obj)

    @classmethod
    def of_optional(cls: BoxT, obj: ta.Union[None, 'BoxT', T]) -> ta.Optional[BoxT]:  # type: ignore
        if obj is None:
            return None
        else:
            return cls.of(obj)
