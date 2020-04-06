import dataclasses as dc
import functools
import inspect
import types
import typing as ta

from .. import check
from .. import codegen
from .specs import DataSpec
from .types import CheckException
from .types import ORIGIN_ATTR
from .types import ValidateMetadata


T = ta.TypeVar('T')


def _get_fn_args(fn) -> ta.List[str]:
    argspec = inspect.getfullargspec(fn)
    if (
            argspec.varargs or
            argspec.varkw or
            argspec.defaults or
            argspec.kwonlyargs or
            argspec.kwonlydefaults
    ):
        raise TypeError(fn)
    return list(argspec.args)


def post_process(
        cls,
        dcls,
        *,
        validate=False,
):
    spec = DataSpec(dcls)

    init_fn: types.FunctionType = cls.__init__
    init_argspec = inspect.getfullargspec(init_fn)
    init_nsb = codegen.NamespaceBuilder(codegen.name_generator(unavailable_names=spec.fields_by_name))
    init_lines = []

    def _type_validator(fld: dc.Field):
        from .validation import build_default_field_validation
        return build_default_field_validation(fld)

    for fld in spec.fields:
        vld_md = fld.metadata.get(ValidateMetadata)
        if callable(vld_md):
            init_lines.append(f'{init_nsb.put(vld_md)}({fld.name})')
        elif vld_md is True or (vld_md is None and validate is True):
            init_lines.append(f'{init_nsb.put(_type_validator(fld))}({fld.name})')
        elif vld_md is False or vld_md is None:
            pass
        else:
            raise TypeError(vld_md)

    for vld in spec.validators:
        vld_args = _get_fn_args(vld)
        for arg in vld_args:
            check.in_(arg, spec.fields_by_name)
        init_lines.append(f'{init_nsb.put(vld)}({", ".join(vld_args)})')

    for chk in spec.checkers:
        chk_args = _get_fn_args(chk)
        for arg in chk_args:
            check.in_(arg, spec.fields_by_name)

        def build_chk_exc(chk, chk_args, *args):
            if len(chk_args) != len(args):
                raise TypeError(chk_args, args)
            raise CheckException({k: v for k, v in zip(chk_args, args)}, chk)
        bound_build_chk_exc = functools.partial(build_chk_exc, chk, chk_args)

        init_lines.append(
            f'if not {init_nsb.put(chk)}({", ".join(chk_args)}): '
            f'raise {init_nsb.put(bound_build_chk_exc)}({", ".join(chk_args)})'
        )

    if init_lines:
        cg = codegen.Codegen()
        cg(f'def {init_fn.__name__}({codegen.render_arg_spec(init_argspec, init_nsb)}:\n')
        with cg.indent():
            cg(f'{init_nsb.put(init_fn)}({", ".join(a for a in init_argspec.args)})\n')
            cg('\n'.join(init_lines))

        ns = dict(init_nsb)
        exec(str(cg), ns)
        cls.__init__ = ns[init_fn.__name__]

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
