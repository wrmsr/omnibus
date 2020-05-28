import glob
import os.path
import time
import typing as ta

from ..._vendor import antlr4
from .._antlr.Python3Lexer import Python3Lexer
from .._antlr.Python3Listener import Python3Listener
from .._antlr.Python3Parser import Python3Parser


class Python3PrintListener(Python3Listener):

    def __init__(
            self,
            stream: antlr4.BufferedTokenStream.BufferedTokenStream,
            parser: Python3Parser
    ) -> None:
        super().__init__()
        self._stream = stream
        self._parser = parser

    def enterCompoundStmt(self, ctx: Python3Parser.CompoundStmtContext):
        for t in (self._stream.getHiddenTokensToRight(ctx.start.tokenIndex, 2) or []):
            print(t.text)


def var_fn(a: int, *b: ta.Dict[str, ta.Tuple[int, float]], **c: ta.Callable[..., float]) -> ta.List[int]:  # noqa
    pass


def test_internal():
    from ...antlr.antlr import patch_speedeups
    patch_speedeups()

    def run(buf):
        lexer = Python3Lexer(antlr4.InputStream(buf))
        stream = antlr4.CommonTokenStream(lexer)
        stream.fill()
        parser = Python3Parser(stream)
        tree = parser.fileInput()
        printer = Python3PrintListener(stream, parser)
        walker = antlr4.ParseTreeWalker()
        walker.walk(printer, tree)

    print()
    dp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../caches'))
    for fp in sorted(glob.glob(f'{dp}/**/*.py', recursive=True)):
        with open(fp, 'r') as f:
            buf = f.read()

        start = time.time()
        run(buf)
        end = time.time()
        print('%-80s: %0.2f' % (fp, end - start,))
