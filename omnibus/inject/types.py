import abc
import functools
import typing as ta

from .. import check
from .. import dataclasses as dc
from .. import dynamic as dyn
from .. import lang
from .. import properties


T = ta.TypeVar('T')
K = ta.TypeVar('K')
V = ta.TypeVar('V')


class NOT_SET(lang.Marker):
    pass


class Element(lang.Abstract):
    pass


@dc.dataclass(frozen=True)
class Key(ta.Generic[T], lang.Final):
    type: ta.Type[T]
    annotation: ta.Any = None


@dc.dataclass(frozen=True)
class RequiredKey(Element, ta.Generic[T], lang.Final):
    key: Key[T]
    required_by: ta.Any


class Provider(lang.Abstract, ta.Generic[T]):

    @lang.abstract
    def __call__(self) -> T:
        raise NotImplementedError


@dc.dataclass(frozen=True)
class ValueProvider(Provider[T]):
    value: T

    def __call__(self) -> T:
        return self.value


@dc.dataclass(frozen=True)
class CallableProvider(Provider[T]):
    callable: ta.Callable[[], T]

    def __call__(self) -> T:
        return self.callable()


@dc.dataclass(frozen=True)
class ClassProvider(CallableProvider[T], lang.Final):
    cls: ta.Type[T]


@dc.dataclass(frozen=True)
class LinkedProvider(Provider[T], lang.Final):
    key: Key[T]

    def __call__(self) -> T:
        return Injector.current.get_instance(self.key)


@dc.dataclass(frozen=True)
class ProviderLinkedProvider(Provider[T], lang.Final):
    key: Key[T]

    def __call__(self) -> T:
        return Injector.current.get_instance(Key(Provider[self.key.type], self.key.annotation))()


@dc.dataclass(frozen=True)
class DelegatedProvider(Provider[T], lang.Final):
    key: Key[T]
    injector: 'Injector'

    def __call__(self) -> T:
        return self.injector.get_instance(self.key)


class BindingSource(lang.Abstract):
    pass


def _special_binding_source(name: str) -> BindingSource:
    return lang.new_type(name + 'BindingSource', (BindingSource,), {})()


BindingSource.EXPLICIT = _special_binding_source('Explicit')
BindingSource.PROVIDER = _special_binding_source('Provider')
BindingSource.INTERNAL = _special_binding_source('Internal')
BindingSource.EXPOSED_PRIVATE = _special_binding_source('ExposedPrivate')


@dc.dataclass(frozen=True)
class JitBindingSource(BindingSource, lang.Final):
    required_by: ta.Any


@dc.dataclass(frozen=True)
class Binding(Element, ta.Generic[T]):
    key: Key[T]
    provider: Provider[T]
    scoping: ta.Type['Scope']
    source: BindingSource

    def provide(self) -> T:
        return Injector.current._scopes[self.scoping].provide(self)


class Scope(lang.Abstract):

    @lang.abstract
    def provide(self, binding: Binding[T]) -> T:
        raise NotImplementedError


@dc.dataclass(frozen=True)
class ScopeBinding(Element):
    scoping: ta.Type[Scope]


@dc.dataclass(frozen=True)
class MultiBinding(Binding[T], lang.Abstract):
    pass


@dc.dataclass(frozen=True)
class MultiProvider(Provider[T], lang.Abstract):
    pass


@dc.dataclass(frozen=True)
class SetBinding(MultiBinding[T], lang.Final):
    pass


@dc.dataclass(frozen=True)
class SetProvider(MultiProvider[ta.Set[T]], lang.Final):
    set_key: Key[ta.Set[T]]

    def __call__(self) -> ta.Set[T]:
        ret = set()
        bindings = Injector.current.get_bindings(Key(SetBinding[self.set_key.type], self.set_key.annotation))
        for binding in bindings:
            check.isinstance(binding, SetBinding)
            ret.add(binding.provide())
        return ret


