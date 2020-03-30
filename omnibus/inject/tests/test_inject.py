import dataclasses as dc
import typing as ta

import pytest

from .. import bind as bind_
from .. import inject as inject_
from .. import types as types_


def test_base():
    binder = bind_.create_binder()

    class C:
        def __init__(self, x: int) -> None:
            super().__init__()
            self.x = x

    class D(C):
        pass

    # binder.bind_callable(lambda: 420, key=Key(int))
    binder.bind(int, to_instance=420)

    # binder.bind_callable(lambda x: D(x), key=Key(D), kwargs={'x': Key(int)}, in_=EagerSingletonScope)
    binder.bind(D, as_eager_singleton=True)

    # injector.install(lambda x: C(x), kwargs={'x': Key(int)}, key=Key(C))

    class E:
        pass

    class F(E):
        pass

    class G(E):
        pass

    binder.bind(G)
    binder.bind(F, to=G)

    injector = inject_.create_injector(binder, config=inject_.InjectorConfig(enable_jit_bindings=True))

    c = injector.get_instance(types_.Key(C))
    assert isinstance(c, C)
    assert c.x == 420
    assert injector.get_instance(types_.Key(C)) is not c

    d = injector.get_instance(types_.Key(D))
    assert isinstance(d, D)
    assert d.x == 420
    assert injector.get_instance(types_.Key(D)) is d

    f = injector.get_instance(F)
    assert isinstance(f, G)


def test_box():
    Name = bind_.make_box('Name', str)
    Title = bind_.make_box('Title', str)

    def make_title(name: Name) -> Title:
        return Title(name.value + ' title')

    binder = bind_.create_binder()
    binder.bind(Name('some name'))
    binder.bind_callable(make_title)

    injector = inject_.create_injector(binder)

    name = injector.get_instance(Name)
    assert isinstance(name, Name)
    assert name.value == 'some name'

    title = injector.get_instance(Title)
    assert isinstance(title, Title)
    assert title.value == 'some name title'


def test_annotation():
    @bind_.annotate('title', name='name')
    def make_title(name: str) -> str:
        return name + ' title'

    binder = bind_.create_binder()
    binder.bind('some name', annotated_with='name')
    binder.bind_callable(make_title)

    injector = inject_.create_injector(binder)

    name = injector.get_instance(types_.Key(str, 'name'))
    assert name == 'some name'

    title = injector.get_instance(types_.Key(str, 'title'))
    assert title == 'some name title'


def test_provider():
    binder = bind_.create_binder()

    binder.bind(5)
    binder.bind(object, to_provider=int)

    injector = inject_.create_injector(binder)

    assert injector.get_instance(object) == 5


def test_default():
    @bind_.annotate('title', name='name')
    def make_title(name: str = 'default name') -> str:
        return name + ' title'

    binder = bind_.create_binder()
    binder.bind_callable(make_title)

    injector = inject_.create_injector(binder)

    title = injector.get_instance(types_.Key(str, 'title'))
    assert title == 'default name title'


def test_set():
    binder = bind_.create_binder()
    binder.new_set_binder(int).bind(to_instance=4)
    binder.new_set_binder(int).bind(to_instance=5)

    injector = inject_.create_injector(binder)

    s = injector.get_instance(ta.Set[int])
    assert s == {4, 5}


def test_dict():
    binder = bind_.create_binder()
    binder.new_dict_binder(int, str).bind(4, to_instance='four')
    binder.new_dict_binder(int, str).bind(5, to_instance='five')

    injector = inject_.create_injector(binder)

    s = injector.get_instance(ta.Dict[int, str])
    assert s == {4: 'four', 5: 'five'}


def test_child():
    binder = bind_.create_binder()
    binder.bind(420)

    injector = inject_.create_injector(binder)
    child_injector = injector.create_child()

    assert injector.get_instance(int) == 420
    assert child_injector.get_instance(int) == 420


def test_child2():
    binder = bind_.create_binder()

    injector = inject_.create_injector(binder, config=types_.InjectorConfig(enable_jit_bindings=True))
    child_injector = injector.create_child()

    assert child_injector.get_instance(int) == 0
    with pytest.raises(types_.InjectionBlacklistedKeyError):
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

    private_binder = bind_.create_private_binder()
    private_binder.bind(A)
    private_binder.bind(C)  # diff
    private_binder.bind(B, to=C)
    private_binder.expose(B)

    binder = bind_.create_binder()
    binder.bind(D)

    injector = inject_.create_injector(private_binder, binder)
    d = injector.get_instance(D)
    assert isinstance(d, D)
    assert isinstance(d.b, C)
    assert isinstance(d.b.a, A)

    with pytest.raises(types_.InjectionBlacklistedKeyError):
        injector.get_instance(A)

    with pytest.raises(types_.InjectionBlacklistedKeyError):
        injector.get_instance(C)


def test_nested_private():
    binder0 = bind_.create_binder()
    binder0.new_set_binder(int).bind(to_instance=-1)
    binder0.new_set_binder(int).bind(to_instance=0)
    injector0 = inject_.create_injector(binder0)

    binder1 = bind_.create_binder()
    binder1.new_set_binder(int).bind(to_instance=1)
    injector1 = injector0.create_child(binder1)

    binder2 = bind_.create_binder()
    binder2.new_set_binder(int).bind(to_instance=2)
    injector2 = injector0.create_child(binder2)

    print(injector0.get_instance(ta.Set[int]))
    print(injector0.get_instance(ta.Set[int]))

    # FIXME: SetProvider.__call__ -> get_bindings parent=True?
    print(injector1.get_instance(ta.Set[int]))
    print(injector2.get_instance(ta.Set[int]))


def test_dataclasses():
    @dc.dataclass()
    class C:
        x: int

    binder = bind_.create_binder()
    binder.bind(420)
    binder.bind(C)

    injector = inject_.create_injector(binder)
    c = injector.get_instance(C)
    assert isinstance(c, C)
    assert c.x == 420
