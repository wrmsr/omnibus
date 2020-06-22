import typing as ta

from .. import check
from .._vendor import antlr4
from .._vendor.antlr4.error.Errors import LexerNoViableAltException


class DelimitingLexer(antlr4.Lexer):

    def __init__(
            self,
            *args,
            delimiter_token: ta.Any,
            delimiters: ta.Iterable[str],
            **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        self._delimiter_token = delimiter_token
        self._delimiters = set(check.not_isinstance(delimiters, str))

    def nextToken(self):
        if self._input is None:
            raise antlr4.IllegalStateException("nextToken requires a non-null input stream.")

        tokenStartMarker = self._input.mark()
        try:
            while True:
                if self._hitEOF:
                    self.emitEOF()
                    return self._token

                self._token = None
                self._channel = antlr4.Token.DEFAULT_CHANNEL
                self._tokenStartCharIndex = self._input.index
                self._tokenStartColumn = self._interp.column
                self._tokenStartLine = self._interp.line
                self._text = None

                continueOuter = False
                while True:
                    self._type = antlr4.Token.INVALID_TYPE
                    ttype = self.SKIP

                    for delimiter in self._delimiters:
                        if self._match_delimiter(delimiter):
                            ttype = self._delimiter_token
                            break
                    else:
                        try:
                            ttype = self._interp.match(self._input, self._mode)
                        except LexerNoViableAltException as e:
                            self.notifyListeners(e)  # report error
                            self.recover(e)

                    if self._input.LA(1) == antlr4.Token.EOF:
                        self._hitEOF = True

                    if self._type == antlr4.Token.INVALID_TYPE:
                        self._type = ttype

                    if self._type == self.SKIP:
                        continueOuter = True
                        break

                    if self._type != self.MORE:
                        break

                if continueOuter:
                    continue

                if self._token is None:
                    self.emit()

                return self._token

        finally:
            self._input.release(tokenStartMarker)

    def _match_delimiter(self, delimiter: str) -> bool:
        for i, c in enumerate(delimiter):
            if self._input.LA(i + 1) != c:
                return False
        self._input.seek(self._input.index + len(delimiter))
        return True
