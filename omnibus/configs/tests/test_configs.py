from .. import flattening as flattening_
from .. import configs as configs_
from .. import fields as fields_


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
    for f in [flattening_.Flattening(), flattening_.Flattening(index_open='((', index_close='))')]:
        fl = f.flatten(m)
        ufl = f.unflatten(fl)
        assert ufl == m


class DbConfig(configs_.Config):
    url: str
    comment: str = fields_.field(doc='comment')


class ExtraConfig(configs_.Config):
    extra0: int = 5
    extra1 = 6
    extra2: int


class ExtraDbConfig(DbConfig, ExtraConfig):
    pass


class BytesUrlConfig(configs_.Config):
    url: bytes


class BytesUrlDbConfig(BytesUrlConfig, DbConfig):
    pass


class MetadataConfig(configs_.Config):
    thing = fields_.field()


def test_configs():
    db_config = DbConfig.of(
        url='a url',
        comment='a comment',
    )
    assert db_config.url == 'a url'
