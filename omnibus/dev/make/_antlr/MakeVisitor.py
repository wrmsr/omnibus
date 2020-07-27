# flake8: noqa
# type: ignore
# Generated from Make.g4 by ANTLR 4.8
from ...._vendor.antlr4 import *
if __name__ is not None and "." in __name__:
    from .MakeParser import MakeParser
else:
    from MakeParser import MakeParser

# This class defines a complete generic visitor for a parse tree produced by MakeParser.

class MakeVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by MakeParser#makefile.
    def visitMakefile(self, ctx:MakeParser.MakefileContext):
        return self.visitChildren(ctx)



del MakeParser
