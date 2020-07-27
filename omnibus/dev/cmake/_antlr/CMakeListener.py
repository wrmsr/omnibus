# flake8: noqa
# type: ignore
# Generated from CMake.g4 by ANTLR 4.8
from ...._vendor.antlr4 import *
if __name__ is not None and "." in __name__:
    from .CMakeParser import CMakeParser
else:
    from CMakeParser import CMakeParser

# This class defines a complete listener for a parse tree produced by CMakeParser.
class CMakeListener(ParseTreeListener):

    # Enter a parse tree produced by CMakeParser#body.
    def enterBody(self, ctx:CMakeParser.BodyContext):
        pass

    # Exit a parse tree produced by CMakeParser#body.
    def exitBody(self, ctx:CMakeParser.BodyContext):
        pass



del CMakeParser
