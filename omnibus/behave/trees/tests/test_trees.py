import random

from .. import base
from .. import leaf
from .... import defs
from ..base import Task


class Dog:

    def __init__(self, name: str, btree: base.BehaviorTree['Dog'] = None) -> None:
        super().__init__()

        self._name = name
        self._btree = btree
        if btree is not None:
            btree.object = self

    defs.repr()

    def bark(self) -> None:
        print(f'{self}: bark')


class BarkTask(leaf.LeafTask[Dog]):

    defs.repr()

    _t = 0

    def start(self) -> None:
        super().start()
        self._t = random.randint(1, 5)

    def execute(self) -> Task.Status:
        print(f'{self} barking {self._t} times')
        for i in range(self._t):
            self.object.bark()
        return base.Task.Status.SUCCEEDED


def test_trees():
    # root = leaf.Success()
    root = BarkTask()

    tree = base.BehaviorTree(root)

    dog = Dog('dog1', tree)  # noqa

    for _ in range(20):
        tree.step()
