"""
TODO:
 - share makefile somehow (dev task really)
 - ! change makefile to mv g4 to antlr/, generate there, then rm
  - NOPE. not sufficient. find all dirs with g4, copy all g4's to antlr, run all, delete all
   - find baseband -name '*.g4' | xargs -n1 dirname | sort | uniq
  - add TRY=0 for cp/paste to baseband lol
 - tok:node matching
  - look at how nodes are stored already
 - higher level ast tools?
 - streaming support is NOT SUPPORTED
  - unlike pyyaml
  - marks DO NOT NEED BUF PTR
 - binary?
  - whatever antlr does?
 - presto shit:
  - error handling
   - attempt to continue?
   - suggestions
  - case insensitive
  - delimiter lexer
  - statement splitter
   - prob configurable
   - how tf is this diff from delimited lexer

MINE:
 - antlr, obviously
 - lib2to3 - patterns
  - /fixes subdir

https://tomassetti.me/antlr-mega-tutorial/
"""
import typing as ta

from .. import dataclasses as dc
from .. import lang
from .._vendor import antlr4


LexerT = ta.TypeVar('LexerT', bound=antlr4.Lexer, covariant=True)
ParserT = ta.TypeVar('ParserT', bound=antlr4.Parser, covariant=True)


class Mark(dc.Pure):
    line: int
    column: int


class Parse(dc.Pure):
    pass


def parse(
        buf: str,
        lexer_cls: ta.Type[LexerT],
        parser_cls: ta.Type[ParserT]
) -> ParserT:
    lexer = lexer_cls(antlr4.InputStream(buf))
    stream = antlr4.CommonTokenStream(lexer)
    stream.fill()
    return parser_cls(stream)


class ParseException(Exception):
    pass


class SilentRaisingErrorListener(antlr4.error.ErrorListener.ErrorListener):

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise ParseException(recognizer, offendingSymbol, line, column, msg, e)


class InputStream(lang.Protocol):

    @property
    def index(self) -> int:
        raise NotImplementedError

    @property
    def size(self) -> int:
        raise NotImplementedError

    # Reset the stream so that it's in the same state it was when the object was created *except* the data array is not
    # touched.
    def reset(self) -> None:
        raise NotImplementedError

    def consume(self) -> None:
        raise NotImplementedError

    def LA(self, offset: int):
        raise NotImplementedError

    def LT(self, offset: int):
        raise NotImplementedError

    # mark/release do nothing; we have entire buffer
    def mark(self):
        raise NotImplementedError

    def release(self, marker: int):
        raise NotImplementedError

    # consume() ahead until p==_index; can't just set p=_index as we must update line and column. If we seek backwards,
    # just set p
    def seek(self, _index: int):
        raise NotImplementedError

    def getText(self, start: int, stop: int) -> str:
        raise NotImplementedError

    def __str__(self) -> str:
        raise NotImplementedError
