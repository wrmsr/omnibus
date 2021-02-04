import string
import typing as ta

from ... import check
from ... import collections as col
from ... import dataclasses as dc
from ... import properties
from .base import Node


class Op(Node, abstract=True):
    GLYPH_WORD_SEP: ta.ClassVar[str] = '_'
    GLYPH_WORD_CHARS: ta.ClassVar[ta.AbstractSet[str]] = {*string.ascii_lowercase, GLYPH_WORD_SEP}

    glyph: str

    dc.validate(lambda glyph: not set(glyph) & set(string.whitespace))

    @properties.cached
    def is_word(self) -> bool:
        return not (set(self.glyph) - Op.GLYPH_WORD_CHARS)

    @properties.cached
    def glyph_parts(self) -> ta.Sequence[str]:
        return self.glyph.split(Op.GLYPH_WORD_SEP)


class BinOp(dc.ValueEnum, Op):
    pass


class BinOps(BinOp.Values):
    ADD = BinOp('+')
    SUB = BinOp('-')
    MUL = BinOp('*')
    DIV = BinOp('/')


class CmpOp(dc.ValueEnum, Op):
    pass


class CmpOps(CmpOp.Values):
    EQ = CmpOp('==')
    NE = CmpOp('!=')
    GT = CmpOp('>')
    GE = CmpOp('>=')
    LT = CmpOp('<')
    LE = CmpOp('<=')

    IS = CmpOp('is')
    IS_NOT = CmpOp('is_not')

    IN = CmpOp('in')
    NOT_IN = CmpOp('not_in')


class UnaryOp(dc.ValueEnum, Op):
    pass


class UnaryOps(UnaryOp.Values):
    NOT = UnaryOp('not')


OPS_BY_GLYPH: ta.Mapping[str, Op] = col.unique_dict((o.glyph, o) for c in [
    BinOps,
    CmpOps,
    UnaryOps,
] for o in c._by_name.values() for o in [check.isinstance(o, Op)])
