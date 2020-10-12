import enum
import typing as ta

from .. import lang


NoneType = type(None)
SpecialForm = ta._SpecialForm
GenericAlias = ta._GenericAlias  # type: ignore
VariadicGenericAlias = ta._VariadicGenericAlias  # type: ignore
TypeLikes = (ta.Type, GenericAlias)
TypeLike = ta.Union[ta.Type, GenericAlias]  # type: ignore


class Var(lang.NotInstantiable):
    pass


Var.register(ta.TypeVar)


class Variance(enum.Enum):
    INVARIANT = 'INVARIANT'
    COVARIANT = 'COVARIANT'
    CONTRAVARIANT = 'CONTRAVARIANT'
