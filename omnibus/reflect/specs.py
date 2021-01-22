"""
An imo missing stdlib component for breaking apart and representing python's ever-expanding generic typing machinery in
a more stable and friendly object hierarchy. Frees users from having to deal with notoriously version-volatile typing
impl detail like __args__, __origin__, Generic's __mro_entries__, and such - ideally approximating something stable like
java.lang.reflect.

TODO:
 - 3.8: TypedDict, Literal, Final, Protocol, get_origin, get_args
 - forward refs / sugar for using god dam ta.get_type_hints
 - newtype
 - typingx: Intersect, Dependent, Raises
 - https://github.com/python/typing/issues/213
 - reflect/__init__.py? is this where subtyper lives? or is that dispatch-only? hinting required..
 - 3.9:
  - list[int].__args__ == (int,), should be fine
  - ta.Annotation finally

https://github.com/ilevkivskyi/typing_inspect
"""
import abc
import traceback
import typing as ta
import weakref

from .. import caches
from .. import check
from .. import defs
from .. import lang
from .. import properties
from .types import BaseGenericAlias
from .types import GenericAlias
from .types import NoneType
from .types import TypeLike
from .types import TypeLikes
from .types import Var
from .types import Variance
from .util import erase_generic
from .util import generic_bases
from .util import get_origin
from .util import get_parameters
from .util import get_root_special
from .util import get_special_args
from .util import is_generic
from .util import is_new_type
from .util import is_special_generic
from .util import unerase_generic


T = ta.TypeVar('T')

Specable = ta.NewType('Specable', ta.Any)  # ta.Union[Spec, ta.Type, Var, None]

_NONE_TYPE = type(None)


_DEBUG = False


class SpecVisitor(ta.Generic[T]):

    def visit_spec(self, spec: 'Spec') -> T:
        raise TypeError(spec)

    def visit_placeholder_spec(self, spec: 'PlaceholderSpec') -> T:
        return self.visit_spec(spec)

    def visit_any_spec(self, spec: 'AnySpec') -> T:
        return self.visit_placeholder_spec(spec)

    def visit_var_spec(self, spec: 'VarSpec') -> T:
        return self.visit_placeholder_spec(spec)

    def visit_union_spec(self, spec: 'UnionSpec') -> T:
        return self.visit_spec(spec)

    def visit_any_union_spec(self, spec: 'AnyUnionSpec') -> T:
        return self.visit_spec(spec)

    def visit_new_type_spec(self, spec: 'NewTypeSpec') -> T:
        return self.visit_spec(spec)

    def visit_type_spec(self, spec: 'TypeSpec') -> T:
        return self.visit_spec(spec)

    def visit_non_generic_type_spec(self, spec: 'NonGenericTypeSpec') -> T:
        return self.visit_type_spec(spec)

    def visit_generic_type_spec(self, spec: 'GenericTypeSpec') -> T:
        return self.visit_type_spec(spec)

    def visit_parameterized_generic_type_spec(self, spec: 'ParameterizedGenericTypeSpec') -> T:
        return self.visit_generic_type_spec(spec)

    def visit_explicit_parameterized_generic_type_spec(self, spec: 'ExplicitParameterizedGenericTypeSpec') -> T:
        return self.visit_parameterized_generic_type_spec(spec)

    def visit_special_parameterized_generic_type_spec(self, spec: 'SpecialParameterizedGenericTypeSpec') -> T:
        return self.visit_parameterized_generic_type_spec(spec)

    def visit_variadic_generic_type_spec(self, spec: 'VariadicGenericTypeSpec') -> T:
        return self.visit_generic_type_spec(spec)

    def visit_tuple_type_spec(self, spec: 'TupleTypeSpec') -> T:
        return self.visit_variadic_generic_type_spec(spec)


