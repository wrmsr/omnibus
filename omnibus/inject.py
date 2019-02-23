"""
https://github.com/google/guice/blob/extensions/mini/src/com/google/inject/mini/MiniGuice.java
 (2f2c3a629eaf7e9a4e3687ae17004789fd41fed6/)

TODO:
- proxies / circular injection
- type converters
- redundant providers / resolve
- override
"""
import collections
import dataclasses as dc
import functools
import inspect
import threading
import typing as ta
import weakref

from . import check
from . import dynamic as dyn
from . import lang
from . import properties
from . import reflect as rfl
from .collections import IdentityKeyDict
from .collections import IdentitySet


T = ta.TypeVar('T')
K = ta.TypeVar('K')
V = ta.TypeVar('V')


ANNOTATIONS: ta.MutableMapping[ta.Any, ta.Dict[str, ta.Any]] = weakref.WeakKeyDictionary()


class NOT_SET(lang.Marker):
    pass


def annotate(return_=NOT_SET, **kwargs) -> ta.Callable[[T], T]:
    def inner(obj):
        check.not_in(obj, ANNOTATIONS)
        ANNOTATIONS[obj] = kwargs
        return obj
    if return_ is not NOT_SET:
        kwargs['return'] = return_
    return inner


def get_annotations(obj: ta.Any) -> ta.Mapping[str, ta.Any]:
    try:
        return ANNOTATIONS.get(obj, {})
    except TypeError:
        return {}


class Box(lang.Abstract, ta.Generic[T]):

    def __init__(self, value: T) -> None:
        super().__init__()

        self._value = value

    TYPE: ta.Type[T] = NOT_SET

    @property
    def value(self) -> T:
        return self._value


def make_box(
        name: str,
        type: ta.Type[T] = object,
        *,
        bases: ta.Iterable[type] = (),
) -> ta.Type[Box[T]]:
    return lang.new_type(name, (Box,) + tuple(bases), {'TYPE': type})


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


class NoScope(Scope, lang.Final):

    def provide(self, binding: Binding[T]) -> T:
        return binding.provider()


class AbstractSingletonScope(Scope, lang.Abstract):

    def __init__(self) -> None:
        super().__init__()

        self._values: ta.MutableMapping[Binding, ta.Any] = IdentityKeyDict()
        self._lock = threading.RLock()

    def provide(self, binding: Binding[T]) -> T:
        try:
            return self._values[binding]
        except KeyError:
            pass
        with self._lock:
            try:
                return self._values[binding]
            except KeyError:
                pass
            value = self._values[binding] = binding.provider()
            return value


class SingletonScope(AbstractSingletonScope, lang.Final):
    pass


class EagerSingletonScope(AbstractSingletonScope, lang.Final):
    pass


class ThreadScope(Scope):

    def __init_(self) -> None:
        super().__init__()

        self._local = threading.local()

    def provide(self, binding: Binding[T]) -> T:
        try:
            values = self._local.values
        except AttributeError:
            values = self._local.values = IdentityKeyDict()
        try:
            return values[binding]
        except KeyError:
            value = values[binding] = binding.provider()
            return value


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
class InjectionBlacklistedKyError(InjectionKeyError):
    pass


Source = ta.Union['PrivateBinder', 'Binder', ta.Iterable[Element]]


