from .. import classes as classes_


def test_property():
    class A:
        fn = classes_.property_()

        @fn.registering(object)
        def fn_object(self, o):
            return 'object'

        @fn.registering(int)
        def fn_int(self, o):
            return 'int'

    class B(A):

        @A.fn.register
        def fn_str(self, o: str):
            return 'Bstr'

    class C(A):

        @A.fn.registering(str)
        def fn_str(self, o):
            return 'Cstr'

    class D(C):

        @A.fn.registering(str)
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
    class A(classes_.Class):
        fn = classes_.property_()

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