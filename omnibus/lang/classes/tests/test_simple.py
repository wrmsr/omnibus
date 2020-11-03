from .. import simple as simple_


def test_init_subclass():
    l = []

    class A:
        def __init_subclass__(cls):
            l.append((A, cls))
            super(A, cls).__init_subclass__()
    assert l == []

    class B(A):
        def __init_subclass__(cls):
            l.append((B, cls))
            super(B, cls).__init_subclass__()
    assert l == [(A, B)]
    l.clear()

    class C(B):
        def __init_subclass__(cls):
            l.append((C, cls))
            super(C, cls).__init_subclass__()
    assert l == [(B, C), (A, C)]


def test_inner():
    class A:

        def __init__(self, x):
            super().__init__()

            self.x = x

        class B(simple_.Inner['A']):

            def __init__(self, y):
                super().__init__()

                self.y = y
                self.xy = self._outer.x + y

    a = A(1)
    b = a.B(2)

    assert a.x == 1
    assert b.y == 2
    assert b._outer is a
    assert b.xy == 3


def test_singletons():
    for bcls in [simple_.Singleton, simple_.LazySingleton]:
        foo_init_calls = 0
        foo2_init_calls = 0

        class Foo(bcls):
            def __init__(self):
                super().__init__()
                nonlocal foo_init_calls
                foo_init_calls += 1

        assert Foo() is Foo()
        assert foo_init_calls == 1

        class Foo2(Foo):
            def __init__(self):
                super().__init__()
                nonlocal foo2_init_calls
                foo2_init_calls += 1

        assert Foo2() is Foo2()
        assert foo2_init_calls == 1
        assert foo_init_calls == 2
