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

        for k, b in [
            ('abstract', lang.Abstract),
            ('final', lang.Final),
        ]:
            if k not in kwargs:
                continue
            v = kwargs.pop(k)
            if not isinstance(v, bool):
                raise TypeError(v)
            if v is not True:
                raise ValueError(v)
            if v and b not in bases:
                bases += (b,)

        # if Final not in bases and Abstract not in bases:
        #     bases = (*bases, Final)

        if '__box_value_cls__' not in namespace:
            [base_arg] = {
                b.__box_value_cls__
                for b in bases
                if Box in b.__mro__
                and hasattr(b, '__box_value_cls__')
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
            namespace['__box_value_cls__'] = args[0]
        if not isinstance(namespace['__box_value_cls__'], type):
            raise TypeError(namespace['__box_value_cls__'])

        cls = super().__new__(mcls, name, bases, namespace, **kwargs)  # noqa

        if cls.value is not Box.value:  # noqa
            raise lang.FinalException(cls)
        if 'is_valid' in cls.__dict__:
            iv = cls.__dict__['is_valid']
            if not isinstance(iv, (classmethod, staticmethod)):
                raise TypeError(cls, iv)

        return cls


@functools.total_ordering
class Box(lang.Abstract, ta.Generic[T], metaclass=_BoxMeta):
    __box_value_cls__: ta.ClassVar[ta.Type[T]]

    def __init__(self, value: T) -> None:
        super().__init__()
        if not isinstance(value, self.__box_value_cls__):
            raise TypeError(value)
        if not self.is_valid(value):
            raise ValueError(value)
        self._value = value

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self._value!r})'

    def __str__(self) -> str:
        return repr(self)

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
        raise TypeError(self)

    @classmethod
    def is_valid(cls, val: T) -> bool:
        return True

    @property
    def value(self) -> T:
        return self._value

    @classmethod
    def of(cls: BoxT, obj: ta.Union['BoxT', T]) -> BoxT:  # type: ignore
        if isinstance(obj, cls):  # type: ignore  # noqa
            return obj  # type: ignore
        elif isinstance(obj, cls.__box_value_cls__):
            return cls(obj)   # type: ignore  # noqa
        else:
            raise TypeError(obj)

    @classmethod
    def of_optional(cls: BoxT, obj: ta.Union[None, 'BoxT', T]) -> ta.Optional[BoxT]:  # type: ignore
        if obj is None:
            return None
        else:
            return cls.of(obj)
