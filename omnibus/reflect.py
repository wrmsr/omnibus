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

https://github.com/ilevkivskyi/typing_inspect
"""
import abc
import enum
import types
import typing as ta
import weakref

from . import caches
from . import check
from . import defs
from . import lang
from . import properties


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
    if isinstance(cls, GenericAlias):
        return True
    elif isinstance(cls, type):
        return issubclass(cls, ta.Generic) and cls.__parameters__
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
        check.state(not issubclass(cls.__origin__, ta.Generic))
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
    elif not issubclass(cls.__origin__, ta.Generic):
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


class _UnionVirtualClassMeta(type):

    def __subclasscheck__(cls, subclass):
        return isinstance(subclass, GenericAlias) and cls.__origin__ is ta.Union

    def __instancecheck__(cls, instance):
        raise TypeError


class UnionVirtualClass(metaclass=_UnionVirtualClassMeta):

    def __new__(cls, *args, **kwargs):
        raise TypeError

    def __init_subclass__(cls, **kwargs):
        raise TypeError


def erase_generic(cls: TypeLike) -> ta.Optional[ta.Type]:
    if isinstance(cls, GenericAlias):
        if cls.__origin__ is ta.Union:
            return UnionVirtualClass
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


class GarbageCollectedException(Exception):
    pass


class SpecVisitor(ta.Generic[T]):

    def visit_spec(self, spec: 'Spec') -> T:
        raise TypeError

    def visit_placeholder_spec(self, spec: 'PlaceholderSpec') -> T:
        return self.visit_spec(spec)

    def visit_any_spec(self, spec: 'AnySpec') -> T:
        return self.visit_placeholder_spec(spec)

    def visit_var_spec(self, spec: 'VarSpec') -> T:
        return self.visit_placeholder_spec(spec)

    def visit_union_spec(self, spec: 'UnionSpec') -> T:
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

    def __init__(self, cls: Specable) -> None:
        super().__init__()

        self._cls_ref = weakref.ref(cls)

    @property
    def _cls(self) -> Specable:
        cls = self._cls_ref()
        if cls is None:
            raise GarbageCollectedException
        return cls

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

    def __init__(self, cls: SpecialForm) -> None:
        super().__init__(cls)

        check.arg(cls is ta.Any)

    def accept(self, visitor: SpecVisitor[T]) -> T:
        return visitor.visit_any_spec(self)


ANY_SPEC = AnySpec(ta.Any)


class Variance(enum.Enum):
    INVARIANT = 'INVARIANT'
    COVARIANT = 'COVARIANT'
    CONTRAVARIANT = 'CONTRAVARIANT'


class VarSpec(PlaceholderSpec, lang.Final):

    def __init__(self, cls: Var) -> None:
        super().__init__(cls)

        check.arg(isinstance(cls, Var))

    @properties.cached
    def bound(self) -> ta.Optional[Spec]:
        if self._cls.__bound__ is not None:
            return get_spec(self._cls.__bound__)
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
        check.arg(cls.__origin__ is ta.Union)

    @properties.cached
    def args_cls(self) -> ta.Sequence[Specable]:
        return self._cls.__args__

    @properties.cached
    def args(self) -> ta.Sequence[Spec]:
        return [get_spec(a) for a in self.args_cls]

    def __iter__(self) -> ta.Iterator[Spec]:
        yield from super().__iter__()
        for a in self.args:
            yield from a

    def accept(self, visitor: SpecVisitor[T]) -> T:
        return visitor.visit_union_spec(self)


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
        return get_spec(self._cls.__supertype__)

    def accept(self, visitor: SpecVisitor[T]) -> T:
        return visitor.visit_new_type_spec(self)


class TypeSpec(Spec, ta.Generic[T], lang.Sealed, lang.Abstract):

    def __init__(self, cls: TypeLike) -> None:
        super().__init__(cls)

        check.arg(isinstance(cls, TypeLike.__args__))

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
        return [get_type_spec(b) for b in self.bases_cls]

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


OBJECT_SPEC = NonGenericTypeSpec(object)


class GenericTypeSpec(TypeSpec[T], lang.Sealed, lang.Abstract):

    def __init__(self, cls: GenericAlias) -> None:
        super().__init__(cls)

        check.arg(isinstance(cls, GenericAlias))
        check.arg(not isinstance(cls, VariadicGenericAlias))
        check.arg(cls.__args__)
        check.arg(isinstance(cls.__origin__, type))

    @property
    def cls(self) -> GenericAlias:
        return self._cls

    @property
    def erased_cls(self) -> ta.Type:
        return self.cls.__origin__

    @properties.cached
    def erased(self) -> TypeSpec:
        return get_type_spec(self.erased_cls)

    @property
    def args_cls(self) -> ta.Sequence[Specable]:
        return self.cls.__args__

    @properties.cached
    def args(self) -> ta.Sequence[Spec]:
        return [get_spec(c) for c in self.args_cls]

    def __iter__(self) -> ta.Iterator[Spec]:
        yield from super().__iter__()
        for a in self.args:
            yield from a


class ParameterizedGenericTypeSpec(GenericTypeSpec[T], lang.Sealed, lang.Abstract):

    def __init__(self, cls: GenericAlias) -> None:
        super().__init__(cls)

        check.unique(self.parameters_cls)

    def _check_arg_param_lens(self) -> None:
        check.state(len(self.parameters_cls) > 0)
        check.state(len(self.args_cls) == len(self.parameters_cls))

    @property
    def bases_cls(self) -> ta.Sequence[TypeLike]:
        def reify_args(cls: Specable) -> TypeLike:
            if not (isinstance(cls, GenericAlias) and cls.__args__):
                return cls
            else:
                check.state(cls.__origin__ is not None)
                args = [self.vars[a].cls if isinstance(a, Var) else a for a in cls.__args__]
                return cls.__origin__.__class_getitem__(tuple(args))
        return [reify_args(b) for b in self._cls.__origin__.__orig_bases__ if erase_generic(b) is not ta.Generic]

    @property
    @abc.abstractmethod
    def parameters_cls(self) -> ta.Sequence[Var]:
        raise NotImplementedError

    @properties.cached
    def parameters(self) -> ta.Sequence[VarSpec]:
        return [check.isinstance(get_spec(p), VarSpec) for p in self.parameters_cls]

    @properties.cached
    def vars(self) -> ta.Mapping[Var, Spec]:
        self._check_arg_param_lens()
        return dict(zip(self.parameters_cls, self.args))


class ExplicitParameterizedGenericTypeSpec(ParameterizedGenericTypeSpec, lang.Final):

    def __init__(self, cls: GenericAlias) -> None:
        super().__init__(cls)

        check.arg(not is_special_generic(cls))
        self._check_arg_param_lens()

    @properties.cached
    def parameters_cls(self) -> ta.Sequence[Var]:
        return self.erased_cls.__parameters__

    def accept(self, visitor: SpecVisitor[T]) -> T:
        return visitor.visit_explicit_parameterized_generic_type_spec(self)


class SpecialParameterizedGenericTypeSpec(ParameterizedGenericTypeSpec, lang.Final):

    def __init__(self, cls: GenericAlias) -> None:
        check.arg(is_special_generic(cls))
        check.arg(not is_generic(cls.__origin__))
        check.arg(not hasattr(cls.__origin__, '__orig_bases__'))
        parameters_cls: ta.Sequence[Var] = get_root_special(cls).__parameters__
        check.arg(all(isinstance(p, Var) for p in parameters_cls))
        self._parameters_cls = parameters_cls

        super().__init__(cls)

    @property
    def parameters_cls(self) -> ta.Sequence[Var]:
        return self._parameters_cls

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

        check.arg(cls.__origin__ is tuple)

    @property
    def bases_cls(self) -> ta.Sequence[TypeLike]:
        return [object]

    def accept(self, visitor: SpecVisitor[T]) -> T:
        return visitor.visit_tuple_type_spec(self)


def _get_spec(cls: Specable) -> Spec:
    if isinstance(cls, Spec):
        return cls
    elif cls is None:
        return get_spec(NoneType)
    elif cls is ta.Any:
        return ANY_SPEC
    elif isinstance(cls, Var):
        return VarSpec(cls)
    elif isinstance(cls, VariadicGenericAlias):
        raise TypeError(cls)
    elif isinstance(cls, GenericAlias):
        if cls.__origin__ is tuple:
            return TupleTypeSpec(cls)
        elif cls.__origin__ is ta.Union:
            return UnionSpec(cls)
        elif is_special_generic(cls):
            return SpecialParameterizedGenericTypeSpec(cls)
        else:
            return ExplicitParameterizedGenericTypeSpec(cls)
    elif is_new_type(cls):
        return NewTypeSpec(cls)
    elif not isinstance(cls, type):
        raise TypeError(cls)
    elif is_generic(cls) and cls.__parameters__:
        return get_spec(cls.__class_getitem__((ta.Any,) * len(cls.__parameters__)))
    else:
        return NonGenericTypeSpec(cls)


@caches.cache(weak_keys=True)
def get_spec(cls: Specable) -> Spec:
    return _get_spec(cls)


def get_type_spec(cls: Specable) -> TypeSpec:
    return check.isinstance(ta.cast(TypeSpec, get_spec(cls)), TypeSpec)


def get_unerased_type_spec(cls: Specable) -> TypeSpec:
    if isinstance(cls, TypeLikes) and is_generic(cls):
        cls = unerase_generic(cls)
    return get_type_spec(cls)


def spec_has_placeholders(spec: Spec) -> bool:
    return any(isinstance(s, PlaceholderSpec) for s in spec)


def spec_is_any(spec: Spec) -> bool:
    if isinstance(spec, AnySpec):
        return True
    elif spec == OBJECT_SPEC:
        return True
    elif isinstance(spec, UnionSpec):
        return any(spec_is_any(a) for a in spec.args)
    else:
        return False
