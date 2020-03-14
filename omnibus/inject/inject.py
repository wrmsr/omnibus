"""
https://github.com/google/guice/blob/extensions/mini/src/com/google/inject/mini/MiniGuice.java
 (2f2c3a629eaf7e9a4e3687ae17004789fd41fed6/)

TODO:
 - proxies / circular injection
 - type converters
 - redundant providers / resolve
 - override
 - LISTENERS - LifecycleManager
"""
import collections
import threading
import typing as ta

from .. import check
from .. import lang
from .. import properties
from .. import reflect as rfl
from ..collections import IdentitySet
from .bind import create_binder
from .bind import PrivateBinder
from .proividers import DelegatedProvider
from .proividers import ValueProvider
from .scopes import EagerSingletonScope
from .scopes import NoScope
from .scopes import SingletonScope
from .scopes import ThreadScope
from .types import Binder
from .types import Binding
from .types import BindingSource
from .types import Element
from .types import ExposedKey
from .types import InjectionBlacklistedKeyError
from .types import InjectionKeyError
from .types import InjectionRequiredKeyError
from .types import Injector
from .types import InjectorConfig
from .types import JitBindingSource
from .types import Key
from .types import MultiBinding
from .types import MultiProvider
from .types import NOT_SET
from .types import PrivateElements
from .types import Provider
from .types import RequiredKey
from .types import Scope
from .types import ScopeBinding
from .types import Source


T = ta.TypeVar('T')


class InjectorImpl(Injector):

    def __init__(
            self,
            *sources: Source,
            config: InjectorConfig = InjectorConfig(),
            parent: 'Injector' = None,
    ) -> None:
        super().__init__()

        self._config = config
        self._parent: ta.Optional[Injector] = parent
        self._children: ta.List[Injector] = []

        self._lock = threading.RLock()
        self._current_state: InjectorImpl.State = None

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
    def config(self) -> InjectorConfig:
        return self._config

    @property
    def parent(self) -> 'ta.Optional[Injector]':
        return self._parent

    @lang.context_wrapped('_lock')
    def create_child(self, *sources: Source) -> 'Injector':
        child = create_injector(
            *sources,
            config=self._config,
            parent=self,
        )
        self._children.append(child)
        return child

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
                raise InjectionBlacklistedKeyError(key)

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
        jit_binder = create_binder()
        jit_binder.bind_class(cls, key=key, source=JitBindingSource(required_by))
        self._process_elements(jit_binder._elements)


def create_injector(
        *sources: Source,
        config: InjectorConfig = InjectorConfig(),
        parent: 'Injector' = None,
) -> Injector:
    return InjectorImpl(
        *sources,
        config=config,
        parent=parent,
    )