class Injector:

    @dc.dataclass(frozen=True)
    class Config(lang.Final):
        enable_jit_bindings: bool = False
        fail_early: bool = False

    def __init__(
            self,
            *sources: Source,
            config: Config = Config(),
            parent: 'Injector' = None,
    ) -> None:
        super().__init__()

        self._config = config
        self._parent: ta.Optional[Injector] = parent
        self._children: ta.List[Injector] = []

        self._lock = threading.RLock()
        self._current_state: Injector.State = None

        self._elements: ta.List[Element] = []

        self._elements.extend([
            ScopeBinding(NoScope),
            ScopeBinding(SingletonScope),
            ScopeBinding(EagerSingletonScope),
            ScopeBinding(ThreadScope),
            Binding(Key(Injector), ValueProvider(self), NoScope, BindingSource.INTERNAL),
        ])

        for source in sources:
            if isinstance(source, PrivateBinder):
                self._elements.append(source._private_elements)
            elif isinstance(source, Binder):
                self._elements.extend(source._elements)
            else:
                for element in source:
                    check.isinstance(element, Element)
                    self._elements.append(element)

        self._scopes: ta.Dict[ta.Type[Scope], Scope] = {}
        self._required_keys = collections.deque()
        self._bindings: ta.List[Binding] = []
        self._blacklisted_keys: ta.Set[Key] = set()

        self._process_elements(self._elements)

        self._add_jit_bindings()
        self._load_eager_singletons()

    class State:

        def __init__(self, injector: 'Injector') -> None:
            super().__init__()

            self._injector = injector

        @properties.cached
        def elements_by_type(self) -> ta.Mapping[ta.Type[Element], ta.Set[Element]]:
            ret = {}
            for ele in self._injector._elements:
                for cls in type(ele).__mro__:
                    ret.setdefault(cls, set()).add(ele)
            return ret

        @properties.cached
        def exposed_keys(self) -> ta.Set[Key]:
            return {e.key for e in self.elements_by_type.get(ExposedKey)}

        @properties.cached
        def bound_keys(self) -> ta.Set[Key]:
            return {b.key for b in self._injector._bindings}

    @property
    def _state(self) -> State:
        if self._current_state is None:
            self._current_state = self.State(self)
        return self._current_state

    def _invalidate_self(self) -> None:
        self._current_state = None

    def _invalidate(self) -> None:
        seen = IdentitySet()
        stack = [self]
        while stack:
            cur = stack.pop()
            if cur in seen:
                continue
            seen.add(cur)
            cur._invalidate_self()
            if cur._parent is not None:
                stack.append(cur._parent)
            stack.extend(cur._children)

    def _process_elements(self, elements: ta.Iterable[Element]) -> None:
        for e in elements:
            if isinstance(e, ScopeBinding):
                self._add_scope_binding(e)

        for e in elements:
            if isinstance(e, RequiredKey):
                self._required_keys.append(e)

        for e in elements:
            if isinstance(e, Binding):
                self._add_binding(e)

        for e in elements:
            if isinstance(e, PrivateElements):
                self._add_private_elements(e)

    @property
    def config(self) -> Config:
        return self._config

    @property
    def parent(self) -> 'ta.Optional[Injector]':
        return self._parent

    @lang.context_wrapped('_lock')
    def create_child(self, *sources: Source) -> 'Injector':
        child = Injector(
            *sources,
            config=self._config,
            parent=self,
        )
        self._children.append(child)
        return child

    _CURRENT = dyn.Var()

    @properties.class_
    def current(cls) -> 'Injector':
        return check.isinstance(cls._CURRENT(), cls)

    @lang.context_wrapped('_lock')
    def get_instance(
            self,
            target: ta.Union[Key[T], ta.Type[T]],
            default: ta.Any = NOT_SET,
    ) -> T:
        if isinstance(target, Key):
            key = target
        else:
            key = Key(target)

        bindings = self.get_bindings(key)

        if not bindings:
            if key in self._blacklisted_keys:
                raise InjectionBlacklistedKyError(key)

            bindings = self.get_bindings(key, parent=True)

        if not bindings:
            if default is not NOT_SET:
                return default

            if not self.config.enable_jit_bindings:
                raise InjectionKeyError(key)
            self._require_key(key, 'jit')
            self._add_jit_bindings()
            bindings = self.get_bindings(key)

        if len(bindings) > 1:
            binding = check.single(set(bindings))
            check.isinstance(binding.provider, MultiProvider)
        else:
            binding = check.single(bindings)

        with self._CURRENT(self):
            return binding.provide()

    def _blacklist(self, key: Key) -> None:
        if self._parent is not None:
            self._parent._blacklist(key)
        self._blacklisted_keys.add(key)

    @lang.context_wrapped('_lock')
    def get_bindings(
            self,
            key: Key[MultiBinding[T]],
            *,
            parent: bool = False,
            children: bool = False,
    ) -> ta.Set[Binding]:
        ret = set()
        if parent and self._parent is not None:
            ret.update(self._parent.get_bindings(key, parent=True))
        for binding in self._bindings:
            if binding.key == key:
                ret.add(binding)
        if children:
            for child in self._children:
                ret.update(child.get_bindings(key, children=True))
        return ret

    def _require_key(
            self,
            key: Key,
            required_by: ta.Any,
    ) -> None:
        check.isinstance(key, Key)
        spec = rfl.get_spec(key.type)
        if isinstance(spec, rfl.ParameterizedGenericTypeSpec) and spec.erased_cls is Provider:
            key = Key(spec.args[0].cls, key.annotation)
        self._required_keys.append(RequiredKey(key, required_by))

    def _add_binding(self, binding: Binding[T]) -> None:
        check.isinstance(binding, Binding)
        spec = rfl.get_spec(binding.key.type)
        if not (
                isinstance(binding.provider, MultiProvider) or
                (isinstance(spec, rfl.ParameterizedGenericTypeSpec) and issubclass(spec.erased_cls, MultiBinding))
        ):
            if self._config.fail_early:
                check.not_in(binding.key, self._state.bound_keys)
        self._bindings.append(binding)
        if self._parent is not None:
            self._parent._blacklist(binding.key)
        self._invalidate()

    def _add_private_elements(self, private_elements: PrivateElements) -> None:
        child = self.create_child(private_elements.elements)
        for e in private_elements.elements:
            if isinstance(e, ExposedKey):
                provider = DelegatedProvider(e.key, child)
                binding = Binding(e.key, provider, NoScope, BindingSource.EXPOSED_PRIVATE)
                self._add_binding(binding)

    def _add_scope_binding(self, scope_binding: ScopeBinding) -> None:
        check.not_in(scope_binding.scoping, self._scopes)
        scope = check.issubclass(scope_binding.scoping, Scope)()
        self._scopes[scope_binding.scoping] = scope
        self._invalidate()

    def _load_eager_singletons(self) -> None:
        for binding in self._bindings:
            if isinstance(binding.scoping, EagerSingletonScope):
                binding.scoping.provide(binding)

    def _add_jit_bindings(self) -> None:
        while self._required_keys:
            required_key: RequiredKey = self._required_keys.popleft()
            if required_key.key in self._state.bound_keys:
                continue

            key = required_key.key
            if not isinstance(key.type, type) or key.annotation is not None:
                raise InjectionRequiredKeyError(required_key.key, required_key.required_by)

            self._add_jit_binding(key, required_key.required_by)

    def _add_jit_binding(self, key: Key, required_by: ta.Any) -> None:
        check.state(self._config.enable_jit_bindings)
        check.none(key.annotation)
        cls = check.isinstance(key.type, type)
        jit_binder = Binder()
        jit_binder.bind_class(cls, key=key, source=JitBindingSource(required_by))
        self._process_elements(jit_binder._elements)


