import abc
import types
import typing as ta

from .. import check
from .. import lang
from .types import GenericAlias
from .types import TypeLike


def is_generic(cls: TypeLike) -> bool:
    if isinstance(cls, GenericAlias):
        return True
    elif isinstance(cls, type):
        return issubclass(cls, ta.Generic) and cls.__parameters__  # noqa
    else:
        raise TypeError(cls)


def unerase_generic(cls: TypeLike) -> GenericAlias:
    check.arg(is_generic(cls))
    if isinstance(cls, type):
        return cls.__class_getitem__(cls.__parameters__)
    elif isinstance(cls, GenericAlias):
        return cls
    else:
        raise TypeError(cls)


ROOT_SPECIALS_BY_NAME = {
    s._name: s for a in dir(ta) for s in [getattr(ta, a)] if isinstance(s, GenericAlias) and s._special
}


def get_root_special(cls: GenericAlias) -> GenericAlias:
    if not isinstance(cls, GenericAlias):
        raise TypeError(cls)
    elif cls._special:
        return cls
    else:
        check.state(not issubclass(cls.__origin__, ta.Generic))  # noqa
        # FIXME: https://bugs.python.org/issue32873
        # special = getattr(ta, cls._name)
        special = ROOT_SPECIALS_BY_NAME[cls._name]
        check.isinstance(special, GenericAlias)
        check.state(special is not cls)
        check.state(special._special)
        return special


def is_special_generic(cls: GenericAlias) -> bool:
    if not isinstance(cls, GenericAlias):
        raise TypeError(cls)
    elif not issubclass(cls.__origin__, ta.Generic):  # noqa
        get_root_special(cls)
        return True
    elif cls._special:
        return True
    else:
        return False


def is_new_type(cls: TypeLike) -> bool:
    return isinstance(cls, types.FunctionType) and cls.__code__ is ta.NewType.__code__.co_consts[1]


def generic_bases(cls: TypeLike) -> ta.Sequence[TypeLike]:
    if isinstance(cls, GenericAlias):
        check.state(cls.__origin__ is not cls)
        return generic_bases(cls.__origin__)
    elif not isinstance(cls, type):
        raise TypeError(cls)
    else:
        try:
            bases = cls.__dict__['__orig_bases__']
        except KeyError:
            bases = cls.__bases__
        return [
            (
                (
                    b.__getitem__((ta.Any,) * len(b.__parameters__))
                    if b._special and b.__parameters__ else
                    b
                ) if isinstance(b, GenericAlias) else
                b.__mro_entries__(bases) if hasattr(b, '__mro_entries__') else
                b
            )
            for b in bases
            if b is not ta.Generic and not (
                isinstance(b, GenericAlias) and
                b.__origin__ is ta.Generic
            )
        ]


class _UnionVirtualMeta(type):

    def __subclasscheck__(cls, subclass):
        return isinstance(subclass, GenericAlias) and cls.__origin__ is ta.Union

    def __instancecheck__(cls, instance):
        raise TypeError


class UnionVirtual(metaclass=_UnionVirtualMeta):

    def __new__(cls, *args, **kwargs):
        raise TypeError

    def __init_subclass__(cls, **kwargs):
        raise TypeError


def erase_generic(cls: TypeLike) -> ta.Optional[ta.Type]:
    if isinstance(cls, GenericAlias):
        if cls.__origin__ is ta.Union:
            return UnionVirtual
        else:
            return cls.__origin__
    elif isinstance(cls, type):
        return cls
    else:
        raise TypeError(cls)


def erased_generic_bases(cls: TypeLike) -> ta.Sequence[ta.Type]:
    return list(map(erase_generic, generic_bases(cls)))


def is_abc_dependent(cls: ta.Type) -> bool:
    if not issubclass(type(cls), abc.ABCMeta):
        return False
    else:
        (_abc_registry, _abc_cache, _abc_negative_cache, _abc_negative_cache_version) = abc._get_dump(cls)
        return bool(_abc_registry)


def is_instance_dependent(cls: ta.Type) -> bool:
    return any('__instancecheck__' in type(t).__dict__ for t in cls.__mro__ if type(t) not in (type, abc.ABCMeta))


def is_subclass_dependent(cls: ta.Type) -> bool:
    return any('__subclasscheck__' in type(t).__dict__ for t in cls.__mro__ if type(t) not in (type, abc.ABCMeta))


def is_dependent(cls: ta.Type) -> bool:
    return is_abc_dependent(cls) or is_instance_dependent(cls) or is_subclass_dependent(cls)


def unpack_optional(cls: TypeLike) -> ta.Optional[TypeLike]:
    if (
            is_generic(cls) and
            getattr(cls, '__origin__', None) is ta.Union and
            len(cls.__args__) == 2 and
            type(None) in cls.__args__
    ):
        [arg] = [a for a in fty.__args__ if a is not type(None)]  # noqa
        return arg
    return None


class AnnotationAdapter(lang.Final):

    def __init__(self, annotations: ta.Mapping[str, ta.Any]) -> None:
        super().__init__()
        self.__annotations__ = annotations

    @property
    def annotations(self) -> ta.Mapping[str, ta.Any]:
        return self.__annotations__


def eval_types(
        annotations: ta.Mapping[str, ta.Any],
        globalns: ta.Mapping[str, ta.Any] = None,
        localns: ta.Mapping[str, ta.Any] = None,
) -> ta.Mapping[str, ta.Any]:
    return ta.get_type_hints(
        AnnotationAdapter(annotations),
        globalns=globalns,
        localns=localns
    )


def eval_type(
        annotation: ta.Any,
        globalns: ta.Mapping[str, ta.Any] = None,
        localns: ta.Mapping[str, ta.Any] = None,
) -> ta.Mapping[str, ta.Any]:
    return ta.get_type_hints(
        AnnotationAdapter({'annotation': annotation}),
        globalns=globalns,
        localns=localns
    )['annotation']
