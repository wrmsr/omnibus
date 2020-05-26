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


T = ta.TypeVar('T')

NoneType = type(None)
SpecialForm = ta._SpecialForm
GenericAlias = ta._GenericAlias
VariadicGenericAlias = ta._VariadicGenericAlias
TypeLikes = (ta.Type, GenericAlias)
TypeLike = ta.Union[ta.Type, GenericAlias]


class Var(lang.NotInstantiable):
    pass


Var.register(ta.TypeVar)


Specable = ta.NewType('Specable', ta.Any)  # ta.Union[Spec, ta.Type, Var, None]


def is_generic(cls: TypeLike) -> bool:
def unerase_generic(cls: TypeLike) -> GenericAlias:
def get_root_special(cls: GenericAlias) -> GenericAlias:
def is_special_generic(cls: GenericAlias) -> bool:
def is_new_type(cls: TypeLike) -> bool:
def generic_bases(cls: TypeLike) -> ta.Sequence[TypeLike]:
class UnionVirtualClass(metaclass=_UnionVirtualClassMeta):
def erase_generic(cls: TypeLike) -> ta.Optional[ta.Type]:
def erased_generic_bases(cls: TypeLike) -> ta.Sequence[ta.Type]:
def is_abc_dependent(cls: ta.Type) -> bool:
def is_instance_dependent(cls: ta.Type) -> bool:
def is_subclass_dependent(cls: ta.Type) -> bool:
def is_dependent(cls: ta.Type) -> bool:
class AnnotationAdapter(lang.Final):
def eval_types(
        annotations: ta.Mapping[str, ta.Any],
        globalns: ta.Mapping[str, ta.Any] = None,
        localns: ta.Mapping[str, ta.Any] = None,
) -> ta.Mapping[str, ta.Any]:
def eval_type(
        annotation: ta.Any,
        globalns: ta.Mapping[str, ta.Any] = None,
        localns: ta.Mapping[str, ta.Any] = None,
) -> ta.Mapping[str, ta.Any]:
class GarbageCollectedException(Exception):
class SpecVisitor(ta.Generic[T]):
class Spec(lang.Sealed, lang.Abstract):
class PlaceholderSpec(Spec, lang.Sealed, lang.Abstract):
class AnySpec(PlaceholderSpec, lang.Final):
ANY_SPEC = AnySpec(ta.Any)
class Variance(enum.Enum):
    INVARIANT = 'INVARIANT'
    COVARIANT = 'COVARIANT'
    CONTRAVARIANT = 'CONTRAVARIANT'
class VarSpec(PlaceholderSpec, lang.Final):
class UnionSpec(Spec, lang.Final):
class NewTypeSpec(Spec, lang.Final):
class TypeSpec(Spec, ta.Generic[T], lang.Sealed, lang.Abstract):
class NonGenericTypeSpec(TypeSpec[T], lang.Final):
OBJECT_SPEC = NonGenericTypeSpec(object)
class GenericTypeSpec(TypeSpec[T], lang.Sealed, lang.Abstract):
class ParameterizedGenericTypeSpec(GenericTypeSpec[T], lang.Sealed, lang.Abstract):
class ExplicitParameterizedGenericTypeSpec(ParameterizedGenericTypeSpec, lang.Final):
class SpecialParameterizedGenericTypeSpec(ParameterizedGenericTypeSpec, lang.Final):
class VariadicGenericTypeSpec(GenericTypeSpec[T], lang.Sealed, lang.Abstract):
class TupleTypeSpec(VariadicGenericTypeSpec[T], lang.Final):
def get_spec(cls: Specable) -> Spec:
def get_type_spec(cls: Specable) -> TypeSpec:
def get_unerased_type_spec(cls: Specable) -> TypeSpec:
def spec_has_placeholders(spec: Spec) -> bool:
def spec_is_any(spec: Spec) -> bool:
