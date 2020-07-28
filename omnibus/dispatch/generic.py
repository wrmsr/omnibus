"""
TODO:
 - fmap
  - asts - traverse, rewrite
 - ensure virtual abc's work
 - https://docs.julialang.org/en/v1/manual/methods/
  - https://www.reddit.com/r/IAmA/comments/hyva5n/we_are_the_creators_of_the_julia_programming/
"""
import typing as ta

from .. import check
from .. import lang
from .. import reflect as rfl
from .. import registries
from .types import AmbiguousDispatchError
from .types import Dispatcher
from .types import Impl
from .types import Manifest
from .types import TypeOrSpec


lang.warn_unstable()


class GenericDispatcher(Dispatcher[Impl]):

    def __init__(self, registry: registries.Registry[rfl.Spec, Impl] = None) -> None:
        super().__init__()

        if registry is not None:
            self._registry = check.isinstance(registry, registries.Registry)
        else:
            self._registry = registries.DictRegistry()

    def key(self, obj: ta.Any) -> rfl.Spec:
        return rfl.spec(obj)

    @property
    def registry(self) -> registries.Registry[TypeOrSpec, Impl]:
        return self._registry

    def register_many(self, keys: ta.Iterable[TypeOrSpec], impl: Impl) -> 'Dispatcher[Impl]':
        for key in keys:
            cls = rfl.spec(key)
            self._registry[cls] = impl
        return self

    def _resolve(self, spec: rfl.Spec) -> ta.Tuple[ta.Optional[Impl], ta.Optional[Manifest]]:
        # TODO: generic_compose_mro to weed out ineligible
        # mro = generic_compose_mro(cls, list(self._registry.keys()))
        # try:
        #     return match, self._registry[match]
        # except registries.NotRegisteredException:
        #     raise UnregisteredDispatchError(match)

        ms = []
        for k, v in self._registry.items():
            for m in rfl.cmp._issubclass(spec, k):
                ms.append((k, m))

        if not ms:
            return None, None

        elif len(ms) > 1:
            best = ms[0]
            for cur in ms[1:]:
                cur_is_a_best = rfl.cmp.issubclass_(cur[0], best[0])
                best_is_a_cur = rfl.cmp.issubclass_(best[0], cur[0])
                if cur_is_a_best and not best_is_a_cur:
                    best = cur
                elif best_is_a_cur and not cur_is_a_best:
                    pass
                else:
                    raise AmbiguousDispatchError
            for cur in ms:
                if cur is best:
                    continue
                cur_is_a_best = rfl.cmp.issubclass_(cur[0], best[0])
                best_is_a_cur = rfl.cmp.issubclass_(best[0], cur[0])
                if cur_is_a_best or not best_is_a_cur:
                    raise AmbiguousDispatchError

        else:
            [best] = ms

        (k, m) = best
        match, impl, = k, self._registry[k]
        vs = {k: v.bind for k, v in m.vars.items()}
        return impl, Manifest(spec, match, vars=vs)

    def dispatch(self, key: TypeOrSpec) -> ta.Tuple[ta.Optional[Impl], ta.Optional[Manifest]]:
        spec = rfl.spec(key)
        try:
            impl = self._registry[spec]
        except registries.NotRegisteredException:
            return self._resolve(spec)
        else:
            return impl, Manifest(key, spec)

    def __contains__(self, key: TypeOrSpec) -> bool:
        raise NotImplementedError