class Binder:

    def __init__(self) -> None:
        super().__init__()

        self._elements: ta.List[Element] = []

    @property
    def elements(self) -> ta.Sequence[Element]:
        return self._elements

    def _require_key(self, key: Key[T], required_by: ta.Any) -> None:
        self._elements.append(RequiredKey(key, required_by))

    def _add_binding(self, binding: Binding[T]) -> None:
        self._elements.append(binding)
        self._add_provider_binding(binding)
        self._auto_expose_binding(binding)

    def _add_provider_binding(self, binding: Binding[T]) -> None:
        provider_key = Key(Provider[binding.key.type], binding.key.annotation)
        provider_binding = Binding(
            provider_key, ValueProvider(binding.provider), binding.scoping, BindingSource.PROVIDER)
        self._elements.append(provider_binding)

    def _auto_expose_binding(self, binding: Binding[T]) -> None:
        self._elements.append(ExposedKey(binding.key))

    def _get_key(
            self,
            target: ta.Union[Key, ta.Type[T], ta.Any],
            *,
            annotated_with: ta.Any = NOT_SET,
            allow_instance: bool = False,
    ) -> Key[T]:
        if isinstance(target, Key):
            check.arg(annotated_with is NOT_SET)
            key = target
        else:
            ann = annotated_with if annotated_with is not NOT_SET else None
            if isinstance(target, type):
                key = Key(target, ann)
            else:
                if not allow_instance:
                    raise TypeError(target)
                key = Key(type(target), ann)

        return key

    def _get_scoping(
            self,
            *,
            as_singleton: bool = NOT_SET,
            as_eager_singleton: bool = NOT_SET,
            in_: ta.Union[ta.Type[Scope], ta.Type[NOT_SET]] = NOT_SET,
    ) -> ta.Type['Scope']:
        scoping = None
        if as_singleton is not NOT_SET:
            scoping = check.replacing_none(scoping, SingletonScope)
        if as_eager_singleton is not NOT_SET:
            scoping = check.replacing_none(scoping, EagerSingletonScope)
        if in_ is not NOT_SET:
            scoping = check.replacing_none(scoping, in_)
        if scoping is None:
            scoping = NoScope

        return scoping

    def _get_provider(
            self,
            *,
            to: ta.Union[Key, ta.Type] = NOT_SET,
            to_provider: ta.Union[Key, ta.Type] = NOT_SET,
            to_instance: ta.Any = NOT_SET,

            required_by: ta.Any = None,
            target: ta.Any = NOT_SET,
    ) -> Provider[T]:
        provider = None
        if to is not NOT_SET:
            if not isinstance(to, Key):
                to = Key(to)
            self._require_key(to, required_by=required_by)
            provider = check.replacing_none(provider, LinkedProvider(to))
        if to_provider is not NOT_SET:
            if not isinstance(to_provider, Key):
                to_provider = Key(to_provider)
            self._require_key(Key(Provider[to_provider.type], to_provider.annotation), required_by=required_by)
            provider = check.replacing_none(provider, ProviderLinkedProvider(to_provider))
        if to_instance is not NOT_SET:
            provider = check.replacing_none(provider, ValueProvider(to_instance))
        if provider is None:
            check.arg(target is not NOT_SET)
            if isinstance(target, type):
                provider = self._make_class_provider(target)
            else:
                provider = ValueProvider(target)

        return provider

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
        if not isinstance(target, (Key, type)):
            check.arg(to is NOT_SET)
            check.arg(to_instance is NOT_SET)
        key = self._get_key(
            target,
            annotated_with=annotated_with,
            allow_instance=True,
        )

        scoping = self._get_scoping(
            as_singleton=as_singleton,
            as_eager_singleton=as_eager_singleton,
            in_=in_,
        )

        provider = self._get_provider(
            to=to,
            to_provider=to_provider,
            to_instance=to_instance,

            target=target,
            required_by=key,
        )

        binding = binding_factory(key, provider, scoping, source)
        self._add_binding(binding)
        return binding

    def _get_callable_key(self, callable: ta.Callable) -> Key:
        annotations = get_annotations(callable)
        return Key(ta.get_type_hints(callable)['return'], annotations.get('return'))

    def _get_callable_inputs(self, callable: ta.Callable) -> ta.Dict[str, Key]:
        annotations = get_annotations(callable)
        return {k: Key(v, annotations.get(k)) for k, v in ta.get_type_hints(callable).items() if k != 'return'}

    def _make_callable_provider(
            self,
            callable: ta.Callable[..., T],
            *,
            prototype: ta.Callable[..., T] = None,
            inputs: ta.Mapping[str, Key] = None,
            provider_factory: ta.Callable[..., Provider[T]] = CallableProvider[T],
    ) -> Provider[T]:
        check.callable(callable)
        if prototype is None:
            prototype = callable
        check.callable(prototype)

        sig = inspect.signature(prototype)
        if inputs is None:
            inputs = self._get_callable_inputs(prototype)
        inputs_and_defaults = {
            k: (v, sig.parameters[k].default if sig.parameters[k].default is not inspect._empty else NOT_SET)
            for k, v in inputs.items()
        }
        for k, (v, d) in inputs_and_defaults.items():
            check.isinstance(k, str)
            check.isinstance(v, Key)
            if d is NOT_SET:
                self._require_key(v, callable)

        def provide():
            kwargs = {k: Injector.current.get_instance(v, d) for k, (v, d) in inputs_and_defaults.items()}
            return callable(**kwargs)

        return provider_factory(provide)

    def bind_callable(
            self,
            callable: ta.Callable[..., T],
            *,
            key: Key[T] = None,
            inputs: ta.Mapping[str, Key] = None,
            in_: ta.Type[Scope] = NoScope,
            source: BindingSource = BindingSource.EXPLICIT,
    ) -> Binding:
        check.callable(callable)

        if key is None:
            key = self._get_callable_key(callable)
        check.isinstance(key, Key)

        provide = self._make_callable_provider(callable, inputs=inputs)

        binding = Binding(key, provide, in_, source)
        self._add_binding(binding)
        return binding

    def _make_class_provider(
            self,
            cls: ta.Type[T],
    ) -> Provider[T]:
        check.isinstance(cls, type)
        init = getattr(cls, '__init__')
        return self._make_callable_provider(
            cls,
            prototype=init,
            provider_factory=lambda c: ClassProvider(c, cls),
        )

    def bind_class(
            self,
            cls: ta.Type[T],
            *,
            key: Key[T] = None,
            in_: ta.Type[Scope] = NoScope,
            source: BindingSource = BindingSource.EXPLICIT,
    ) -> Binding:
        check.isinstance(cls, type)

        if key is None:
            key = Key(cls)
        check.isinstance(key, Key)

        provide = self._make_class_provider(cls)

        binding = Binding(key, provide, in_, source)
        self._add_binding(binding)
        return binding

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
        set_key = Key(ta.Set[value], annotated_with)

        scoping = self._get_scoping(
            as_singleton=as_singleton,
            as_eager_singleton=as_eager_singleton,
            in_=in_,
        )

        provider = SetProvider(set_key)

        binding = Binding(set_key, provider, scoping, source)
        self._add_binding(binding)
        return self.SetBinder(self, set_key)

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
        dict_key = Key(ta.Dict[key, value], annotated_with)

        scoping = self._get_scoping(
            as_singleton=as_singleton,
            as_eager_singleton=as_eager_singleton,
            in_=in_,
        )

        provider = DictProvider(dict_key)

        binding = Binding(dict_key, provider, scoping, source)
        self._add_binding(binding)
        return self.DictBinder(self, dict_key)


class PrivateBinder(Binder):

    def __init__(self, parent: Binder = None) -> None:
        super().__init__()

        self._private_elements = PrivateElements(self._elements)

        self._parent = parent
        if parent is not None:
            self._parent._elements.append(self._private_elements)

    @property
    def parent(self) -> ta.Optional[Binder]:
        return self._parent

    def _auto_expose_binding(self, binding: Binding[T]) -> None:
        self._elements.append(binding)

    def expose(
            self,
            target: ta.Union[Key, ta.Type, ta.Any],
            *,
            annotated_with: ta.Any = NOT_SET,
    ) -> None:
        key = self._get_key(
            target,
            annotated_with=annotated_with,
        )

        self._elements.append(ExposedKey(key))
