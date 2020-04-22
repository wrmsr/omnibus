import abc

import pytest

from .. import restrict as restrict_
from .. import virtual as virtual_


def test_protocol():
    class P(virtual_.Protocol):
        @restrict_.abstract
        def f(self):
            raise NotImplementedError()

    class A:
        def f(self):
            pass

    class B:
        def g(self):
            pass

    assert issubclass(A, P)
    assert not issubclass(B, P)
    assert isinstance(A(), P)
    assert not isinstance(B(), P)

    @P
    class C:
        def f(self):
            pass

    with pytest.raises(virtual_.ProtocolException):
        @P
        class D:
            pass


def test_intersection():
    class Appendable(restrict_.Abstract):

        @abc.abstractmethod
        def append(self, obj):
            raise NotImplementedError

    class Clearable(restrict_.Abstract):

        @abc.abstractmethod
        def clear(self):
            raise NotImplementedError

    class AppendableClearable(Appendable, Clearable, virtual_.Intersection):
        pass

    class Thing0(Appendable, Clearable):
        def append(self, other): pass
        def clear(self) -> None: pass

    class Thing1(Appendable, Clearable):
        def append(self, other): pass
        def clear(self) -> None: pass

    class Thing2(Appendable):
        def append(self, other): pass
        def clear(self) -> None: pass

    class Thing3(Clearable):
        def append(self, other): pass
        def clear(self) -> None: pass

    assert issubclass(Thing0, AppendableClearable)
    assert issubclass(Thing0, Appendable)
    assert issubclass(Thing0, Clearable)

    assert issubclass(Thing1, AppendableClearable)
    assert issubclass(Thing1, Appendable)
    assert issubclass(Thing1, Clearable)

    assert not issubclass(Thing2, AppendableClearable)
    assert issubclass(Thing2, Appendable)
    assert not issubclass(Thing2, Clearable)

    assert not issubclass(Thing3, AppendableClearable)
    assert not issubclass(Thing3, Appendable)
    assert issubclass(Thing3, Clearable)

    class Hashable(restrict_.Abstract):

        @abc.abstractmethod
        def hash(self) -> int:
            raise NotImplementedError

    class AppendableClearableHashable(AppendableClearable, Hashable, virtual_.Intersection):
        pass

    class Thing4(Thing0, Hashable):
        def hash(self) -> int: pass

    assert issubclass(Thing4, AppendableClearableHashable)
    assert issubclass(Thing4, Hashable)

    assert not issubclass(Thing0, Hashable)
    assert not issubclass(Thing1, Hashable)
    assert not issubclass(Thing2, Hashable)
    assert not issubclass(Thing3, Hashable)

    with pytest.raises(TypeError):
        class AppendableClearableHashable2(AppendableClearable, Hashable):
            pass