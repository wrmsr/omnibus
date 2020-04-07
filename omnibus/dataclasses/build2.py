import dataclasses as dc
import functools
import inspect
import sys
import types
import typing as ta

from .. import check
from .. import codegen
from .. import lang
from .. import properties
from .defdecls import CheckerDefdcel
from .defdecls import DeriverDefdecl
from .defdecls import PostInitDefdecl
from .defdecls import ValidatorDefdecl


TypeT = ta.TypeVar('TypeT', bound=type, covariant=True)


def params(
        *,
        init=True,
        repr=True,
        eq=True,
        order=False,
        unsafe_hash=None,
        frozen=False,
):
    return dc._DataclassParams(init, repr, eq, order, unsafe_hash, frozen)


class ClassProcessor(ta.Generic[TypeT]):

    def __init__(
            self,
            cls: TypeT,
            params: dc._DataclassParams,
    ) -> None:
        super().__init__()

        self._cls = check.isinstance(cls, type)
        self._params = check.isinstance(params, dc._DataclassParams)

        self.check_invariants()

    @property
    def cls(self) -> TypeT:
        return self._cls

    @property
    def params(self) -> dc._DataclassParams:
        return self._params

    def check_invariants(self) -> None:
        if self.params.order and not self.params.eq:
            raise ValueError('eq must be true if order is true')

        any_frozen_base = any(getattr(b, dc._PARAMS).frozen for b in self.dataclass_rmro)
        if any_frozen_base:
            if any_frozen_base and not self.params.frozen:
                raise TypeError('cannot inherit non-frozen dataclass from a frozen one')
            if not any_frozen_base and self.params.frozen:
                raise TypeError('cannot inherit frozen dataclass from a non-frozen one')

    def set_new_attribute(self, name: str, value: ta.Any) -> bool:
        if name in self.cls.__dict__:
            return True
        setattr(self.cls, name, value)
        return False

    @properties.cached
    def globals(self) -> ta.MutableMapping[str, ta.Any]:
        if self.cls.__module__ in sys.modules:
            return sys.modules[self.cls.__module__].__dict__
        else:
            return {}

    @properties.cached
    def dataclass_rmro(self) -> ta.List[type]:
        return [b for b in self.cls.__mro__[-1:0:-1] if getattr(b, dc._FIELDS, None)]

    @properties.cached
    def fields(self) -> ta.Mapping[str, dc.Field]:
        fields = {}
        for b in self.dataclass_rmro:
            base_fields = getattr(b, dc._FIELDS, None)
            if base_fields:
                for f in base_fields.values():
                    fields[f.name] = f

        # Annotations that are defined in this class (not in base classes).  If __annotations__ isn't present, then this
        # class adds no new annotations.  We use this to compute fields that are added by this class.
        #
        # Fields are found from cls_annotations, which is guaranteed to be ordered.  Default values are from class
        # attributes, if a field has a default.  If the default value is a Field(), then it contains additional info
        # beyond (and possibly including) the actual default value.  Pseudo-fields ClassVars and InitVars are included,
        # despite the fact that they're not real fields.  That's dealt with later.
        cls_annotations = self.cls.__dict__.get('__annotations__', {})

        # Now find fields in our class.  While doing so, validate some things, and set the default values (as class
        # attributes) where we can.
        cls_fields = [dc._get_field(self.cls, name, type) for name, type in cls_annotations.items()]
        for f in cls_fields:
            fields[f.name] = f

            # If the class attribute (which is the default value for this field) exists and is of type 'Field', replace
            # it with the real default.  This is so that normal class introspection sees a real default value, not a
            # Field.
            if isinstance(getattr(self.cls, f.name, None), dc.Field):
                if f.default is dc.MISSING:
                    # If there's no default, delete the class attribute. This happens if we specify field(repr=False),
                    # for example (that is, we specified a field object, but no default value).  Also if we're using a
                    # default factory.  The class attribute should not be set at all in the post-processed class.
                    delattr(self.cls, f.name)
                else:
                    setattr(self.cls, f.name, f.default)

        # Do we have any Field members that don't also have annotations?
        for name, value in self.cls.__dict__.items():
            if isinstance(value, dc.Field) and name not in cls_annotations:
                raise TypeError(f'{name!r} is a field but has no type annotation')

        return fields

    def install_fields(self) -> None:
        setattr(self.cls, dc._FIELDS, self.fields)

    @properties.cached
    def field_maps_by_field_type(self) -> ta.Mapping[str, ta.Sequence[dc.Field]]:
        ret = {}
        for f in self.fields.values():
            ret.setdefault(f._field_type, {})[f.name] = f
        return ret

    @properties.cached
    def instance_fields(self) -> ta.List[dc.Field]:
        return list(self.field_maps_by_field_type.get(dc._FIELD, {}).values())

    def install_init(self) -> None:
        fn = InitBuilder(self)()
        self.set_new_attribute('__init__', fn)

    def install_repr(self) -> None:
        flds = [f for f in self.instance_fields if f.repr]
        self.set_new_attribute('__repr__', dc._repr_fn(flds, self.globals))

    def install_eq(self) -> None:
        flds = [f for f in self.instance_fields if f.compare]
        self_tuple = dc._tuple_str('self', flds)
        other_tuple = dc._tuple_str('other', flds)
        self.set_new_attribute('__eq__', dc._cmp_fn('__eq__', '==', self_tuple, other_tuple, globals=self.globals))

    def install_order(self) -> None:
        flds = [f for f in self.instance_fields if f.compare]
        self_tuple = dc._tuple_str('self', flds)
        other_tuple = dc._tuple_str('other', flds)
        for name, op in [
            ('__lt__', '<'),
            ('__le__', '<='),
            ('__gt__', '>'),
            ('__ge__', '>='),
        ]:
            if self.set_new_attribute(name, dc._cmp_fn(name, op, self_tuple, other_tuple, globals=self.globals)):
                raise TypeError(
                    f'Cannot overwrite attribute {name} in class {self.cls.__name__}. '
                    f'Consider using functools.total_ordering')

    def install_frozen(self) -> None:
        for fn in dc._frozen_get_del_attr(self.cls, self.instance_fields, self.globals):
            if self.set_new_attribute(fn.__name__, fn):
                raise TypeError(f'Cannot overwrite attribute {fn.__name__} in class {self.cls.__name__}')

    def maybe_install_hash(self) -> bool:
        # Was this class defined with an explicit __hash__?  Note that if __eq__ is defined in this class, then python
        # will automatically set __hash__ to None.  This is a heuristic, as it's possible that such a __hash__ == None
        # was not auto-generated, but it close enough.
        class_hash = self.cls.__dict__.get('__hash__', dc.MISSING)
        has_explicit_hash = not (class_hash is dc.MISSING or (class_hash is None and '__eq__' in self.cls.__dict__))
        hash_action = dc._hash_action[(
            bool(self.params.unsafe_hash),
            bool(self.params.eq),
            bool(self.params.frozen),
            has_explicit_hash,
        )]
        if hash_action:
            self.cls.__hash__ = hash_action(self.cls, self.instance_fields, self.globals)
            return True
        else:
            return False

    def maybe_install_doc(self) -> None:
        if not getattr(self.cls, '__doc__'):
            self.cls.__doc__ = (self.cls.__name__ + str(inspect.signature(self.cls)).replace(' -> None', ''))

    def __call__(self) -> TypeT:
        setattr(self.cls, dc._PARAMS, self.params)

        self.install_fields()

        if self.params.init:
            self.install_init()

        if self.params.repr:
            self.install_repr()

        if self.params.eq:
            self.install_eq()

        if self.params.order:
            self.install_order()

        if self.params.frozen:
            self.install_frozen()

        self.maybe_install_hash()

        self.maybe_install_doc()

        return self.cls


