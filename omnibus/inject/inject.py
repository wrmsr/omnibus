"""
https://github.com/google/guice/blob/extensions/mini/src/com/google/inject/mini/MiniGuice.java
 (2f2c3a629eaf7e9a4e3687ae17004789fd41fed6/)

TODO:
 - ** PROVIDER DEPENDENCY INTROSPECTION - include defaults
 - ** type converters **
 - overhaul (remove?) invalidation
 - listeners
  - children
  - toposort deps
  - once per scope?
  - dep chain
  - recursion bit lifecycle listener, handle or just force impls to handle? scopes just force impls lol
 - more generic support - bind_class takes type, take spec
 - freezing?
 - parent/child traversing multis
 - proxies / circular injection
 - redundant providers / resolve
 - override
 - custom scopes: async/cvar/dyn?
 - assisted injection + config (dc) interop - adapter for externals w/ some-kwargs-injected some-kwargs-config'd
 - *dimensions* - cartesians, etc - likely child injectors
 - hybridize w actors/otp/akka props
  - ** PROPS ARE HERE, SUPER TREE IS IN LIFECYCLES **
  - message dispatcher
  - lifecycle rework for fsms/actors/btrees
 - use for generic Templates..
  - prob want field injection..
   - resurrect unwrappers? :|
   - ALT: templates are dataclasses lol, free ctor
    - weird poss's like pointlessly cythonized generic templates.. too much freedom?
 - injection super __init__ kwargs inspection?
  - almost certainly NOT. force manually forwarding. shouldn't have that many deps - if a lot then break out to compo.
  - *maybe* a @inj.inject_kwargs(SuperThing[.__init__?])
"""
import collections
import functools
import typing as ta
import weakref

