import dataclasses as dc
import inspect
import sys

from .. import check


def params(
        *,
        init=None,
        repr=None,
        eq=None,
        order=None,
        unsafe_hash=None,
        frozen=None,
):
    return dc._DataclassParams(init, repr, eq, order, unsafe_hash, frozen)


class ClassProcessor:

    def __init__(
            self,
            cls,
            params: dc._DataclassParams,
    ) -> None:
        super().__init__()

        self._cls = check.isinstance(cls, type)
        self._params = check.isinstance(params, dc._DataclassParams)

    def __call__(self, init, repr, eq, order, unsafe_hash, frozen):
        fields = {}

        if self._cls.__module__ in sys.modules:
            globals = sys.modules[self._cls.__module__].__dict__
        else:
            globals = {}

        setattr(self._cls, dc._PARAMS, self._params)

        any_frozen_base = False
        has_dataclass_bases = False
        for b in self._cls.__mro__[-1:0:-1]:
            # Only process classes that have been processed by our decorator.  That is, they have a _FIELDS attribute.
            base_fields = getattr(b, dc._FIELDS, None)
            if base_fields:
                has_dataclass_bases = True
                for f in base_fields.values():
                    fields[f.name] = f
                if getattr(b, dc._PARAMS).frozen:
                    any_frozen_base = True

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
        cls_fields = [_get_field(self._cls, name, type) for name, type in cls_annotations.items()]
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

        # Check rules that apply if we are derived from any dataclasses.
        if has_dataclass_bases:
            # Raise an exception if any of our bases are frozen, but we're not.
            if any_frozen_base and not self._params.frozen:
                raise TypeError('cannot inherit non-frozen dataclass from a frozen one')

            # Raise an exception if we're frozen, but none of our bases are.
            if not any_frozen_base and self._params.frozen:
                raise TypeError('cannot inherit frozen dataclass from a non-frozen one')

        # Remember all of the fields on our class (including bases).  This also marks this class as being a dataclass.
        setattr(self._cls, dc._FIELDS, fields)

        # Was this class defined with an explicit __hash__?  Note that if __eq__ is defined in this class, then python
        # will automatically set __hash__ to None.  This is a heuristic, as it's possible that such a __hash__ == None
        # was not auto-generated, but it close enough.
        class_hash = self._cls.__dict__.get('__hash__', dc.MISSING)
        has_explicit_hash = not (class_hash is dc.MISSING or (class_hash is None and '__eq__' in self._cls.__dict__))

        # If we're generating ordering methods, we must be generating the eq methods.
        if self._params.order and not self._params.eq:
            raise ValueError('eq must be true if order is true')

        if self._params.init:
            # Does this class have a post-init function?
            has_post_init = hasattr(self._cls, dc._POST_INIT_NAME)

            # Include InitVars and regular fields (so, not ClassVars).
            flds = [f for f in fields.values() if f._field_type in (dc._FIELD, dc._FIELD_INITVAR)]
            _set_new_attribute(
                self._cls,
                '__init__',
                _init_fn(
                    flds,
                    self._params.frozen,
                    has_post_init,
                    '__dataclass_self__' if 'self' in fields
                    else 'self',
                    globals,
                )
            )

        field_list = [f for f in fields.values() if f._field_type is dc._FIELD]

        if self._params.repr:
            flds = [f for f in field_list if f.repr]
            _set_new_attribute(self._cls, '__repr__', _repr_fn(flds, globals))

        if self._params.eq:
            flds = [f for f in field_list if f.compare]
            self_tuple = _tuple_str('self', flds)
            other_tuple = _tuple_str('other', flds)
            _set_new_attribute(self._cls, '__eq__', _cmp_fn('__eq__', '==', self_tuple, other_tuple, globals=globals))

        if self._params.order:
            flds = [f for f in field_list if f.compare]
            self_tuple = _tuple_str('self', flds)
            other_tuple = _tuple_str('other', flds)
            for name, op in [
                ('__lt__', '<'),
                ('__le__', '<='),
                ('__gt__', '>'),
                ('__ge__', '>='),
            ]:
                if _set_new_attribute(self._cls, name, _cmp_fn(name, op, self_tuple, other_tuple, globals=globals)):
                    raise TypeError(
                        f'Cannot overwrite attribute {name} in class {self._cls.__name__}. Consider using functools.total_ordering')

        if self._params.frozen:
            for fn in _frozen_get_del_attr(self._cls, field_list, globals):
                if _set_new_attribute(self._cls, fn.__name__, fn):
                    raise TypeError(f'Cannot overwrite attribute {fn.__name__} in class {self._cls.__name__}')

        hash_action = _hash_action[bool(self._params.unsafe_hash), bool(self._params.eq), bool(self._params.frozen), has_explicit_hash]
        if hash_action:
            self._cls.__hash__ = hash_action(self._cls, field_list, globals)

        if not getattr(self._cls, '__doc__'):
            self._cls.__doc__ = (self._cls.__name__ + str(inspect.signature(self._cls)).replace(' -> None', ''))

        return self._cls
