import typing as ta

from .. import nodes as no
from ... import dispatch
from .contexts import EvalContext


class Evaluator(dispatch.Class):
    __call__ = dispatch.property()

    def __call__(self, node: no.Node, ctx: EvalContext) -> ta.Tuple[ta.Any, EvalContext]:  # noqa
        raise TypeError(node)

    def __call__(self, node: no.BinExpr, ctx: EvalContext) -> ta.Tuple[ta.Any, EvalContext]:  # noqa
        left, ctx = self(node.left, ctx)
        right, ctx = self(node.right, ctx)
        if node.op is no.BinOps.ADD:
            ret = left + right
        else:
            raise ValueError(node.op)
        return ret, ctx

    def __call__(self, node: no.Break, ctx: EvalContext) -> ta.Tuple[ta.Any, EvalContext]:  # noqa
        raise NotImplementedError

    def __call__(self, node: no.Call, ctx: EvalContext) -> ta.Tuple[ta.Any, EvalContext]:  # noqa
        raise NotImplementedError

    def __call__(self, node: no.CmpExpr, ctx: EvalContext) -> ta.Tuple[ta.Any, EvalContext]:  # noqa
        raise NotImplementedError

    def __call__(self, node: no.Const, ctx: EvalContext) -> ta.Tuple[ta.Any, EvalContext]:  # noqa
        return node.value, ctx

    def __call__(self, node: no.Continue, ctx: EvalContext) -> ta.Tuple[ta.Any, EvalContext]:  # noqa
        raise NotImplementedError

    def __call__(self, node: no.ExprStmt, ctx: EvalContext) -> ta.Tuple[ta.Any, EvalContext]:  # noqa
        raise NotImplementedError

    def __call__(self, node: no.ForIter, ctx: EvalContext) -> ta.Tuple[ta.Any, EvalContext]:  # noqa
        raise NotImplementedError

    def __call__(self, node: no.GetAttr, ctx: EvalContext) -> ta.Tuple[ta.Any, EvalContext]:  # noqa
        raise NotImplementedError

    def __call__(self, node: no.GetItem, ctx: EvalContext) -> ta.Tuple[ta.Any, EvalContext]:  # noqa
        raise NotImplementedError

    def __call__(self, node: no.GetVar, ctx: EvalContext) -> ta.Tuple[ta.Any, EvalContext]:  # noqa
        raise NotImplementedError

    def __call__(self, node: no.If, ctx: EvalContext) -> ta.Tuple[ta.Any, EvalContext]:  # noqa
        raise NotImplementedError

    def __call__(self, node: no.Pass, ctx: EvalContext) -> ta.Tuple[ta.Any, EvalContext]:  # noqa
        raise NotImplementedError

    def __call__(self, node: no.Raise, ctx: EvalContext) -> ta.Tuple[ta.Any, EvalContext]:  # noqa
        raise NotImplementedError

    def __call__(self, node: no.Return, ctx: EvalContext) -> ta.Tuple[ta.Any, EvalContext]:  # noqa
        raise NotImplementedError

    def __call__(self, node: no.SetAttr, ctx: EvalContext) -> ta.Tuple[ta.Any, EvalContext]:  # noqa
        raise NotImplementedError

    def __call__(self, node: no.SetItem, ctx: EvalContext) -> ta.Tuple[ta.Any, EvalContext]:  # noqa
        raise NotImplementedError

    def __call__(self, node: no.SetVar, ctx: EvalContext) -> ta.Tuple[ta.Any, EvalContext]:  # noqa
        raise NotImplementedError

    def __call__(self, node: no.UnaryExpr, ctx: EvalContext) -> ta.Tuple[ta.Any, EvalContext]:  # noqa
        raise NotImplementedError