@dc.dataclass(frozen=True)
class DictBinding(MultiBinding[T], lang.Final):
    assignment: K


@dc.dataclass(frozen=True)
class DictProvider(MultiProvider[ta.Dict[K, V]], lang.Final):
    dict_key: Key[ta.Dict[K, V]]

    def __call__(self) -> ta.Dict[K, V]:
        ret = {}
        bindings = Injector.current.get_bindings(Key(DictBinding[self.dict_key.type], self.dict_key.annotation))
        for binding in bindings:
            check.isinstance(binding, DictBinding)
            check.not_in(binding.assignment, ret)
            ret[binding.assignment] = binding.provide()
        return ret


@dc.dataclass(frozen=True)
class PrivateElements(Element, lang.Final):
    elements: ta.List[Element]


@dc.dataclass(frozen=True)
class ExposedKey(Element, ta.Generic[T], lang.Final):
    key: Key[T]


class InjectionError(Exception):
    pass


@dc.dataclass(frozen=True)
class InjectionKeyError(InjectionError):
    key: Key


@dc.dataclass(frozen=True)
class InjectionRequiredKeyError(InjectionKeyError):
    required_by: ta.Any = None


@dc.dataclass(frozen=True)
class InjectionBlacklistedKeyError(InjectionKeyError):
    pass


Source = ta.Union['PrivateBinder', 'Binder', ta.Iterable[Element]]


@dc.dataclass(frozen=True)
class InjectorConfig(lang.Final):
    enable_jit_bindings: bool = False
    fail_early: bool = False


class Injector(lang.Abstract):

    _CURRENT: dyn.Var['Injector'] = dyn.Var()

    @properties.class_
    def current(cls) -> 'Injector':
        return check.isinstance(cls._CURRENT(), cls)

    @abc.abstractproperty
    def config(self) -> InjectorConfig:
        raise NotImplementedError

    @abc.abstractproperty
    def parent(self) -> 'ta.Optional[Injector]':
        raise NotImplementedError

    @abc.abstractmethod
    def create_child(self, *sources: Source) -> 'Injector':
        raise NotImplementedError

    @abc.abstractmethod
    def get_instance(
            self,
            target: ta.Union[Key[T], ta.Type[T]],
            default: ta.Any = NOT_SET,
    ) -> T:
        raise NotImplementedError

    @abc.abstractmethod
    def get_bindings(
            self,
            key: Key[MultiBinding[T]],
            *,
            parent: bool = False,
            children: bool = False,
    ) -> ta.Set[Binding]:
        raise NotImplementedError


