# flake8: noqa
# Generated from CMake.g4 by ANTLR 4.8
from ...._vendor.antlr4 import *
if __name__ is not None and "." in __name__:
    from .CMakeParser import CMakeParser
else:
    from CMakeParser import CMakeParser

# This class defines a complete generic visitor for a parse tree produced by CMakeParser.

class CMakeVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by CMakeParser#body.
    def visitBody(self, ctx:CMakeParser.BodyContext):
        return self.visitChildren(ctx)



del CMakeParser
