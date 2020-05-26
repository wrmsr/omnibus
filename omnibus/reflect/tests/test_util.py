import collections.abc
import typing as ta

from .. import util as util_


T = ta.TypeVar('T')


def test_is_new_type():
    assert util_.is_new_type(ta.NewType('Barf', int))
    assert not util_.is_new_type(5)


def test_generic_bases():
    assert util_.generic_bases(ta.Dict[int, str]) == [object]

    class A:
        pass

    assert util_.generic_bases(A) == [object]

    class B(ta.Generic[T], A):
        pass

    assert util_.generic_bases(B) == [A]
    assert util_.generic_bases(B[int]) == [A]

    class C:
        pass

    class D(B[str], C):
        pass

    assert util_.generic_bases(D) == [B[str], C]


def test_instance_dependents():
    assert not util_.is_instance_dependent(int)

    class A(type):
        def __instancecheck__(self, instance):
            return True

    class B(metaclass=A):
        pass

    assert isinstance(5, B)
    assert util_.is_instance_dependent(B)

    class C:
        pass

    assert not util_.is_instance_dependent(C)


def test_subclass_dependents():
    assert not util_.is_dependent(int)
    assert not util_.is_subclass_dependent(collections.abc.Mapping)
    assert util_.is_abc_dependent(collections.abc.Mapping)

    class A(type):
        def __subclasscheck__(self, instance):
            return True

    class B(metaclass=A):
        pass

    assert issubclass(int, B)
    assert util_.is_subclass_dependent(B)

    class C:
        pass

    assert not util_.is_subclass_dependent(C)
