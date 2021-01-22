"""
FIXME:
 - 3.9: https://github.com/python/cpython/pull/19719
 - typing.get_args/get_origin equivs for 3.7, deprecate
"""
import enum
import sys
import typing as ta

from .. import lang


NoneType = type(None)
SpecialForm = ta._SpecialForm
GenericAlias = ta._GenericAlias  # type: ignore

if sys.version_info < (3, 9):
    BaseGenericAlias = ta._GenericAlias  # noqa
else:
    BaseGenericAlias = ta._BaseGenericAlias  # noqa

TypeLikes = (ta.Type, BaseGenericAlias)
TypeLike = ta.Union[ta.Type, BaseGenericAlias]  # type: ignore


class Var(lang.NotInstantiable):
    pass


Var.register(ta.TypeVar)


class Variance(enum.Enum):
    INVARIANT = 'INVARIANT'
    COVARIANT = 'COVARIANT'
    CONTRAVARIANT = 'CONTRAVARIANT'
