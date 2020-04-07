"""
TODO:
 - order=False, kwwonly=False
 - *default_factory with lambda args* - toposort again
 - *default null makes optional.. lol..*
 - redaction - RedactedStr type?
 - auto-typecheck-validation
 - storage -> storage.py
 - coerce: True=just call w val, cls-lvl default on/off, unary void callable
 - validate: True=default, cls-lvl default on/off, unary void callable ...
 - jackson style json serdes interop
   - https://github.com/FasterXML/jackson-databind/wiki/Mapper-Features
 - pyo3 + cy struct type interop
"""
import collections
import collections.abc
import copy
import dataclasses as dc
import typing as ta

from .. import check as check_
from .. import lang
from .types import Checker
from .types import CHECKERS_ATTR
from .types import CoerceMetadata
from .types import DeriveMetadata
from .types import Deriver
from .types import DERIVERS_ATTR
from .types import DocMetadata
from .types import POST_INITS_ATTR
from .types import PostInit
from .types import SizeMetadata
from .types import ValidateMetadata
from .types import Validator
from .types import VALIDATORS_ATTR


T = ta.TypeVar('T')


def make_dataclass(*args, **kwargs):
    # FIXME
    raise NotImplementedError


def fields(class_or_instance: ta.Union[type, object]) -> ta.Iterable[dc.Field]:
    return dc.fields(class_or_instance)


def fields_dict(class_or_instance) -> ta.Dict[str, dc.Field]:
    return {f.name: f for f in fields(class_or_instance)}


def asdict(obj, *, dict_factory=dict, shallow=False):
    if not dc._is_dataclass_instance(obj):
        raise TypeError('asdict() should be called on dataclass instances')
    if shallow:
        return {f.name: getattr(obj, f.name) for f in fields(obj)}
    return _asdict_inner(obj, dict_factory)


def _asdict_inner(obj, dict_factory):
    # https://bugs.python.org/issue35540
    if dc._is_dataclass_instance(obj):
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
    if not dc._is_dataclass_instance(obj):
        raise TypeError('astuple() should be called on dataclass instances')
    return _astuple_inner(obj, tuple_factory)


def _astuple_inner(obj, tuple_factory):
    if dc._is_dataclass_instance(obj):
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
        default=dc.MISSING,
        default_factory=dc.MISSING,
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
        **kwargs
) -> dc.Field:
    md = {}
    if coerce is not None:
        md[CoerceMetadata] = coerce
    if derive is not None:
        md[DeriveMetadata] = derive
    if doc is not None:
        md[DocMetadata] = doc
    if size is not None:
        md[SizeMetadata] = size
    if validate is not None:
        md[ValidateMetadata] = validate
    if md:
        metadata = {**(metadata or {}), **md}

    return dc.field(
        default=default,
        default_factory=default_factory,
        init=init,
        repr=repr,
        hash=hash,
        compare=compare,
        metadata=metadata,
        **kwargs
    )


@lang.cls_dct_fn()
def check(cls_dct, checker: Checker) -> None:
    check_.callable(checker)
    cls_dct.setdefault(CHECKERS_ATTR, []).append(checker)


@lang.cls_dct_fn()
def derive(cls_dct, deriver: Deriver) -> None:
    check_.callable(deriver)
    cls_dct.setdefault(DERIVERS_ATTR, []).append(deriver)


@lang.cls_dct_fn()
def post_init(cls_dct, post_init: PostInit) -> None:
    check_.callable(post_init)
    cls_dct.setdefault(POST_INITS_ATTR, []).append(post_init)


@lang.cls_dct_fn()
def validate(cls_dct, validator: Validator) -> None:
    check_.callable(validator)
    cls_dct.setdefault(VALIDATORS_ATTR, []).append(validator)
