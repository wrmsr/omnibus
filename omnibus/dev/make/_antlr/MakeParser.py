# flake8: noqa
# Generated from Make.g4 by ANTLR 4.8
# encoding: utf-8
from ...._vendor.antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\2")
        buf.write("\7\4\2\t\2\3\2\3\2\3\2\2\2\3\2\2\2\2\5\2\4\3\2\2\2\4\5")
        buf.write("\7\2\2\3\5\3\3\2\2\2\2")
        return buf.getvalue()


class MakeParser ( Parser ):

    grammarFileName = "Make.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [  ]

    symbolicNames = [  ]

    RULE_makefile = 0

    ruleNames =  [ "makefile" ]

    EOF = Token.EOF
    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.8")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class MakefileContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(MakeParser.EOF, 0)

        def getRuleIndex(self):
            return MakeParser.RULE_makefile

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMakefile" ):
                listener.enterMakefile(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMakefile" ):
                listener.exitMakefile(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMakefile" ):
                return visitor.visitMakefile(self)
            else:
                return visitor.visitChildren(self)




    def makefile(self):

        localctx = MakeParser.MakefileContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_makefile)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 2
            self.match(MakeParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx
