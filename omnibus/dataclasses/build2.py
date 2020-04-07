import dataclasses as dc
import inspect
import sys
import typing as ta

from .. import check
from .. import lang
from .. import properties


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

        if self._params.order and not self._params.eq:
            raise ValueError('eq must be true if order is true')

    def _set_new_attribute(self, name: str, value: ta.Any) -> bool:
        if name in self._cls.__dict__:
            return True
        setattr(self._cls, name, value)
        return False

    @properties.cached
    def _globals(self) -> ta.MutableMapping[str, ta.Any]:
        if self._cls.__module__ in sys.modules:
            return sys.modules[self._cls.__module__].__dict__
        else:
            return {}

    @properties.cached
    def _dataclass_rmro(self) -> ta.List[type]:
        return [b for b in self._cls.__mro__[-1:0:-1] if getattr(b, dc._FIELDS, None)]

    def _check_frozen_bases(self) -> None:
        any_frozen_base = any(getattr(b, dc._PARAMS).frozen for b in self._dataclass_rmro)
        if any_frozen_base:
            if any_frozen_base and not self._params.frozen:
                raise TypeError('cannot inherit non-frozen dataclass from a frozen one')
            if not any_frozen_base and self._params.frozen:
                raise TypeError('cannot inherit frozen dataclass from a non-frozen one')

    @properties.cached
    def _fields(self) -> ta.Mapping[str, dc.Field]:
        fields = {}
        for b in self._dataclass_rmro:
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
        cls_annotations = self._cls.__dict__.get('__annotations__', {})

        # Now find fields in our class.  While doing so, validate some things, and set the default values (as class
        # attributes) where we can.
        cls_fields = [dc._get_field(self._cls, name, type) for name, type in cls_annotations.items()]
        for f in cls_fields:
            fields[f.name] = f

            # If the class attribute (which is the default value for this field) exists and is of type 'Field', replace
            # it with the real default.  This is so that normal class introspection sees a real default value, not a
            # Field.
            if isinstance(getattr(self._cls, f.name, None), dc.Field):
                if f.default is dc.MISSING:
                    # If there's no default, delete the class attribute. This happens if we specify field(repr=False),
                    # for example (that is, we specified a field object, but no default value).  Also if we're using a
                    # default factory.  The class attribute should not be set at all in the post-processed class.
                    delattr(self._cls, f.name)
                else:
                    setattr(self._cls, f.name, f.default)

        # Do we have any Field members that don't also have annotations?
        for name, value in self._cls.__dict__.items():
            if isinstance(value, dc.Field) and not name in cls_annotations:
                raise TypeError(f'{name!r} is a field but has no type annotation')

        return fields

    def _install_fields(self) -> None:
        setattr(self._cls, dc._FIELDS, self._fields)

    @properties.cached
    def _field_maps_by_field_type(self) -> ta.Mapping[str, ta.Sequence[dc.Field]]:
        ret = {}
        for f in self._fields.values():
            ret.setdefault(f._field_type, {})[f.name] = f
        return ret

    @properties.cached
    def _instance_fields(self) -> ta.List[dc.Field]:
        return list(self._field_maps_by_field_type.get(dc._FIELD, {}).values())

    def _install_init(self) -> None:
        # Does this class have a post-init function?
        has_post_init = hasattr(self._cls, dc._POST_INIT_NAME)

        # Include InitVars and regular fields (so, not ClassVars).
        flds = [f for f in self._fields.values() if f._field_type in (dc._FIELD, dc._FIELD_INITVAR)]
        self._set_new_attribute(
            '__init__',
            dc._init_fn(
                flds,
                self._params.frozen,
                has_post_init,
                '__dataclass_self__' if 'self' in self._fields
                else 'self',
                self._globals,
            )
        )

    def _install_repr(self) -> None:
        flds = [f for f in self._instance_fields if f.repr]
        self._set_new_attribute('__repr__', dc._repr_fn(flds, self._globals))

    def _install_eq(self) -> None:
        flds = [f for f in self._instance_fields if f.compare]
        self_tuple = dc._tuple_str('self', flds)
        other_tuple = dc._tuple_str('other', flds)
        self._set_new_attribute('__eq__', dc._cmp_fn('__eq__', '==', self_tuple, other_tuple, globals=self._globals))

    def _install_order(self) -> None:
        flds = [f for f in self._instance_fields if f.compare]
        self_tuple = dc._tuple_str('self', flds)
        other_tuple = dc._tuple_str('other', flds)
        for name, op in [
            ('__lt__', '<'),
            ('__le__', '<='),
            ('__gt__', '>'),
            ('__ge__', '>='),
        ]:
            if self._set_new_attribute(name, dc._cmp_fn(name, op, self_tuple, other_tuple, globals=self._globals)):
                raise TypeError(
                    f'Cannot overwrite attribute {name} in class {self._cls.__name__}. Consider using functools.total_ordering')

    def _install_frozen(self) -> None:
        for fn in dc._frozen_get_del_attr(self._cls, self._instance_fields, self._globals):
            if self._set_new_attribute(fn.__name__, fn):
                raise TypeError(f'Cannot overwrite attribute {fn.__name__} in class {self._cls.__name__}')

    def _maybe_install_doc(self) -> None:
        if not getattr(self._cls, '__doc__'):
            self._cls.__doc__ = (self._cls.__name__ + str(inspect.signature(self._cls)).replace(' -> None', ''))

    def _maybe_install_hash(self) -> bool:
        # Was this class defined with an explicit __hash__?  Note that if __eq__ is defined in this class, then python
        # will automatically set __hash__ to None.  This is a heuristic, as it's possible that such a __hash__ == None
        # was not auto-generated, but it close enough.
        class_hash = self._cls.__dict__.get('__hash__', dc.MISSING)
        has_explicit_hash = not (class_hash is dc.MISSING or (class_hash is None and '__eq__' in self._cls.__dict__))
        hash_action = dc._hash_action[(
            bool(self._params.unsafe_hash),
            bool(self._params.eq),
            bool(self._params.frozen),
            has_explicit_hash,
        )]
        if hash_action:
            self._cls.__hash__ = hash_action(self._cls, self._instance_fields, self._globals)
            return True
        else:
            return False

    def __call__(self) -> TypeT:
        setattr(self._cls, dc._PARAMS, self._params)

        self._check_frozen_bases()

        self._install_fields()

        if self._params.init:
            self._install_init()

        if self._params.repr:
            self._install_repr()

        if self._params.eq:
            self._install_eq()

        if self._params.order:
            self._install_order()

        if self._params.frozen:
            self._install_frozen()

        self._maybe_install_hash()
        self._maybe_install_doc()

        return self._cls
