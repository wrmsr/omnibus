import abc
import enum
import types
import typing as ta
import weakref

from .. import caches
from .. import check
from .. import defs
from .. import lang
from .. import properties


NoneType = type(None)
SpecialForm = ta._SpecialForm
GenericAlias = ta._GenericAlias
VariadicGenericAlias = ta._VariadicGenericAlias
TypeLikes = (ta.Type, GenericAlias)
TypeLike = ta.Union[ta.Type, GenericAlias]


class Var(lang.NotInstantiable):
    pass


Var.register(ta.TypeVar)


