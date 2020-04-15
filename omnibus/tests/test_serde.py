import datetime
import typing as ta

from .. import lang
from .. import serde


def test_mapping_serde():
    ser = serde.build_serializer(ta.Dict[datetime.datetime, str])
    des = serde.build_deserializer(ta.Dict[datetime.datetime, str])

    dct = {datetime.datetime.now(): '420'}
    sdct = ser(dct)
    print(sdct)
    assert isinstance(list(sdct.keys())[0], str)
    ddct = des(sdct)
    print(ddct)
    assert ddct == dct


def test_set_serde():
    ser = serde.build_serializer(ta.Set[datetime.datetime])
    des = serde.build_deserializer(ta.Set[datetime.datetime])

    st = {datetime.datetime.now()}
    sst = ser(st)
    print(sst)
    assert isinstance(sst, list)
    assert isinstance(sst[0], str)
    dst = des(sst)
    print(dst)
    assert dst == st


def test_redact_serde():
    ser = serde.build_serializer(lang.Redacted[datetime.datetime])
    des = serde.build_deserializer(lang.Redacted[datetime.datetime])

    st = lang.redact(datetime.datetime.now())
    sst = ser(st)
    print(sst)
    assert isinstance(sst, str)
    dst = des(sst)
    print(dst)
    assert dst == st
