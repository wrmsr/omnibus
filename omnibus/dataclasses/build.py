import dataclasses as dc
import inspect
import types
import typing as ta

from .. import check
from .. import codegen
from .api import fields
from .types import ORIGIN_ATTR
from .types import ValidateMetadata


T = ta.TypeVar('T')


def post_process(
        cls,
        dcls,
        *,
        validate=False,
):
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


def _has_default(fld: dc.Field) -> bool:
    return fld.default is not dc.MISSING or fld.default_factory is not dc.MISSING


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

    post_process_kwargs = dict(
        validate=validate,
    )

    check.isinstance(reorder, bool)
    check.isinstance(validate, bool)

    def build(cls):
        if reorder:
            flds = _compose_fields(cls)
            new_flds = {k: v for d in [False, True] for k, v in flds.items() if _has_default(v) == d}
            if list(flds.keys()) != list(new_flds.keys()):
                _check_bases(cls.__mro__, frozen=frozen)
                anns = {name: fld.type for name, fld in new_flds.items()}
                ns = {'__annotations__': anns, ORIGIN_ATTR: cls, **new_flds}
                new_dc = dc.dataclass(type('_Reordered', (object,), ns), **fwd_kwargs)
                ret = post_process(cls, type(cls.__name__, (new_dc, cls), {}), **post_process_kwargs)
                ret.__module__ = cls.__module__
                return ret

        dcls = dc.dataclass(cls, **fwd_kwargs, **kwargs)
        return post_process(cls, dcls, **post_process_kwargs)

    if _cls is None:
        return build
    return build(_cls)
