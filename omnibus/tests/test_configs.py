from .. import configs


def test_flattening():
    m = {
        'a': 1,
        'b': {
            'c': 2
        },
        'd': [
            'e',
            {
                'f': 3
            }
        ],
        'g': [
            [
                'a',
                'b'
            ],
            [
                'c',
                'd'
            ]
        ]
    }
    for f in [configs.Flattening(), configs.Flattening(index_open='((', index_close='))')]:
        fl = f.flatten(m)
        ufl = f.unflatten(fl)
        assert ufl == m


class DbConfig(configs.Config):
    url: str
    comment: str = configs.field(doc='comment')


class ExtraConfig(configs.Config):
    extra0: int = 5
    extra1 = 6
    extra2: int


class ExtraDbConfig(DbConfig, ExtraConfig):
    pass


class BytesUrlConfig(configs.Config):
    url: bytes


class BytesUrlDbConfig(BytesUrlConfig, DbConfig):
    pass


class MetadataConfig(configs.Config):
    thing = configs.field()


def test_configs():
    pass