class Spec(lang.Sealed, lang.Abstract):

    def __init__(self, cls: ta.Any) -> None:
        super().__init__()

        self._raw_cls = ta.cast(Specable, cls)

        if _DEBUG:
            self._cls_repr = repr(cls)
            self._traceback = traceback.extract_stack()

    @property
    def _cls(self) -> Specable:
        return self._raw_cls

    defs.repr('cls')
    defs.hash_eq('cls')
    defs.ne()
    defs.no_order()

    @property
    def cls(self) -> Specable:
        return self._cls

    def __iter__(self) -> ta.Iterator['Spec']:
        yield self

    @properties.cached
    def all_types(self) -> ta.Sequence['TypeSpec']:
        return [s for s in self if isinstance(s, TypeSpec)]

    @abc.abstractmethod
    def accept(self, visitor: SpecVisitor[T]) -> T:
        raise NotImplementedError


class PlaceholderSpec(Spec, lang.Sealed, lang.Abstract):
    pass


class AnySpec(PlaceholderSpec, lang.Final):

    def __init__(self) -> None:
        super().__init__(ta.Any)

    def accept(self, visitor: SpecVisitor[T]) -> T:
        return visitor.visit_any_spec(self)


ANY = AnySpec()


class VarSpec(PlaceholderSpec, lang.Final):

    def __init__(self, cls: Var) -> None:
        super().__init__(cls)

        check.arg(isinstance(cls, Var))

    @properties.cached
    def bound(self) -> ta.Optional[Spec]:
        if self._cls.__bound__ is not None:
            return spec(self._cls.__bound__)
        else:
            return None

    @properties.cached
    def variance(self) -> Variance:
        if self._cls.__covariant__:
            if self.cls.__contravariant__:
                raise TypeError
            return Variance.COVARIANT
        elif self.cls.__contravariant__:
            return Variance.CONTRAVARIANT
        else:
            return Variance.INVARIANT

    def __iter__(self) -> ta.Iterator[Spec]:
        yield from super().__iter__()
        if self.bound is not None:
            yield self.bound

    def accept(self, visitor: SpecVisitor[T]) -> T:
        return visitor.visit_var_spec(self)


class UnionSpec(Spec, lang.Final):

    def __init__(self, cls: GenericAlias) -> None:
        super().__init__(cls)

        check.arg(isinstance(cls, GenericAlias))
        check.arg(get_origin(cls) is ta.Union)

    @properties.cached
    def cls_args(self) -> ta.Sequence[Specable]:
        return get_special_args(self._cls)

    @properties.cached
    def args(self) -> ta.Sequence[Spec]:
        return [spec(a) for a in self.cls_args]

    def __iter__(self) -> ta.Iterator[Spec]:
        yield from super().__iter__()
        for a in self.args:
            yield from a

    def accept(self, visitor: SpecVisitor[T]) -> T:
        return visitor.visit_union_spec(self)

    @properties.cached
    def optional_arg(self) -> ta.Optional[Spec]:
        if len(self.cls_args) == 2 and _NONE_TYPE in self.cls_args:
            return check.single(a for a in self.args if a.cls is not _NONE_TYPE)
        else:
            return None


class AnyUnionSpec(Spec, lang.Final):

    def __init__(self) -> None:
        super().__init__(ta.Union)

    def accept(self, visitor: SpecVisitor[T]) -> T:
        return visitor.visit_any_union_spec(self)


ANY_UNION = AnyUnionSpec()


class NewTypeSpec(Spec, lang.Final):

    def __init__(self, cls: GenericAlias) -> None:
        super().__init__(cls)

        check.arg(is_new_type(cls))

    defs.repr('name', 'cls')

    @property
    def name(self) -> str:
        return self._cls.__name__

    @properties.cached
    def base(self) -> 'Spec':
        return spec(self._cls.__supertype__)

    def accept(self, visitor: SpecVisitor[T]) -> T:
        return visitor.visit_new_type_spec(self)


class TypeSpec(Spec, ta.Generic[T], lang.Sealed, lang.Abstract):

    def __init__(self, cls: TypeLike) -> None:
        super().__init__(cls)

        check.arg(isinstance(cls, get_special_args(TypeLike)))  # type: ignore

    @property
    def cls(self) -> TypeLike:
        return self._cls

    @property
    @abc.abstractmethod
    def erased_cls(self) -> ta.Type:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def erased(self) -> 'TypeSpec':
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def bases_cls(self) -> ta.Sequence[TypeLike]:
        raise NotImplementedError

    @properties.cached
    def bases(self) -> ta.Sequence['TypeSpec']:
        return [type_spec(b) for b in self.bases_cls]

    def __iter__(self) -> ta.Iterator[Spec]:
        yield from super().__iter__()
        for b in self.bases:
            yield from b