from .. import check
from .. import collections as ocol
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
from .types import MISSING
from .types import MultiBinding
from .types import MultiProvider
from .types import PrivateElements
from .types import Provider
from .types import ProvisionListenerBinding
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
            lock: lang.DefaultLockable = None,
    ) -> None:
        super().__init__()

        self._config = config
        self._parent: ta.Optional[Injector] = parent
        self._children: ta.MutableSet[Injector] = weakref.WeakSet() if config.weak_children else ocol.OrderedSet()

        self._lock = lang.default_lock(
            config.lock, lock if lock is None else config.lock if config.lock is not None else True)
        self._current_state: InjectorImpl.State = None
        self._locking = lambda *a, **k: self._lock()

        src_elements: ta.List[Element] = []

        src_elements.extend([
            ScopeBinding(NoScope),
            ScopeBinding(SingletonScope),
            ScopeBinding(EagerSingletonScope),
            ScopeBinding(ThreadScope),
            Binding(Key(Injector), ValueProvider(self), NoScope, BindingSource.INTERNAL),
        ])

        for source in sources:
            if isinstance(source, PrivateBinder):
                src_elements.append(source._private_elements)
            elif isinstance(source, Binder):
                src_elements.extend(source._elements)
            else:
                for element in source:
                    check.isinstance(element, Element)
                    src_elements.append(element)

        self._scopes: ta.Dict[ta.Type[Scope], Scope] = {}
        self._scope_bindings: ta.List[ScopeBinding] = []
        self._required_keys = collections.deque()
        self._bindings: ta.List[Binding] = []
        self._blacklisted_keys: ta.Set[Key] = set()

        self._elements: ta.List[Element] = [e.possess(self) for e in src_elements]
        self._process_elements(self._elements)

        self._original_required_keys: ta.List[RequiredKey] = list(self._required_keys)
        self._add_jit_bindings()
        self._load_eager_singletons()

    class State:

        def __init__(self, injector: 'InjectorImpl') -> None:
            super().__init__()

            self._injector = injector
            self._bindings_cache: ta.Dict[Key, ta.List[Binding]] = {}

        @properties.cached
        def elements_by_type(self) -> ta.Mapping[ta.Type[Element], ta.List[Element]]:
            ret = {}
            for ele in self._injector._elements:
                for cls in type(ele).__mro__:
                    ret.setdefault(cls, []).append(ele)
            return ret

        @properties.cached
        def exposed_keys(self) -> ta.Set[Key]:
            return {e.key for e in self.elements_by_type.get(ExposedKey)}

        @properties.cached
        def recursive_bound_keys(self) -> ta.Set[Key]:
            ret = {b.key for b in self._injector._bindings}
            if self._injector._parent is not None:
                ret |= self._injector._parent._state.recursive_bound_keys
            return ret

    @property
    def _state(self) -> State:
        if self._current_state is None:
            self._current_state = self.State(self)
        return self._current_state

    def _invalidate_self(self) -> None:
        self._current_state = None

    def _invalidate(
            self,
            *,
            parent: bool = False,
            children: bool = False,
    ) -> None:
        seen = IdentitySet()
        stack = [self]
        while stack:
            cur = stack.pop()
            if cur in seen:
                continue
            seen.add(cur)
            cur._invalidate_self()
            if parent and cur._parent is not None:
                stack.append(cur._parent)
            if children:
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

    @lang.context_wrapped('_locking')
    def create_child(self, *sources: Source) -> 'Injector':
        child = create_injector(
            *sources,
            config=self._config,
            parent=self,
        )
        self._children.add(child)
        return child

    @lang.context_wrapped('_locking')
    def get_binding(
            self,
            target: ta.Union[Key[T], ta.Type[T]],
            *,
            has_default: bool = False,
    ) -> ta.Optional[Binding[T]]:
        check.isinstance(has_default, bool)

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
            if has_default:
                return None

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

        return binding

    @lang.context_wrapped('_locking')
    def get(
            self,
            target: ta.Union[Key[T], ta.Type[T]],
            default: ta.Any = MISSING,
    ) -> T:
        binding = self.get_binding(target, has_default=default is not MISSING)

        if binding is None:
            check.state(default is not MISSING)
            return default

        with self._CURRENT(self):
            fn = binding.provide

            if not isinstance(binding, ProvisionListenerBinding):
                for listener_binding in self.get_elements_by_type(ProvisionListenerBinding, parent=True):
                    fn = functools.partial(listener_binding.listener, self, target, fn)

            instance = fn()
            return instance

    def _blacklist(self, key: Key) -> None:
        if self._parent is not None:
            self._parent._blacklist(key)
        self._blacklisted_keys.add(key)

    @lang.context_wrapped('_locking')
    def get_elements_by_type(
            self,
            cls: ta.Type[Element],
            *,
            parent: bool = False,
            children: bool = False,
    ) -> ta.List[Element]:
        ret = []

        if parent and self._parent is not None:
            ret.extend(self._parent.get_elements_by_type(cls, parent=True))

        ret.extend(self._state.elements_by_type.get(cls, []))

        if children:
            for child in self._children:
                ret.extend(child.get_elements_by_type(cls, children=True))

        return ret

    @lang.context_wrapped('_locking')
    def get_bindings(
            self,
            key: Key,
            *,
            parent: bool = False,
            children: bool = False,
    ) -> ta.List[Binding]:
        ret = []

        if parent and self._parent is not None:
            ret.extend(self._parent.get_bindings(key, parent=True))

        try:
            self_bindings = self._state._bindings_cache[key]
        except KeyError:
            self_bindings = []
            for binding in self._bindings:
                if binding.key == key:
                    self_bindings.append(binding)
            self._state._bindings_cache[key] = self_bindings
        ret.extend(self_bindings)

        if children:
            for child in self._children:
                ret.extend(child.get_bindings(key, children=True))

        return ret

    def _require_key(
            self,
            key: Key,
            required_by: ta.Any,
    ) -> None:
        check.isinstance(key, Key)
        spec = rfl.spec(key.type)
        if isinstance(spec, rfl.ParameterizedGenericTypeSpec) and spec.erased_cls is Provider:
            key = Key(spec.args[0].cls, key.annotation)
        self._required_keys.append(RequiredKey(key, required_by))

    def _add_binding(self, binding: Binding[T]) -> None:
        check.isinstance(binding, Binding)
        spec = rfl.spec(binding.key.type)
        if not (
                isinstance(binding.provider, MultiProvider) or
                (isinstance(spec, rfl.ParameterizedGenericTypeSpec) and issubclass(spec.erased_cls, MultiBinding))
        ):
            if self._config.fail_early:
                check.not_in(binding.key, self._state.recursive_bound_keys)
        self._bindings.append(binding)
        if self._parent is not None:
            self._parent._blacklist(binding.key)
        self._invalidate()

    def _add_private_elements(self, private_elements: PrivateElements) -> None:
        child = self.create_child(private_elements.elements)
        for e in private_elements.elements:
            if isinstance(e, ExposedKey):
                provider = DelegatedProvider(e.key, child)
                binding = Binding(e.key, provider, NoScope, BindingSource.EXPOSED_PRIVATE).possess(self)
                self._add_binding(binding)

    def _construct_scope(self, scope_binding: ScopeBinding) -> Scope:
        return check.issubclass(scope_binding.scoping, Scope)()

    def _add_scope_binding(self, scope_binding: ScopeBinding) -> None:
        check.not_in(scope_binding.scoping, self._scopes)
        self._scope_bindings.append(scope_binding)
        self._scopes[scope_binding.scoping] = self._construct_scope(scope_binding)
        self._invalidate()

    def _load_eager_singletons(self) -> None:
        for binding in self._bindings:
            if binding.scoping is EagerSingletonScope:
                self.get(binding.key)

    def _add_jit_bindings(self) -> None:
        while self._required_keys:
            required_key: RequiredKey = self._required_keys.popleft()
            if required_key.key in self._state.recursive_bound_keys:
                continue

            key = required_key.key
            if not isinstance(key.type, type) or key.annotation is not None:
                raise InjectionRequiredKeyError(required_key.key, required_key.required_by)

            self._add_jit_binding(key, required_key.required_by)

    def _add_jit_binding(self, key: Key, required_by: ta.Any) -> None:
        if not self._config.enable_jit_bindings:
            raise InjectionRequiredKeyError(key, required_by)
        check.none(key.annotation)
        cls = check.isinstance(key.type, type)
        jit_binder = create_binder()
        jit_binder.bind_class(cls, key=key, source=JitBindingSource(required_by))
        jit_elements = [e.possess(self) for e in jit_binder._elements]
        self._process_elements(jit_elements)


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
