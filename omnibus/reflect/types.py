import enum
import typing as ta

from .. import lang


NoneType = type(None)
SpecialForm = ta._SpecialForm
GenericAlias = ta._GenericAlias
VariadicGenericAlias = ta._VariadicGenericAlias
TypeLikes = (ta.Type, GenericAlias)
TypeLike = ta.Union[ta.Type, GenericAlias]


class Var(lang.NotInstantiable):
    pass


Var.register(ta.TypeVar)


class Variance(enum.Enum):
    INVARIANT = 'INVARIANT'
    COVARIANT = 'COVARIANT'
    CONTRAVARIANT = 'CONTRAVARIANT'
