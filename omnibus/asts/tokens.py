import typing as ta

from . import analysis as ana
from . import nodes as no
from .. import check
from .. import collections as ocol
from .. import properties
from .._vendor import antlr4
from ..antlr import tokens


class TokenAnalysis:

    def __init__(self, root: no.Node) -> None:
        super().__init__()

        self._root = check.isinstance(root, no.Node)

        self._basic = ana.basic(self._root)

        self._tok_ana = tokens.TokenAnalysis(self._root.meeta[antlr4.ParserRuleContext])

    @properties.cached
    @property
    def rnodes(self) -> ta.Mapping[no.Node, int]:
        return ocol.IdentityKeyDict(
            (n, self._tok_ana.rctxs[n.meta[antlr4.ParserRuleContext]])
            for n in self._basic.nodes
        )

    def get_node_toks(self, node: no.Node) -> ta.Sequence[antlr4.Token]:
        l = self.rnodes[node]
        try:
            r = next(self._tok_ana.ctxs.itemsfrom(l + 1))[0]
        except StopIteration:
            r = -1
        return self._tok_ana.toks[l:r]

    def get_node_comments(self, node: no.Node) -> ta.Sequence[str]:
        return [t.text for t in self.get_node_toks(node) if t.channel == 1]