class Binder(lang.Abstract):

    @abc.abstractproperty
    def elements(self) -> ta.Sequence[Element]:
        raise NotImplementedError

    @abc.abstractmethod
    def bind(
            self,
            target: ta.Union[Key, ta.Type, ta.Any],
            *,
            annotated_with: ta.Any = NOT_SET,

            to: ta.Union[Key, ta.Type] = NOT_SET,
            to_provider: ta.Union[Key, ta.Type] = NOT_SET,
            to_instance: ta.Any = NOT_SET,

            as_singleton: bool = NOT_SET,
            as_eager_singleton: bool = NOT_SET,
            in_: ta.Union[ta.Type[Scope], ta.Type[NOT_SET]] = NOT_SET,

            source: BindingSource = BindingSource.EXPLICIT,

            binding_factory: ta.Callable[..., Binding] = Binding,
    ) -> Binding:
        raise NotImplementedError

    @abc.abstractmethod
    def bind_callable(
            self,
            callable: ta.Callable[..., T],
            *,
            key: Key[T] = None,
            inputs: ta.Mapping[str, Key] = None,
            in_: ta.Type[Scope] = NOT_SET,
            source: BindingSource = BindingSource.EXPLICIT,
    ) -> Binding:
        raise NotImplementedError

    @abc.abstractmethod
    def bind_class(
            self,
            cls: ta.Type[T],
            *,
            key: Key[T] = None,
            in_: ta.Type[Scope] = NOT_SET,
            source: BindingSource = BindingSource.EXPLICIT,
    ) -> Binding:
        raise NotImplementedError

    class _Child(lang.Abstract):

        def __init__(self, binder: 'Binder') -> None:
            super().__init__()

            self._binder = binder

    class SetBinder(_Child, ta.Generic[T], lang.Final):

        def __init__(self, binder: 'Binder', set_key: Key[ta.Set[T]]) -> None:
            super().__init__(binder)

            self._set_key = set_key

        def bind(
                self,
                *,
                to: ta.Union[Key, ta.Type] = NOT_SET,
                to_provider: ta.Union[Key, ta.Type] = NOT_SET,
                to_instance: ta.Any = NOT_SET,

                as_singleton: bool = NOT_SET,
                as_eager_singleton: bool = NOT_SET,
                in_: ta.Union[ta.Type[Scope], ta.Type[NOT_SET]] = NOT_SET,

                source: BindingSource = BindingSource.EXPLICIT,
        ) -> Binding:
            binding_key = Key(SetBinding[self._set_key.type], self._set_key.annotation)

            return self._binder.bind(
                binding_key,

                to=to,
                to_provider=to_provider,
                to_instance=to_instance,

                as_singleton=as_singleton,
                as_eager_singleton=as_eager_singleton,
                in_=in_,

                source=source,

                binding_factory=SetBinding,
            )

    @abc.abstractmethod
    def new_set_binder(
            self,
            value: ta.Type,
            *,
            annotated_with: ta.Any = None,

            as_singleton: bool = NOT_SET,
            as_eager_singleton: bool = NOT_SET,
            in_: ta.Union[ta.Type[Scope], ta.Type[NOT_SET]] = NOT_SET,

            source: BindingSource = BindingSource.EXPLICIT,
    ) -> SetBinder:
        raise NotImplementedError

    class DictBinder(_Child, ta.Generic[K, V], lang.Final):

        def __init__(self, binder: 'Binder', dict_key: Key[ta.Dict[K, V]]) -> None:
            super().__init__(binder)

            self._dict_key = dict_key

        def bind(
                self,
                assignment: K,
                *,
                to: ta.Union[Key, ta.Type] = NOT_SET,
                to_provider: ta.Union[Key, ta.Type] = NOT_SET,
                to_instance: ta.Any = NOT_SET,

                as_singleton: bool = NOT_SET,
                as_eager_singleton: bool = NOT_SET,
                in_: ta.Union[ta.Type[Scope], ta.Type[NOT_SET]] = NOT_SET,

                source: BindingSource = BindingSource.EXPLICIT,
        ) -> Binding:
            binding_key = Key(DictBinding[self._dict_key.type], self._dict_key.annotation)

            return self._binder.bind(
                binding_key,

                to=to,
                to_provider=to_provider,
                to_instance=to_instance,

                as_singleton=as_singleton,
                as_eager_singleton=as_eager_singleton,
                in_=in_,

                source=source,

                binding_factory=functools.partial(DictBinding, assignment=assignment),
            )

    @abc.abstractmethod
    def new_dict_binder(
            self,
            key: ta.Type,
            value: ta.Type,
            *,
            annotated_with: ta.Any = None,

            as_singleton: bool = NOT_SET,
            as_eager_singleton: bool = NOT_SET,
            in_: ta.Union[ta.Type[Scope], ta.Type[NOT_SET]] = NOT_SET,

            source: BindingSource = BindingSource.EXPLICIT,
    ) -> DictBinder:
        raise NotImplementedError


class PrivateBinder(Binder):

    @abc.abstractmethod
    def expose(
            self,
            target: ta.Union[Key, ta.Type, ta.Any],
            *,
            annotated_with: ta.Any = NOT_SET,
    ) -> None:
        raise NotImplementedError
