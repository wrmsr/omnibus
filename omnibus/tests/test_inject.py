import dataclasses as dc
import typing as ta

import pytest

from .. import inject as inj


def test_base():
    binder = inj.Binder()

    class C:
        def __init__(self, x: int) -> None:
            super().__init__()
            self.x = x

    class D(C):
        pass

    # binder.bind_callable(lambda: 420, key=Key(int))
    binder.bind(int, to_instance=420)

    # binder.bind_callable(lambda x: D(x), key=Key(D), inputs={'x': Key(int)}, in_=EagerSingletonScope)
    binder.bind(D, as_eager_singleton=True)

    # injector.install(lambda x: C(x), inputs={'x': Key(int)}, key=Key(C))

    class E:
        pass

    class F(E):
        pass

    class G(E):
        pass

    binder.bind(G)
    binder.bind(F, to=G)

    injector = inj.Injector(binder, config=inj.Injector.Config(enable_jit_bindings=True))

    c = injector.get_instance(inj.Key(C))
    assert isinstance(c, C)
    assert c.x == 420
    assert injector.get_instance(inj.Key(C)) is not c

    d = injector.get_instance(inj.Key(D))
    assert isinstance(d, D)
    assert d.x == 420
    assert injector.get_instance(inj.Key(D)) is d

    f = injector.get_instance(F)
    assert isinstance(f, G)


def test_box():
    Name = inj.make_box('Name', str)
    Title = inj.make_box('Title', str)

    def make_title(name: Name) -> Title:
        return Title(name.value + ' title')

    binder = inj.Binder()
    binder.bind(Name('some name'))
    binder.bind_callable(make_title)

    injector = inj.Injector(binder)

    name = injector.get_instance(Name)
    assert isinstance(name, Name)
    assert name.value == 'some name'

    title = injector.get_instance(Title)
    assert isinstance(title, Title)
    assert title.value == 'some name title'


def test_annotation():
    @inj.annotate('title', name='name')
    def make_title(name: str) -> str:
        return name + ' title'

    binder = inj.Binder()
    binder.bind('some name', annotated_with='name')
    binder.bind_callable(make_title)

    injector = inj.Injector(binder)

    name = injector.get_instance(inj.Key(str, 'name'))
    assert name == 'some name'

    title = injector.get_instance(inj.Key(str, 'title'))
    assert title == 'some name title'


def test_provider():
    binder = inj.Binder()

    binder.bind(5)
    binder.bind(object, to_provider=int)

    injector = inj.Injector(binder)

    assert injector.get_instance(object) == 5


def test_default():
    @inj.annotate('title', name='name')
    def make_title(name: str = 'default name') -> str:
        return name + ' title'

    binder = inj.Binder()
    binder.bind_callable(make_title)

    injector = inj.Injector(binder)

    title = injector.get_instance(inj.Key(str, 'title'))
    assert title == 'default name title'


def test_set():
    binder = inj.Binder()
    binder.new_set_binder(int).bind(to_instance=4)
    binder.new_set_binder(int).bind(to_instance=5)

    injector = inj.Injector(binder)

    s = injector.get_instance(ta.Set[int])
    assert s == {4, 5}


def test_dict():
    binder = inj.Binder()
    binder.new_dict_binder(int, str).bind(4, to_instance='four')
    binder.new_dict_binder(int, str).bind(5, to_instance='five')

    injector = inj.Injector(binder)

    s = injector.get_instance(ta.Dict[int, str])
    assert s == {4: 'four', 5: 'five'}


def test_child():
    binder = inj.Binder()
    binder.bind(420)

    injector = inj.Injector(binder)
    child_injector = injector.create_child()

    assert injector.get_instance(int) == 420
    assert child_injector.get_instance(int) == 420


def test_child2():
    binder = inj.Binder()

    injector = inj.Injector(binder, config=inj.Injector.Config(enable_jit_bindings=True))
    child_injector = injector.create_child()

    assert child_injector.get_instance(int) == 0
    with pytest.raises(inj.InjectionBlacklistedKeyError):
        injector.get_instance(int)


def test_private():
    class A:
        pass

    class B:
        pass

    class C(B):
        def __init__(self, a: A) -> None:
            self.a = a

    class D:
        def __init__(self, b: B) -> None:
            self.b = b

    private_binder = inj.PrivateBinder()
    private_binder.bind(A)
    private_binder.bind(C)  # diff
    private_binder.bind(B, to=C)
    private_binder.expose(B)

    binder = inj.Binder()
    binder.bind(D)

    injector = inj.Injector(private_binder, binder)
    d = injector.get_instance(D)
    assert isinstance(d, D)
    assert isinstance(d.b, C)
    assert isinstance(d.b.a, A)

    with pytest.raises(inj.InjectionBlacklistedKeyError):
        injector.get_instance(A)

    with pytest.raises(inj.InjectionBlacklistedKeyError):
        injector.get_instance(C)


def test_dataclasses():
    @dc.dataclass()
    class C:
        x: int

    binder = inj.Binder()
    binder.bind(420)
    binder.bind(C)

    injector = inj.Injector(binder)
    c = injector.get_instance(C)
    assert isinstance(c, C)
    assert c.x == 420
