from .. import base
from .. import leaf


def test_trees():
    root = leaf.Success()
    tree = base.BehaviorTree(root, None)
    print(tree)
