from .. import lang


ORIGIN_ATTR = '__dataclass_origin__'
FIELDS_VALIDATORS_ATTR = '__dataclass_fields_validators__'
VALIDATORS_ATTR = '__dataclass_validators__'


class SizeMetadata(lang.Marker):
    pass


class ValidateMetadata(lang.Marker):
    pass


class CoerceMetadata(lang.Marker):
    pass


class DeriveMetadata(lang.Marker):
    pass