class NonGenericTypeSpec(TypeSpec[T], lang.Final):

    def __init__(self, cls: ta.Type[T]) -> None:
        super().__init__(cls)

        check.arg(not is_generic(cls))

    @property
    def cls(self) -> ta.Type[T]:
        return self._cls

    @property
    def erased_cls(self) -> ta.Type[T]:
        return self.cls

    @property
    def erased(self) -> TypeSpec:
        return self

    @property
    def bases_cls(self) -> ta.Sequence[TypeLike]:
        return generic_bases(self.erased_cls)

    def accept(self, visitor: SpecVisitor[T]) -> T:
        return visitor.visit_non_generic_type_spec(self)


OBJECT = NonGenericTypeSpec(object)


class GenericTypeSpec(TypeSpec[T], lang.Sealed, lang.Abstract):

    def __init__(self, cls: BaseGenericAlias) -> None:
        super().__init__(cls)

        check.arg(isinstance(cls, BaseGenericAlias))
        check.arg(get_special_args(cls))  # type: ignore
        check.arg(isinstance(get_origin(cls), type))  # type: ignore

    @property
    def cls(self) -> GenericAlias:
        return self._cls

    @property
    def erased_cls(self) -> ta.Type:
        return get_origin(self.cls)

    @properties.cached
    def erased(self) -> TypeSpec:
        return type_spec(self.erased_cls)

    @property
    def cls_args(self) -> ta.Sequence[Specable]:
        return get_special_args(self.cls)  # type: ignore

    @properties.cached
    def args(self) -> ta.Sequence[Spec]:
        return [spec(c) for c in self.cls_args]

    def __iter__(self) -> ta.Iterator[Spec]:
        yield from super().__iter__()
        for a in self.args:
            yield from a


class ParameterizedGenericTypeSpec(GenericTypeSpec[T], lang.Sealed, lang.Abstract):

    def __init__(self, cls: GenericAlias) -> None:
        super().__init__(cls)

        check.unique(self.cls_parameters)

    def _check_arg_param_lens(self) -> None:
        check.state(len(self.cls_parameters) > 0)
        check.state(len(self.cls_args) == len(self.cls_parameters))

    @property
    def bases_cls(self) -> ta.Sequence[TypeLike]:
        def reify_args(cls: Specable) -> TypeLike:
            if not (isinstance(cls, GenericAlias) and get_special_args(cls)):  # type: ignore
                return cls
            else:
                check.state(get_origin(cls) is not None)  # type: ignore
                args = [self.vars[a].cls if isinstance(a, Var) else a for a in get_special_args(cls)]  # type: ignore
                return get_origin(cls).__class_getitem__(tuple(args))  # type: ignore
        return [reify_args(b) for b in get_origin(self._cls).__orig_bases__ if erase_generic(b) is not ta.Generic]  # type: ignore  # noqa

    @property
    @abc.abstractmethod
    def cls_parameters(self) -> ta.Sequence[Var]:
        raise NotImplementedError

    @properties.cached
    def parameters(self) -> ta.Sequence[VarSpec]:
        return [check.isinstance(spec(p), VarSpec) for p in self.cls_parameters]

    @properties.cached
    def vars(self) -> ta.Mapping[Var, Spec]:
        self._check_arg_param_lens()
        return dict(zip(self.cls_parameters, self.args))


class ExplicitParameterizedGenericTypeSpec(ParameterizedGenericTypeSpec, lang.Final):

    def __init__(self, cls: GenericAlias) -> None:
        super().__init__(cls)

        check.arg(not is_special_generic(cls))
        self._check_arg_param_lens()

    @properties.cached
    def cls_parameters(self) -> ta.Sequence[Var]:
        return get_parameters(self.erased_cls)

    def accept(self, visitor: SpecVisitor[T]) -> T:
        return visitor.visit_explicit_parameterized_generic_type_spec(self)


