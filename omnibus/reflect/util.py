import abc
import sys
import types
import typing as ta

from .. import check
from .. import lang
from .types import BaseGenericAlias
from .types import GenericAlias
from .types import TypeLike


if sys.version_info < (3, 8):
    def get_args(tp):
        if isinstance(tp, GenericAlias):
            return tp.__args__
        return None

    def get_origin(tp):
        if isinstance(tp, GenericAlias):
            return tp.__origin__
        if tp is ta.Generic:
            return ta.Generic
        return None

else:
    get_args = ta.get_args
    get_origin = ta.get_origin


if sys.version_info < (3, 9):
    def get_parameters(tp):
        if isinstance(tp, type) and issubclass(tp, ta.Generic):  # noqa
            return tp.__parameters__  # noqa
        if isinstance(tp, ta._GenericAlias):  # noqa
            return tp.__parameters__  # noqa
        raise TypeError(tp)

else:
    def get_parameters(tp):
        if isinstance(tp, type) and issubclass(tp, ta.Generic):  # noqa
            return tp.__parameters__  # noqa
        if isinstance(tp, ta._GenericAlias):  # noqa
            return tp.__parameters__  # noqa
        if isinstance(tp, ta._SpecialGenericAlias):  # noqa
            return tuple(ta.TypeVar(f'_{i}') for i in range(tp._nparams))  # noqa
        raise TypeError(tp)


def get_special_args(tp):
    return tp.__args__


def is_generic(cls: TypeLike) -> bool:
    if isinstance(cls, GenericAlias):
        return True
    elif isinstance(cls, type):
        return issubclass(cls, ta.Generic) and get_parameters(cls)  # noqa
    else:
        raise TypeError(cls)


def unerase_generic(cls: TypeLike) -> GenericAlias:
    check.arg(is_generic(cls))
    if isinstance(cls, type):
        return cls.__class_getitem__(get_parameters(cls))
    elif isinstance(cls, GenericAlias):
        return cls
    else:
        raise TypeError(cls)


if sys.version_info < (3, 9):
    def _is_special(tp):
        return tp._special

else:
    def _is_special(tp):
        return isinstance(tp, ta._SpecialGenericAlias)  # noqa


ROOT_SPECIALS_BY_NAME = {
    s._name: s for a in dir(ta) for s in [getattr(ta, a)] if isinstance(s, BaseGenericAlias) and _is_special(s)
}


def get_root_special(cls: BaseGenericAlias) -> GenericAlias:
    if not isinstance(cls, BaseGenericAlias):
        raise TypeError(cls)
    elif _is_special(cls):
        return cls
    else:
        check.state(not issubclass(get_origin(cls), ta.Generic))  # noqa
        # FIXME: https://bugs.python.org/issue32873
        # special = getattr(ta, cls._name)
        special = ROOT_SPECIALS_BY_NAME[cls._name]
        check.isinstance(special, BaseGenericAlias)
        check.state(special is not cls)
        check.state(_is_special(special))
        return special


def is_special_generic(cls: BaseGenericAlias) -> bool:
    if not isinstance(cls, BaseGenericAlias):
        raise TypeError(cls)
    elif not issubclass(get_origin(cls), ta.Generic):  # noqa
        get_root_special(cls)
        return True
    elif _is_special(cls):
        return True
    else:
        return False


def is_new_type(cls: TypeLike) -> bool:
    return isinstance(cls, types.FunctionType) and cls.__code__ is ta.NewType.__code__.co_consts[1]


def generic_bases(cls: TypeLike) -> ta.Sequence[TypeLike]:
    if isinstance(cls, GenericAlias):
        check.state(get_origin(cls) is not cls)
        return generic_bases(get_origin(cls))
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
                    b.__getitem__((ta.Any,) * len(get_parameters(b)))
                    if _is_special(b) and get_parameters(b) else
                    b
                ) if isinstance(b, GenericAlias) else
                b.__mro_entries__(bases) if hasattr(b, '__mro_entries__') else
                b
            )
            for b in bases
            if b is not ta.Generic and not (
                isinstance(b, GenericAlias) and
                get_origin(b) is ta.Generic
            )
        ]


class _UnionVirtualMeta(type):

    def __subclasscheck__(cls, subclass):
        return isinstance(subclass, GenericAlias) and get_origin(cls) is ta.Union

    def __instancecheck__(cls, instance):
        raise TypeError


class UnionVirtual(metaclass=_UnionVirtualMeta):

    def __new__(cls, *args, **kwargs):
        raise TypeError

    def __init_subclass__(cls, **kwargs):
        raise TypeError


def erase_generic(cls: TypeLike) -> ta.Optional[ta.Type]:
    if isinstance(cls, GenericAlias):
        if get_origin(cls) is ta.Union:
            return UnionVirtual
        else:
            return get_origin(cls)
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
            get_origin(cls) is ta.Union and
            len(get_special_args(cls)) == 2 and
            type(None) in get_special_args(cls)
    ):
        [arg] = [a for a in get_special_args(cls) if a is not type(None)]  # noqa
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
