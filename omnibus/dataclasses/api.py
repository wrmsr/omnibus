"""
** FEATURE LOCK **

DECREE:
 - validate returns None and raises, check returns bool
 - self_check and self_validate variants take a constructed object

TODO:
 - attrs
  - fld: order, kwonly
  - cls: weakref_slot, auto_attribs, kwonly
  - cache_hash: hash='cache', transient
  - exc handling: https://github.com/python-attrs/attrs/pull/500
 - ..transient
 - *default_factory with lambda args* - toposort again
 - *default null makes optional.. lol..*
 - redaction - RedactedStr type?
 - auto-typecheck-validation
 - coerce: True=just call w val, cls-lvl default on/off, unary void callable
 - validate: True=default, cls-lvl default on/off, unary void callable ...
 - jackson style json serdes interop
   - https://github.com/FasterXML/jackson-databind/wiki/Mapper-Features
 - pyo3 + cy struct type interop
 - ExtraFieldParams?
 - observable? dc.observe? per-cls/per-field? config-lvl?
 - fix: validate/coerce on setattr
 - per-field finality
 - intern?
 - frozen_subtypes, frozen_deep - enum?
 - freeze a non-frozen dc
 - lazy derivers
"""
import collections
import collections.abc
import copy
import dataclasses as dc
import functools
import typing as ta

from .. import lang
from .build import BuildContext
from .build import ClassProcessor
from .internals import DataclassParams
from .internals import is_dataclass_instance
from .types import Checker
from .types import Deriver
from .types import ExtraFieldParams
from .types import ExtraParams
from .types import Extras
from .types import METADATA_ATTR
from .types import PostInit
from .types import SelfChecker
from .types import SelfValidator
from .types import Validator


T = ta.TypeVar('T')


Field = dc.Field
FrozenInstanceError = dc.FrozenInstanceError
InitVar = dc.InitVar
is_dataclass = dc.is_dataclass
MISSING = dc.MISSING
replace = dc.replace


def make_dataclass(*args, **kwargs):
    # FIXME
    raise NotImplementedError


def fields(class_or_instance: ta.Union[type, object]) -> ta.Iterable[Field]:
    return dc.fields(class_or_instance)


def fields_dict(class_or_instance) -> ta.Dict[str, Field]:
    return {f.name: f for f in fields(class_or_instance)}


def asdict(obj, *, dict_factory=dict, shallow=False):
    if not is_dataclass_instance(obj):
        raise TypeError('asdict() should be called on dataclass instances')
    if shallow:
        return {f.name: getattr(obj, f.name) for f in fields(obj)}
    return _asdict_inner(obj, dict_factory)


def _asdict_inner(obj, dict_factory):
    # https://bugs.python.org/issue35540
    if is_dataclass_instance(obj):
        result = []
        for f in fields(obj):
            value = _asdict_inner(getattr(obj, f.name), dict_factory)
            result.append((f.name, value))
        return dict_factory(result)
    elif isinstance(obj, tuple) and hasattr(obj, '_fields'):
        return type(obj)(*[_asdict_inner(v, dict_factory) for v in obj])
    elif isinstance(obj, (list, tuple)):
        return type(obj)(_asdict_inner(v, dict_factory) for v in obj)
    elif isinstance(obj, collections.defaultdict):
        return type(obj)(obj.default_factory, ((_asdict_inner(k, dict_factory), _asdict_inner(v, dict_factory)) for k, v in obj.items()))  # noqa
    elif isinstance(obj, dict):
        return type(obj)((_asdict_inner(k, dict_factory), _asdict_inner(v, dict_factory)) for k, v in obj.items())
    else:
        return copy.deepcopy(obj)


def astuple(obj, *, tuple_factory=tuple):
    if not is_dataclass_instance(obj):
        raise TypeError('astuple() should be called on dataclass instances')
    return _astuple_inner(obj, tuple_factory)


def _astuple_inner(obj, tuple_factory):
    if is_dataclass_instance(obj):
        result = []
        for f in fields(obj):
            value = _astuple_inner(getattr(obj, f.name), tuple_factory)
            result.append(value)
        return tuple_factory(result)
    elif isinstance(obj, tuple) and hasattr(obj, '_fields'):
        return type(obj)(*[_astuple_inner(v, tuple_factory) for v in obj])
    elif isinstance(obj, (list, tuple)):
        return type(obj)(_astuple_inner(v, tuple_factory) for v in obj)
    elif isinstance(obj, collections.defaultdict):
        return type(obj)(obj.default_factory, ((_asdict_inner(k, tuple_factory), _asdict_inner(v, tuple_factory)) for k, v in obj.items()))  # noqa
    elif isinstance(obj, dict):
        return type(obj)((_astuple_inner(k, tuple_factory), _astuple_inner(v, tuple_factory)) for k, v in obj.items())
    else:
        return copy.deepcopy(obj)


def field(
        *,
        default=MISSING,
        default_factory=MISSING,
        init=True,
        repr=True,
        hash=None,
        compare=True,
        metadata=None,

        coerce=None,
        derive=None,
        doc=None,
        size=None,
        validate=None,
) -> Field:
    extra_field_params = ExtraFieldParams(
        coerce=coerce,
        derive=derive,
        doc=doc,
        size=size,
        validate=validate,
    )

    metadata = dict(metadata or {})
    if ExtraFieldParams in metadata:
        raise KeyError(metadata, ExtraFieldParams)
    metadata[ExtraFieldParams] = extra_field_params

    return dc.field(
        default=default,
        default_factory=default_factory,
        init=init,
        repr=repr,
        hash=hash,
        compare=compare,
        metadata=metadata,
    )


def dataclass(
        _cls: ta.Type[T] = None,
        *,
        init=True,
        repr=True,
        eq=True,
        order=False,
        unsafe_hash=None,
        frozen=False,

        validate=None,
        field_attrs=False,
) -> ta.Type[T]:
    params = DataclassParams(
        init=init,
        repr=repr,
        eq=eq,
        order=order,
        unsafe_hash=unsafe_hash,
        frozen=frozen,
    )

    extra_params = ExtraParams(
        validate=validate,
        field_attrs=field_attrs,
    )

    def build(cls):
        ctx = BuildContext(cls, params, extra_params)
        ClassProcessor(ctx)()
        return cls

    if _cls is None:
        return build
    return build(_cls)


@lang.cls_dct_fn()
def install(cls_dct, cls, *args, **kwargs) -> None:
    if len(args) == 1 and isinstance(args[0], cls):
        [obj] = args
    else:
        obj = cls(*args, **kwargs)
    cls_dct.setdefault(METADATA_ATTR, {}).setdefault(Extras, []).append(obj)


check_ = functools.partial(install, Checker)
check_self = functools.partial(install, SelfChecker)
derive = functools.partial(install, Deriver)
post_init = functools.partial(install, PostInit)
validate = functools.partial(install, Validator)
validate_self = functools.partial(install, SelfValidator)
