import datetime
import typing as ta

from .. import json


def test_codec():
    assert json.codec().decode(json.codec().encode({'a': 2})) == {'a': 2}


def test_serde():
    ser = json.build_serializer(ta.Dict[datetime.datetime, str])
    des = json.build_deserializer(ta.Dict[datetime.datetime, str])

    dct = {datetime.datetime.now(): '420'}
    sdct = ser(dct)
    print(sdct)
    ddct = des(sdct)
    print(ddct)
    assert ddct == dct
