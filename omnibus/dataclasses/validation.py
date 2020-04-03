import collections.abc
import dataclasses as dc_
import typing as ta

from .. import check
from .. import dispatch
from .. import lang
from .. import reflect
from .virtual import VirtualClass


T = ta.TypeVar('T')
Field = dc_.Field
MISSING = dc_.MISSING

FieldValidator = ta.Callable[[T], None]
FieldValidation = ta.Callable[[Field], FieldValidator[T]]
DEFAULT_FIELD_VALIDATION_DISPATCHER: dispatch.Dispatcher[FieldValidation] = dispatch.CachingDispatcher(dispatch.ErasingDispatcher())  # noqa


def build_default_field_validation(fld: Field, type=MISSING) -> FieldValidator:
    impl, manifest = DEFAULT_FIELD_VALIDATION_DISPATCHER[type if type is not MISSING else (fld.type or object)]
    return dispatch.inject_manifest(impl, manifest)(fld)


@DEFAULT_FIELD_VALIDATION_DISPATCHER.registering(object, *lang.BUILTIN_SCALAR_ITERABLE_TYPES)
def default_field_validation(fld: Field, *, manifest: dispatch.Manifest) -> FieldValidator:
    cls = manifest.spec.erased_cls
    return lambda value: check.isinstance(value, cls, f'Invalid type for field {fld.name}')


@DEFAULT_FIELD_VALIDATION_DISPATCHER.registering(collections.abc.Iterable)
def iterable_default_field_validation(fld: Field, *, manifest: dispatch.Manifest) -> FieldValidator:
    cls = manifest.spec.erased_cls
    if isinstance(manifest.spec, reflect.NonGenericTypeSpec):
        return default_field_validation(fld, manifest=manifest)

    elif isinstance(manifest.spec, reflect.ParameterizedGenericTypeSpec):
        [e] = manifest.spec.args
        ev = build_default_field_validation(fld, e)

        def inner(value):
            check.isinstance(value, cls, f'Invalid type for field {fld.name}')
            for e in value:
                ev(e)

        return inner

    else:
        raise TypeError(manifest.spec)


@DEFAULT_FIELD_VALIDATION_DISPATCHER.registering(collections.abc.Mapping)
def mapping_default_field_validation(fld: Field, *, manifest: dispatch.Manifest) -> FieldValidator:
    cls = manifest.spec.erased_cls
    if isinstance(manifest.spec, reflect.NonGenericTypeSpec):
        return default_field_validation(fld, manifest=manifest)

    elif isinstance(manifest.spec, reflect.ParameterizedGenericTypeSpec):
        k, v = manifest.spec.args
        kv = build_default_field_validation(fld, k)
        vv = build_default_field_validation(fld, v)

        def inner(value):
            check.isinstance(value, cls, f'Invalid type for field {fld.name}')
            for k, v in value.items():
                kv(k)
                vv(v)

        return inner

    else:
        raise TypeError(manifest.spec)


@DEFAULT_FIELD_VALIDATION_DISPATCHER.registering(VirtualClass)
def dataclass_default_field_validation(fld: Field, *, manifest: dispatch.Manifest) -> FieldValidator:
    # FIXME: recurse?
    return default_field_validation(fld, manifest=manifest)
