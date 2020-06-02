"""
** FEATURE LOCK **

DECREE:
 - validate returns None and raises, check returns bool

TODO:
 - Field options:
  - transient (+cache_hash)
  - *default_factory with lambda args* - toposort again
  - redaction - RedactedStr type?
  - per-field finality
  - per-field ordering (does this already?)
 - Class options:
  - coerce: True=just call w val, cls-lvl default on/off, unary void callable
  - validate: True=default, cls-lvl default on/off, unary void callable ...
 - typecheck defaults on def
 - jackson style json serdes interop
   - https://github.com/FasterXML/jackson-databind/wiki/Mapper-Features
 - pyo3 + cy struct type interop
  - derive dataclasses from external
 - ExtraFieldParams?
 - observable? dc.observe? per-cls/per-field? config-lvl?
 - fix: validate/coerce on setattr
 - intern? class-level, can intern fields w/ just coerce
 - frozen_subtypes, frozen_deep - enum?
 - freeze a non-frozen dc
 - lazy derivers
 - gen
  - interops:
   - protobuf
   - thrift
   - jsonschema
   - avro
  - incl enums
  - extend w functions? grpc/twirp/thrift?
 - partial validation - subclass?
 - parameterized tests - storage, params, etc
 - standard named aspect packs: tuple, dict, pyrsistent
  - 'profiles' - will also be in serde too (but keep eye on inj interop)
 - ** CYTHON **
  - dogfood CacheLink
  - with jitted/compiled dataclasses ~can bypass dict hits~...
  - maven style classpath scan at build, hash/cmp structure at boot, use if present / warn if not
   - just like tok
 - make FunctionCtx use code.FunctionGen (need argspec earlier)
 - sql interop? https://marshmallow-sqlalchemy.readthedocs.io/en/latest/
 - enforce immut metadata
"""
import collections
import collections.abc
import copy
import dataclasses as dc
import functools
import keyword
import types
import typing as ta

from . import process
from .. import lang
from .internals import DataclassParams
from .internals import is_dataclass_instance
from .types import Checker
from .types import Deriver
from .types import ExtraFieldParams
from .types import ExtraParams
from .types import Extras
from .types import METADATA_ATTR
from .types import MISSING_TYPE
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


def make_dataclass(
        cls_name: str,
        fields: ta.Union[str, ta.Tuple],
        *,
        bases: ta.Iterable[type] = (),
        namespace: ta.MutableMapping[str, ta.Any] = None,
        **kwargs
) -> type:
    if namespace is None:
        namespace = {}
    else:
        namespace = namespace.copy()

    seen = set()
    anns = {}
    for item in fields:
        if isinstance(item, str):
            name = item
            tp = 'typing.Any'
        elif len(item) == 2:
            name, tp, = item
        elif len(item) == 3:
            name, tp, spec = item
            namespace[name] = spec
        else:
            raise TypeError(f'Invalid field: {item!r}')

        if not isinstance(name, str) or not name.isidentifier():
            raise TypeError(f'Field names must be valid identifiers: {name!r}')
        if keyword.iskeyword(name):
            raise TypeError(f'Field names must not be keywords: {name!r}')
        if name in seen:
            raise TypeError(f'Field name duplicated: {name!r}')

        seen.add(name)
        anns[name] = tp

    namespace['__annotations__'] = anns
    cls = types.new_class(cls_name, tuple(bases), {}, lambda ns: ns.update(namespace))
    return dataclass(cls, **kwargs)


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
        default: ta.Union[ta.Any, MISSING_TYPE] = MISSING,
        default_factory: ta.Union[ta.Callable[[], ta.Any], MISSING_TYPE] = MISSING,
        init: bool = True,
        repr: bool = True,
        hash: ta.Optional[bool] = None,
        compare: bool = True,
        metadata: ta.Optional[ta.Mapping[ta.Any, ta.Any]] = None,

        doc: ta.Optional[str] = None,
        size: ta.Optional[ta.Any] = None,
        kwonly: bool = False,
        coerce: ta.Optional[ta.Union[bool, ta.Callable[[ta.Any], ta.Any]]] = None,
        derive: ta.Optional[ta.Callable[..., ta.Any]] = None,
        check: ta.Optional[ta.Union[bool, ta.Callable[[ta.Any], bool]]] = None,
        validate: ta.Optional[ta.Union[bool, ta.Callable[[ta.Any], None]]] = None,
) -> Field:
    extra_field_params = ExtraFieldParams(
        doc=doc,
        size=size,
        kwonly=kwonly,
        coerce=coerce,
        derive=derive,
        check=check,
        validate=validate,
    )

    if metadata is not None:
        if not isinstance(metadata, ta.Mapping):
            raise TypeError(metadata)
    else:
        metadata = {}

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
        _cls: ta.Optional[ta.Type[T]] = None,
        *,
        init: ta.Union[bool, MISSING_TYPE] = MISSING,  # True
        repr: ta.Union[bool, MISSING_TYPE] = MISSING,  # True
        eq: ta.Union[bool, MISSING_TYPE] = MISSING,  # True
        order: ta.Union[bool, MISSING_TYPE] = MISSING,  # False
        unsafe_hash: ta.Union[bool, MISSING_TYPE] = MISSING,  # False
        frozen: ta.Union[bool, MISSING_TYPE] = MISSING,  # False

        validate: ta.Union[bool, MISSING_TYPE] = MISSING,  # False
        field_attrs: ta.Union[bool, MISSING_TYPE] = MISSING,  # False
        cache_hash: ta.Union[bool, MISSING_TYPE] = MISSING,  # False
        pickle: ta.Union[bool, MISSING_TYPE] = MISSING,  # False
        reorder: ta.Union[bool, MISSING_TYPE] = MISSING,  # False
        aspects: ta.Union[None, ta.Sequence[ta.Any], MISSING_TYPE] = MISSING,  # None
        confer: ta.Union[None, ta.Sequence[str], ta.Mapping[str, ta.Any], MISSING_TYPE] = MISSING,  # None
) -> ta.Type[T]:
    if aspects is not MISSING and aspects is not None:
        aspects = list(aspects)
    if confer is not MISSING and confer is not None:
        confer = dict(confer) if isinstance(confer, ta.Mapping) else set(confer)

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
        cache_hash=cache_hash,
        pickle=pickle,
        reorder=reorder,
        aspects=aspects,
        confer=confer,
    )

    def build(cls):
        ctx = process.Context(cls, params, extra_params)
        drv = process.Driver(ctx)
        drv()
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