class SpecialParameterizedGenericTypeSpec(ParameterizedGenericTypeSpec, lang.Final):

    def __init__(self, cls: GenericAlias) -> None:
        check.arg(is_special_generic(cls))
        check.arg(not is_generic(get_origin(cls)))
        check.arg(not hasattr(get_origin(cls), '__orig_bases__'))
        cls_parameters: ta.Sequence[Var] = get_parameters(get_root_special(cls))
        check.arg(all(isinstance(p, Var) for p in cls_parameters))
        self._cls_parameters = cls_parameters

        super().__init__(cls)

    @property
    def cls_parameters(self) -> ta.Sequence[Var]:
        return self._cls_parameters

    @property
    def bases_cls(self) -> ta.Sequence[ta.Type]:
        return self.erased_cls.__bases__

    def accept(self, visitor: SpecVisitor[T]) -> T:
        return visitor.visit_special_parameterized_generic_type_spec(self)


class VariadicGenericTypeSpec(GenericTypeSpec[T], lang.Sealed, lang.Abstract):
    pass


class TupleTypeSpec(VariadicGenericTypeSpec[T], lang.Final):

    def __init__(self, cls: GenericAlias) -> None:
        super().__init__(cls)

        check.arg(get_origin(cls) is tuple)

    @property
    def bases_cls(self) -> ta.Sequence[TypeLike]:
        return [object]

    def accept(self, visitor: SpecVisitor[T]) -> T:
        return visitor.visit_tuple_type_spec(self)


def _spec(cls: Specable) -> Spec:
    if isinstance(cls, Spec):
        return cls
    elif cls is None:
        return spec(NoneType)
    elif cls is ta.Any:
        return ANY
    elif isinstance(cls, Var):
        return VarSpec(cls)
    elif isinstance(cls, BaseGenericAlias):
        if get_origin(cls) is tuple:
            return TupleTypeSpec(cls)
        elif get_origin(cls) is ta.Union:
            return UnionSpec(cls)
        elif is_special_generic(cls):
            return SpecialParameterizedGenericTypeSpec(cls)
        else:
            return ExplicitParameterizedGenericTypeSpec(cls)
    elif is_new_type(cls):
        return NewTypeSpec(cls)
    elif cls is ta.Union:
        return ANY_UNION
    elif not isinstance(cls, type):
        raise TypeError(cls)
    elif is_generic(cls) and get_parameters(cls):
        return spec(cls.__class_getitem__((ta.Any,) * len(get_parameters(cls))))
    else:
        return NonGenericTypeSpec(cls)


@caches.cache(weak_keys=True, weak_values=True)
def _cached_spec(cls: Specable) -> Spec:
    return _spec(cls)


_SPECS_BY_TYPE: ta.MutableMapping[type, Spec] = weakref.WeakKeyDictionary()


def spec(cls: Specable) -> Spec:
    if isinstance(spec, Spec):
        return cls
    if isinstance(cls, type):
        try:
            return _SPECS_BY_TYPE[cls]
        except KeyError:
            ret = _SPECS_BY_TYPE[cls] = _spec(cls)
            return ret
        except TypeError:
            pass
    return _cached_spec(cls)


def type_spec(cls: Specable) -> TypeSpec:
    return check.isinstance(ta.cast(TypeSpec, spec(cls)), TypeSpec)


def get_unerased_type_spec(cls: Specable) -> TypeSpec:
    if isinstance(cls, TypeLikes) and is_generic(cls):
        cls = unerase_generic(cls)
    return type_spec(cls)


def spec_has_placeholders(spec: Spec) -> bool:
    return any(isinstance(s, PlaceholderSpec) for s in spec)


def spec_is_any(spec: Spec) -> bool:
    if isinstance(spec, AnySpec):
        return True
    elif spec == OBJECT:
        return True
    elif isinstance(spec, UnionSpec):
        return any(spec_is_any(a) for a in spec.args)
    else:
        return False
