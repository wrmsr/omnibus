"""
TODO:
 - ** (serializers|deserializers)_by_spec
 - strict mode
 - replace with builtin omni generic impl
 - extensible serde Contexts? want pluggable datatypes, -> Datatype.of
 - recursive custom serde?
 - allow_empty? system: {{}}
"""
import typing as ta
import weakref

from ... import check
from ... import defs
from ... import reflect as rfl
from .types import DeserializationException
from .types import Serde
from .types import SerdeGen
from .types import Serialized


T = ta.TypeVar('T')


class _ProxySerde(Serde):

    def __init__(self, spec: rfl.Spec) -> None:
        super().__init__()

        self._spec = spec
        self._child: ta.Optional[Serde] = None

    defs.repr('_spec')

    def set(self, child: Serde) -> None:
        check.none(self._child)
        self._child = child

    def serialize(self, obj: T) -> ta.Any:
        return self._child.serialize(obj)

    def deserialize(self, ser: ta.Any) -> T:
        return self._child.deserialize(ser)


class _SerdeState:

    def __init__(self) -> None:
        super().__init__()

        self._priority_serde_gens: ta.MutableSequence[SerdeGen] = []
        self._serde_gens: ta.MutableSequence[SerdeGen] = []

        self._serdes_by_spec: ta.MutableMapping[rfl.Spec, Serde] = weakref.WeakKeyDictionary()
        self._proxies_by_spec: ta.MutableMapping[rfl.Spec, _ProxySerde] = {}

    def register_serde_gen(self, serde_gen: SerdeGen, priority: bool = False) -> None:
        check.callable(serde_gen)
        if priority:
            self._priority_serde_gens.append(serde_gen)
        else:
            self._serde_gens.append(serde_gen)

    def _gen_serde(self, spec: rfl.Spec) -> Serde:
        check.isinstance(spec, rfl.Spec)

        for g in self._priority_serde_gens:
            s = g(spec)
            if s:
                return s

        matches = [s for g in self._serde_gens for s in [g(spec)] if s is not None]
        if matches:
            return check.single(matches)

        raise TypeError(spec)

    def serde(self, spec: ta.Optional[ta.Any]) -> Serde:
        spec = rfl.spec(spec)

        try:
            return self._serdes_by_spec[spec]
        except KeyError:
            pass

        try:
            return self._proxies_by_spec[spec]
        except KeyError:
            pass

        try:
            prx = self._proxies_by_spec[spec] = _ProxySerde(spec)
            sd = self._gen_serde(spec)
            self._serdes_by_spec[spec] = sd
            prx.set(sd)
        finally:
            del self._proxies_by_spec[spec]

        return sd

    def serialize(self, obj: T, spec: ta.Optional[ta.Any] = None) -> Serialized:
        return self.serde(spec if spec is not None else type(obj)).serialize(obj)

    _NO_RERAISE = False
    # _NO_RERAISE = True

    def deserialize(self, ser: Serialized, spec: ta.Any, no_reraise: bool = False) -> T:
        spec = rfl.spec(spec)
        if no_reraise or self._NO_RERAISE:
            return self.serde(spec).deserialize(ser)
        else:
            try:
                return self.serde(spec).deserialize(ser)
            except Exception as e:
                raise DeserializationException(spec=spec, ser=ser) from e


_STATE = _SerdeState()


def serde_gen(*, priority: bool = False):
    def inner(obj):
        if isinstance(obj, type):
            sd = obj()
        else:
            sd = obj
        _STATE.register_serde_gen(sd, priority=priority)
        return obj
    return inner


serde = _STATE.serde
serialize = _STATE.serialize
deserialize = _STATE.deserialize
