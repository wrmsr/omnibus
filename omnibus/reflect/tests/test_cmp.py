class A:
    pass


class B:
    pass


class C(A):
    pass


class D(A):
    pass


class E(D):
    pass


def test_is_subclass():
    def isc(sub, sup):
        return rfl.get_spec(sup).accept(IsSubclassVisitor(rfl.get_spec(sub)))

    assert isc(int, int)
    assert isc(int, object)
    assert isc(int, ta.Any)

