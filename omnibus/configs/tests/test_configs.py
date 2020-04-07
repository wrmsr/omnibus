import re
import textwrap

from .. import configs as configs_
from .. import dataclasses as dataclasses_  # noqa
from .. import dotenv as dotenv_
from .. import fields as fields_
from .. import flattening as flattening_
from ... import dataclasses as dc


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


def test_dotenv():
    parser = dotenv_.Parser(textwrap.dedent("""
    a=b
    c=d
    """))

    parser.read_pattern(re.compile(r'\s*'))
    m0 = parser.read_pattern(re.compile(r'\w+=\w+'))
    parser.read_pattern(re.compile(r'\s*'))
    m1 = parser.read_pattern(re.compile(r'\w+=\w+'))

    assert m0 is not None
    assert m1 is not None


def test_dataclasses():
    @dc.dataclass(frozen=True)
    class ConfigDc:
        username: str
        password: str

    # DcConfig = dataclasses_.build_dataclass_config(ConfigDc)
    # assert DcConfig is not None
