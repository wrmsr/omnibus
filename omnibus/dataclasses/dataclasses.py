"""
TODO:
 - order=False, kwwonly=False
 - *default_factory with lambda args* - toposort again
 - *default null makes optional.. lol..*
 - redaction - RedactedStr type?
 - auto-typecheck-validation
 - tuple, pyrsistent (diy, not PRecord), struct, struct-of-arrays. numpy?, mmap? ObjectArrayBackedMap equiv
  - with nesting
  - 'Storage' impls: default, ... - both inline/classdef *and* 're-casting' against bltin dc
   - so 'Stubbing' ala compcache shaper..
 - coerce: True=just call w val, cls-lvl default on/off, unary void callable
 - validate: True=default, cls-lvl default on/off, unary void callable ...
  - FieldValidator vs Validator - lambda x, y: vs lambda obj: - ~want both~
   - dc.validate_fields(lambda x, y:)
   - dc.validate(lambda obj:) - ~before~ post_init - ~could~ be used to do post-init shit but discourage w/ name
 - jackson style json serdes interop
   - https://github.com/FasterXML/jackson-databind/wiki/Mapper-Features
 - field.__doc__
 - pyo3 + cy struct type interop
"""
import collections
import collections.abc
import copy
import dataclasses as dc
import inspect
import types
import typing as ta

from .. import check
from .. import codegen
from .. import lang
from .types import ORIGIN_ATTR


T = ta.TypeVar('T')


def make_dataclass(*args, **kwargs):
    # FIXME
    raise NotImplementedError


def fields(class_or_instance: ta.Union[type, object]) -> ta.Iterable[dc.Field]:
    return dc.fields(class_or_instance)


def fields_dict(class_or_instance) -> ta.Dict[str, dc.Field]:
    return {f.name: f for f in fields(class_or_instance)}


def _compose_fields(cls: ta.Type) -> ta.Dict[str, dc.Field]:
    fields = {}

    for b in cls.__mro__[-1:0:-1]:
        base_fields = getattr(b, dc._FIELDS, None)
        if base_fields:
            for f in base_fields.values():
                fields[f.name] = f

    cls_annotations = cls.__dict__.get('__annotations__', {})

    cls_fields = [dc._get_field(cls, name, type) for name, type in cls_annotations.items()]
    for f in cls_fields:
        fields[f.name] = f

    return fields


def _check_bases(mro: ta.Sequence[ta.Type], *, frozen=False) -> None:
    any_frozen_base = False
    has_dataclass_bases = False
    for b in mro[-1:0:-1]:
        base_fields = getattr(b, dc._FIELDS, None)
        if base_fields:
            has_dataclass_bases = True
            if getattr(b, dc._PARAMS).frozen:
                any_frozen_base = True

    if has_dataclass_bases:
        if any_frozen_base and not frozen:
            raise TypeError('cannot inherit non-frozen dataclass from a frozen one')

        if not any_frozen_base and frozen:
            raise TypeError('cannot inherit frozen dataclass from a non-frozen one')


def _has_default(fld: dc.Field) -> bool:
    return fld.default is not dc.MISSING or fld.default_factory is not dc.MISSING


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


class SizeMetadata(lang.Marker):
    pass


class ValidateMetadata(lang.Marker):
    pass


class CoerceMetadata(lang.Marker):
    pass


class DeriveMetadata(lang.Marker):
    pass


def field(
        *,
        default=dc.MISSING,
        default_factory=dc.MISSING,
        init=True,
        repr=True,
        hash=None,
        compare=True,
        metadata=None,

        size=None,
        validate=None,
        coerce=None,
        derive=None,
        **kwargs
) -> dc.Field:
    md = {}
    if size is not None:
        md[SizeMetadata] = size
    if validate is not None:
        md[ValidateMetadata] = validate
    if coerce is not None:
        md[CoerceMetadata] = coerce
    if derive is not None:
        md[DeriveMetadata] = derive
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


def dataclass(
        _cls: ta.Type[T] = None,
        *,
        init=True,
        repr=True,
        eq=True,
        order=False,
        unsafe_hash=None,
        frozen=False,

        reorder=False,
        validate=False,
        **kwargs
) -> ta.Type[T]:
    fwd_kwargs = dict(
        init=init,
        repr=repr,
        eq=eq,
        order=order,
        unsafe_hash=unsafe_hash,
        frozen=frozen,
    )

    check.isinstance(reorder, bool)
    check.isinstance(validate, bool)

    def wrap(cls):
        def post_process(dcls):
            fn: types.FunctionType = cls.__init__
            argspec = inspect.getfullargspec(fn)
            nsb = codegen.NamespaceBuilder()

            lines = []

            def _type_validator(fld: dc.Field):
                from .validation import build_default_field_validation
                return build_default_field_validation(fld)

            for fld in fields(cls):
                vm = fld.metadata.get(ValidateMetadata)
                if callable(vm):
                    lines.append(f'{nsb.put(vm)}({fld.name})')
                elif vm is True or (vm is None and validate is True):
                    lines.append(f'{nsb.put(_type_validator(fld))}({fld.name})')
                elif vm is False or vm is None:
                    pass
                else:
                    raise TypeError(vm)

            if lines:
                cg = codegen.Codegen()
                cg(f'def {fn.__name__}({codegen.render_arg_spec(argspec, nsb)}:\n')
                with cg.indent():
                    cg(f'{nsb.put(fn)}({", ".join(a for a in argspec.args)})\n')
                    cg('\n'.join(lines))

                ns = dict(nsb)
                exec(str(cg), ns)
                cls.__init__ = ns[fn.__name__]

            return dcls

        if reorder:
            flds = _compose_fields(cls)
            new_flds = {k: v for d in [False, True] for k, v in flds.items() if _has_default(v) == d}
            if list(flds.keys()) != list(new_flds.keys()):
                _check_bases(cls.__mro__, frozen=frozen)
                anns = {name: fld.type for name, fld in new_flds.items()}
                ns = {'__annotations__': anns, ORIGIN_ATTR: cls, **new_flds}
                new_dc = dc.dataclass(type('_Reordered', (object,), ns), **fwd_kwargs)
                ret = post_process(type(cls.__name__, (new_dc, cls), {}))
                ret.__module__ = cls.__module__
                return ret

        return post_process(
            dc.dataclass(
                cls,
                init=init,
                repr=repr,
                eq=eq,
                order=order,
                unsafe_hash=unsafe_hash,
                frozen=frozen,
                **kwargs
            )
        )

    if _cls is None:
        return wrap
    return wrap(_cls)
