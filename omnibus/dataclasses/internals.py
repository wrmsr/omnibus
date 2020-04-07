import dataclasses as dc


FIELDS = dc._FIELDS
PARAMS = dc._PARAMS

POST_INIT_NAME = dc._POST_INIT_NAME

HAS_DEFAULT_FACTORY = dc._HAS_DEFAULT_FACTORY

FIELD = dc._FIELD
FIELD_CLASSVAR = dc._FIELD_CLASSVAR
FIELD_INITVAR = dc._FIELD_INITVAR

DataclassParams = dc._DataclassParams

is_dataclass_instance = dc._is_dataclass_instance

get_field = dc._get_field
repr_fn = dc._repr_fn
cmp_fn = dc._cmp_fn
frozen_get_del_attr = dc._frozen_get_del_attr
hash_action = dc._hash_action
field_init = dc._field_init
tuple_str = dc._tuple_str
create_fn = dc._create_fn
init_param = dc._init_param


def get_field_type(fld: dc.Field) -> dc._FIELD_BASE:
    return fld._field_type
