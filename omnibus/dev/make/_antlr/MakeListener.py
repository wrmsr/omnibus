# flake8: noqa
# Generated from Make.g4 by ANTLR 4.8
from ...._vendor.antlr4 import *
if __name__ is not None and "." in __name__:
    from .MakeParser import MakeParser
else:
    from MakeParser import MakeParser

# This class defines a complete listener for a parse tree produced by MakeParser.
class MakeListener(ParseTreeListener):

    # Enter a parse tree produced by MakeParser#makefile.
    def enterMakefile(self, ctx:MakeParser.MakefileContext):
        pass

    # Exit a parse tree produced by MakeParser#makefile.
    def exitMakefile(self, ctx:MakeParser.MakefileContext):
        pass



del MakeParser
