import datetime
import typing as ta

import pytest

from .. import erasing as erasing_
from .. import functions as functions_
from .. import manifests as manifests_
from .. import registry as registry_
from .. import types as types_


K = ta.TypeVar('K')
V = ta.TypeVar('V')
T0 = ta.TypeVar('T0')
T1 = ta.TypeVar('T1')


def test_erasing_dispatch():
    disp = erasing_.ErasingDispatcher()
    disp[ta.Dict[K, V]] = 'dict'
    impl, manifest = disp[ta.Dict[int, str]]
    assert isinstance(manifest, types_.Manifest)
    assert manifest.spec.erased_cls is dict
    assert manifest.spec.args[0].cls is int
    assert manifest.spec.args[1].cls is str


@pytest.mark.parametrize('nolock', [False, True])
def test_function(nolock):
    @functions_.function(**({'lock': None} if nolock else {}))
    def f(val):
        return 'default'

    assert f(()) == 'default'
    assert f(1) == 'default'
    assert f('1') == 'default'
    assert f(b'1') == 'default'

    @f.register(int)  # noqa
    def _(val):
        return 'int'

    assert f(()) == 'default'
    assert f(1) == 'int'
    assert f('1') == 'default'
    assert f(b'1') == 'default'

    @f.register(str, bytes)  # noqa
    def _(val):
        return 'str/bytes'

    assert f(()) == 'default'
    assert f(1) == 'int'
    assert f('1') == 'str/bytes'
    assert f(b'1') == 'str/bytes'


def test_property():
    class A:
        fn = registry_.property_()

        @fn.register(object)
        def fn_object(self, o):
            return 'object'

        @fn.register(int)
        def fn_int(self, o):
            return 'int'

    class B(A):

        @A.fn.register
        def fn_str(self, o: str):
            return 'Bstr'

    class C(A):

        @A.fn.register(str)
        def fn_str(self, o):
            return 'Cstr'

    class D(C):

        @A.fn.register(str)
        def fn_str(self, o):
            return 'Dstr'

        @A.fn.register
        def fn_float(self, o: float):
            return 'Dfloat'

    assert A().fn(6) == 'int'
    assert A().fn(6.) == 'object'
    assert A().fn('hi') == 'object'

    for _ in range(2):
        a = A()
        for _ in range(2):
            assert a.fn(6) == 'int'
            assert a.fn(6.) == 'object'
            assert a.fn('hi') == 'object'

    assert B().fn(6) == 'int'
    assert B().fn(6.) == 'object'
    assert B().fn('hi') == 'Bstr'

    assert C().fn(6) == 'int'
    assert C().fn(6.) == 'object'
    assert C().fn('hi') == 'Cstr'

    assert D().fn(6) == 'int'
    assert D().fn(6.) == 'Dfloat'
    assert D().fn('hi') == 'Dstr'


def test_class():
    class A(registry_.Class):
        fn = registry_.property_()

        def fn(self, o: object):  # noqa
            return 'object'

        def fn(self, o: int):  # noqa
            return 'int'

    class B(A):

        def fn(self, o: str):
            return 'str'

    assert A().fn(0) == 'int'
    assert A().fn('') == 'object'

    assert B().fn(0) == 'int'
    assert B().fn('') == 'str'


def test_jsonifier():
    @functions_.function()
    def build_jsonizer(_: object):
        return lambda value: value

    @build_jsonizer.register(ta.Dict[K, V])
    def build_dict_jsonizer(_: ta.Dict[K, V], *, manifest: manifests_.Manifest):
        k, v = manifest.spec.args
        impl, manifest = build_jsonizer.dispatcher[k]
        kj = manifests_.inject_manifest(impl, manifest)(None)
        impl, manifest = build_jsonizer.dispatcher[v]
        vj = manifests_.inject_manifest(impl, manifest)(None)
        return lambda dct: {kj(K): vj(v) for k, v in dct.items()}

    @build_jsonizer.register(datetime.datetime)
    def build_datetime_jsonizer(_: datetime.datetime):
        return lambda dt: str(dt)

    impl, manifest = build_jsonizer.dispatcher[ta.Dict[datetime.datetime, str]]
    j = manifests_.inject_manifest(impl, manifest)(None)

    print(j({datetime.datetime.now(): '420'}))
