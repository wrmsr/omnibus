from . import nodes as no
from .. import check
from ..graphs import trees


class BasicAnalysis(trees.BasicTreeAnalysis[no.Node]):

    def __init__(
            self,
            root: no.Node,
            walker: trees.NodeWalker[no.Node] = lambda n: n.children,
            **kwargs,
    ) -> None:
        super().__init__(check.isinstance(root, no.Node), walker, **kwargs)


def basic(root: no.Node) -> trees.BasicTreeAnalysis[no.Node]:
    return BasicAnalysis.from_nodal(root)
