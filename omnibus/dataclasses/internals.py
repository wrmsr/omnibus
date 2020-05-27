import dataclasses as dc

from .. import lang


def _patch_missing_ctor():
    # dc.asdict uses copy.deepcopy which instantiates new _MISSING_TYPE objects which do not pass the 'foo is MISSING'
    # checks used throughout dataclasses code. Code should not depend on this behavior but it is a debugging landmine.
    def _MISSING_TYPE_new(cls):
        return dc.MISSING
    dc._MISSING_TYPE.__new__ = _MISSING_TYPE_new


FIELDS = dc._FIELDS
PARAMS = dc._PARAMS

POST_INIT_NAME = dc._POST_INIT_NAME


class FieldType(lang.ValueEnum):
    INSTANCE = dc._FIELD
    CLASS = dc._FIELD_CLASSVAR
    INIT = dc._FIELD_INITVAR


def get_field_type(fld: dc.Field) -> FieldType:
    return fld._field_type


DataclassParams = dc._DataclassParams


tuple_str = dc._tuple_str
repr_fn = dc._repr_fn
frozen_get_del_attr = dc._frozen_get_del_attr
cmp_fn = dc._cmp_fn
get_field = dc._get_field
hash_action = dc._hash_action
is_dataclass_instance = dc._is_dataclass_instance
