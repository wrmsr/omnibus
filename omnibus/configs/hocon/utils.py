import typing as ta

from ... import collections as ocol
from .types import ArrayValue
from .types import CompoundValue
from .types import ObjectValue
from .types import ReferenceValue
from .types import Value


UnwrappedValue = ta.Union[dict, list, Value]


def wrap_value(obj: UnwrappedValue) -> Value:
    if isinstance(obj, dict):
        return ObjectValue(ocol.FrozenDict({k: wrap_value(v) for k, v in obj.items()}))
    elif isinstance(obj, list):
        return ArrayValue(tuple(map(wrap_value, obj)))
    elif isinstance(obj, Value):
        return obj
    else:
        raise TypeError(obj)


def unwrap_value(val: Value) -> UnwrappedValue:
    if isinstance(val, ObjectValue):
        return {k: unwrap_value(v) for k, v in val.value.items()}
    elif isinstance(val, ArrayValue):
        return list(map(unwrap_value, val.value))
    elif isinstance(val, Value):
        return val
    else:
        raise TypeError(val)


def resolve_references(value: Value) -> Value:
    def rec(cur: Value):
        if isinstance(cur, ObjectValue):
            for c in cur.value.values():
                rec(c)
        elif isinstance(cur, ArrayValue):
            for c in cur.value:
                rec(c)
        elif isinstance(cur, CompoundValue):
            for c in cur.value:
                rec(c)
        elif isinstance(cur, ReferenceValue):
            unresolved.add(cur.value)
        elif isinstance(cur, Value):
            pass
        else:
            raise TypeError(cur)

    unresolved: ta.Set[str] = set()
    rec(value)

    resolved: ta.Dict[str, Value] = {}

    def get(path: str) -> ta.Optional[Value]:
        try:
            return resolved[path]
        except KeyError:
            pass
        cur = value
        for part in path.split('.'):
            if isinstance(cur, ReferenceValue):
                return None
            elif isinstance(cur, ObjectValue):
                try:
                    cur = cur.value[part]
                except KeyError:
                    return None
            else:
                raise TypeError(cur)
        if isinstance(cur, CompoundValue):
            for e in cur.value:
                if isinstance(e, ReferenceValue) and e.value not in resolved:
                    return None
        return cur

    while unresolved:
        changed = False
        for path in list(unresolved):
            val = get(path)
            if val is not None:
                resolved[path] = val
                unresolved.remove(path)
                changed = True
        if not changed:
            break

    def rec(cur: Value) -> Value:
        if isinstance(cur, ObjectValue):
            return ObjectValue(ocol.FrozenDict({k: rec(v) for k, v in cur.value.items()}))
        elif isinstance(cur, ArrayValue):
            return ArrayValue(tuple(map(rec, cur.value)))
        elif isinstance(cur, CompoundValue):
            return CompoundValue(tuple(map(rec, cur.value)))
        elif isinstance(cur, ReferenceValue):
            return resolved.get(cur.value, cur)
        elif isinstance(cur, Value):
            return cur
        else:
            raise TypeError(cur)

    return rec(value)
