import functools
import inspect
import typing as ta
import weakref

from .. import check
from .. import lang
from .multi import DictBinding
from .multi import DictProvider
from .multi import SetBinding
from .multi import SetProvider
from .proividers import CallableProvider
from .proividers import ClassProvider
from .proividers import LinkedProvider
from .proividers import ProviderLinkedProvider
from .proividers import ValueProvider
from .scopes import EagerSingletonScope
from .scopes import NoScope
from .scopes import SingletonScope
from .types import Binder
from .types import Binding
from .types import BindingSource
from .types import Element
from .types import ExposedKey
from .types import Injector
from .types import Key
from .types import NOT_SET
from .types import PrivateBinder
from .types import PrivateElements
from .types import Provider
from .types import ProvisionListener
from .types import ProvisionListenerBinding
from .types import RequiredKey
from .types import Scope


T = ta.TypeVar('T')
K = ta.TypeVar('K')
V = ta.TypeVar('V')


ANNOTATIONS: ta.MutableMapping[ta.Any, ta.Dict[str, ta.Any]] = weakref.WeakKeyDictionary()


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


class BinderImpl(Binder):

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

    def _get_callable_key(self, callable: ta.Callable, annotated_with: ta.Any = NOT_SET) -> Key:
        annotations = get_annotations(callable)
        key_ann = annotated_with if annotated_with is not NOT_SET else annotations.get('return')
        return Key(ta.get_type_hints(callable)['return'], key_ann)

    def _get_callable_inputs(self, callable: ta.Callable) -> ta.Dict[str, Key]:
        annotations = get_annotations(callable)
        return {k: Key(v, annotations.get(k)) for k, v in ta.get_type_hints(callable).items() if k != 'return'}

    def _make_callable_provider(
            self,
            callable: ta.Callable[..., T],
            *,
            prototype: ta.Callable[..., T] = None,
            inputs: ta.Mapping[str, ta.Union[Key, ta.Type]] = None,
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
            k: (self._get_key(v), (
                sig.parameters[k].default
                if k in sig.parameters and sig.parameters[k].default is not inspect._empty
                else NOT_SET
            ))
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
            annotated_with: ta.Any = NOT_SET,

            inputs: ta.Mapping[str, ta.Union[Key, ta.Type]] = None,

            as_singleton: bool = NOT_SET,
            as_eager_singleton: bool = NOT_SET,
            in_: ta.Union[ta.Type[Scope], ta.Type[NOT_SET]] = NOT_SET,

            source: BindingSource = BindingSource.EXPLICIT,
    ) -> Binding:
        check.callable(callable)

        if key is None:
            key = self._get_callable_key(callable, annotated_with=annotated_with)
        check.isinstance(key, Key)

        provide = self._make_callable_provider(callable, inputs=inputs)

        scoping = self._get_scoping(
            as_singleton=as_singleton,
            as_eager_singleton=as_eager_singleton,
            in_=in_,
        )

        binding = Binding(key, provide, scoping, source)
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

            as_singleton: bool = NOT_SET,
            as_eager_singleton: bool = NOT_SET,
            in_: ta.Union[ta.Type[Scope], ta.Type[NOT_SET]] = NOT_SET,

            source: BindingSource = BindingSource.EXPLICIT,
    ) -> Binding:
        check.isinstance(cls, type)

        if key is None:
            key = Key(cls)
        check.isinstance(key, Key)

        provide = self._make_class_provider(cls)

        scoping = self._get_scoping(
            as_singleton=as_singleton,
            as_eager_singleton=as_eager_singleton,
            in_=in_,
        )

        binding = Binding(key, provide, scoping, source)
        self._add_binding(binding)
        return binding

    class SetBinder(Binder.SetBinder[T]):

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
    ) -> Binder.SetBinder:
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

    class DictBinder(Binder.DictBinder[K, V]):

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
    ) -> Binder.DictBinder:
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

    def bind_provision_listener(
            self,
            target: ProvisionListener,
    ) -> None:
        check.callable(target)

        self._elements.append(ProvisionListenerBinding(target))


def create_binder() -> Binder:
    return BinderImpl()


class PrivateBinderImpl(BinderImpl, PrivateBinder):

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
        pass

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


def create_private_binder() -> PrivateBinder:
    return PrivateBinderImpl()
