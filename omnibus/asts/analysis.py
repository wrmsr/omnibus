import typing as ta

from . import nodes as no
from .. import collections as ocol
from .. import properties


T = ta.TypeVar('T')
NodeGen = ta.Generator[no.Node, None, None]


class BasicAnalysis:

    def __init__(self, root: no.Node) -> None:
        super().__init__()

        self._root = root

        def walk(cur: no.Node) -> None:
            if cur in node_set:
                raise Exception(f'Duplicate node: {cur}', cur)
            nodes.append(cur)
            node_set.add(cur)
            for child in cur.children:
                walk(child)

        self._nodes = nodes = []
        self._node_set = node_set = ocol.IdentitySet()
        walk(root)

        self._node_sets_by_type: ta.Dict[type, ta.AbstractSet[no.Node]] = {}

    @property
    def root(self) -> no.Node:
        return self._root

    @property
    def nodes(self) -> ta.Sequence[no.Node]:
        return self._nodes

    @property
    def node_set(self) -> ta.AbstractSet[no.Node]:
        return self._node_set

    def get_node_type_set(self, ty: ta.Type[T]) -> ta.AbstractSet[T]:
        try:
            return self._node_sets_by_type[ty]
        except KeyError:
            ret = self._node_sets_by_type[ty] = ocol.IdentitySet(n for n in self.nodes if isinstance(n, ty))
            return ret

    @properties.cached
    def parents_by_node(self) -> ta.Mapping[no.Node, no.Node]:
        def walk(cur: no.Node) -> None:
            for child in cur.children:
                dct[child] = cur
                walk(child)
        dct = ocol.IdentityKeyDict()
        walk(self._root)
        return dct

    def yield_ancestors(self, node: no.Node) -> NodeGen:
        cur = node
        while True:
            cur = self.parents_by_node.get(cur)
            if cur is None:
                break
            yield cur

    def get_first_parent_of_type(self, node: no.Node, ty: ta.Type[T]) -> ta.Optional[no.Node]:
        for cur in self.yield_ancestors(node):
            if isinstance(cur, ty):
                return cur
        return None

    @properties.cached
    def child_sets_by_node(self) -> ta.Mapping[no.Node, ta.AbstractSet[no.Node]]:
        def walk(cur: no.Node) -> None:
            dct[cur] = ocol.IdentitySet(cur.children)
            for child in cur.children:
                walk(child)
        dct = ocol.IdentityKeyDict()
        walk(self._root)
        return dct


basic = BasicAnalysis
