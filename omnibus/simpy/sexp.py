"""
TODO:
 - usecase:
  - when don't have AST access (omni core)
  - when want a non-reprable const but but dont want to do ast construction
  - as shorthand when transforming

['def', 'f', ['x', 'y']
 ['return' ['+', 'x', 'y']]]

['def', 'say_hello', []
 ['print', c('hi')]]

['def', 'sum_pt', ['pt'],
 ['return', ['+', 'pt.x', 'pt.y']]]
"""
import functools
import typing as ta

from . import nodes as no
from .. import check


def c(o: ta.Any) -> no.Node:
    return no.Const(o)


def xlat(obj: ta.Any) -> no.Node:
    if isinstance(obj, no.Node):
        return obj

    if isinstance(obj, (int, float)):
        return no.Const(obj)

    if isinstance(obj, str):
        if obj and obj[0] == '~':
            return no.Const(obj[1:])
        else:
            return no.GetVar(no.Ident(obj))

    if isinstance(obj, list):
        args = list(obj)
        shift = functools.partial(args.pop, 0)
        tag = shift()

        if tag == 'def':
            name = no.Ident(shift())
            fnargs = no.Args([no.Arg(no.Ident(a)) for a in shift()])
            body = []
            for b in args:
                xb = xlat(b)
                if isinstance(xb, no.Stmt):
                    xs = xb
                elif isinstance(xb, no.Expr):
                    xs = no.ExprStmt(xb)
                else:
                    raise TypeError(xb)
                body.append(xs)
            return no.Fn(
                name,
                fnargs,
                body,
            )

        elif tag == 'return':
            if args:
                value = xlat(shift())
            else:
                value = None
            check.empty(args)
            return no.Return(value)

        elif tag in no.OPS_BY_GLYPH:
            op = no.OPS_BY_GLYPH[tag]

            if isinstance(op, no.BinOp):
                left, right = map(xlat, args)
                return no.BinExpr(
                    left,
                    op,
                    right,
                )

            elif isinstance(op, no.CmpOp):
                left, right = map(xlat, args)
                return no.CmpExpr(
                    left,
                    op,
                    right,
                )

            elif isinstance(op, no.UnaryOp):
                value = xlat(check.single(args))
                return no.UnaryExpr(
                    op,
                    value,
                )

            else:
                raise TypeError(op)

        else:
            fn = xlat(tag)
            cargs = []
            for a in args:
                xa = xlat(a)
                if isinstance(xa, no.Expr):
                    xe = xa
                else:
                    raise TypeError(xa)
                cargs.append(xe)
            return no.Call(
                fn,
                cargs,
            )

    raise TypeError(obj)