class InitBuilder:

    def __init__(self, cp: ClassProcessor) -> None:
        super().__init__()

        self._cp = check.isinstance(cp, ClassProcessor)

    @property
    def cp(self) -> ClassProcessor:
        return self._cp

    @staticmethod
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

    def post_process(self, validate=False):
        init_fn: types.FunctionType = self.cp.cls.__init__
        init_argspec = inspect.getfullargspec(init_fn)
        init_nsb = codegen.NamespaceBuilder(codegen.name_generator(unavailable_names=self.cp.fields))
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

        for vld in spec.defdecls[ValidatorDefdecl]:
            vld_args = self._get_fn_args(vld.fn)
            for arg in vld_args:
                check.in_(arg, self.cp.fields)
            init_lines.append(f'{init_nsb.put(vld.fn)}({", ".join(vld_args)})')

        for chk in spec.defdecls[CheckerDefdcel]:
            chk_args = self._get_fn_args(chk.fn)
            for arg in chk_args:
                check.in_(arg, self.cp.fields)

            def build_chk_exc(chk, chk_args, *args):
                if len(chk_args) != len(args):
                    raise TypeError(chk_args, args)
                raise CheckException({k: v for k, v in zip(chk_args, args)}, chk)

            bound_build_chk_exc = functools.partial(build_chk_exc, chk, chk_args)

            init_lines.append(
                f'if not {init_nsb.put(chk.fn)}({", ".join(chk_args)}): '
                f'raise {init_nsb.put(bound_build_chk_exc)}({", ".join(chk_args)})'
            )

        if spec.defdecls[PostInitDefdecl]:
            post_init_nsb = codegen.NamespaceBuilder(codegen.name_generator(unavailable_names={'args', 'kwargs'}))
            post_init_lines = []

            for pi in spec.defdecls[PostInitDefdecl]:
                post_init_lines.append(f'{post_init_nsb.put(pi.fn)}(self)')

            cg = codegen.Codegen()
            cg(f'def __post_init__(self, *args, **kwargs):\n')
            with cg.indent():
                post_init_fn = cls.__dict__.get('__post_init__')
                if post_init_fn is not None:
                    cg(f'{post_init_nsb.put(post_init_fn)}(self, *args, **kwargs)\n')
                elif hasattr(cls, '__post_init__'):
                    cg(f'{post_init_fn.put(super)}({post_init_fn.put(cls)}, self).__post_init__(*args, **kwargs)')
                else:
                    init_lines.append(f'self.__post_init__()')
                cg('\n'.join(post_init_lines))

            ns = dict(post_init_nsb)
            exec(str(cg), ns)
            cls.__post_init__ = ns['__post_init__']

        if init_lines:
            cg = codegen.Codegen()
            cg(f'def {init_fn.__name__}{codegen.render_arg_spec(init_argspec, init_nsb)}:\n')
            with cg.indent():
                cg(f'{init_nsb.put(init_fn)}({", ".join(a for a in init_argspec.args)})\n')
                cg('\n'.join(init_lines))

            ns = dict(init_nsb)
            exec(str(cg), ns)
            cls.__init__ = ns[init_fn.__name__]

        return dcls

    def __call__(self) -> None:
        # Does this class have a post-init function?
        has_post_init = hasattr(self.cp.cls, dc._POST_INIT_NAME)

        # Include InitVars and regular fields (so, not ClassVars).
        flds = [f for f in self.cp.fields.values() if f._field_type in (dc._FIELD, dc._FIELD_INITVAR)]

        self_name = '__dataclass_self__' if 'self' in self.cp.fields else 'self'

        # Make sure we don't have fields without defaults following fields with defaults.  This actually would be caught
        # when exec-ing the function source code, but catching it here gives a better error message, and future-proofs
        # us in case we build up the function using ast.
        seen_default = False
        for f in flds:
            # Only consider fields in the __init__ call.
            if f.init:
                if not (f.default is dc.MISSING and f.default_factory is dc.MISSING):
                    seen_default = True
                elif seen_default:
                    raise TypeError(f'non-default argument {f.name!r} follows default argument')

        locals = {f'_type_{f.name}': f.type for f in flds}
        locals.update({
            'MISSING': dc.MISSING,
            '_HAS_DEFAULT_FACTORY': dc._HAS_DEFAULT_FACTORY,
        })

        body_lines = []
        for f in flds:
            line = dc._field_init(f, self.cp.params.frozen, locals, self_name)
            # line is None means that this field doesn't require initialization (it's a pseudo-field).  Just skip it.
            if line:
                body_lines.append(line)

        # Does this class have a post-init function?
        if has_post_init:
            params_str = ','.join(f.name for f in flds if f._field_type is dc._FIELD_INITVAR)
            body_lines.append(f'{self_name}.{dc._POST_INIT_NAME}({params_str})')

        # If no body lines, use 'pass'.
        if not body_lines:
            body_lines = ['pass']

        return dc._create_fn(
            '__init__',
            [self_name] + [dc._init_param(f) for f in flds if f.init],
            body_lines,
            locals=locals,
            globals=self.cp.globals,
            return_type=None,
        )
