# flake8: noqa
# type: ignore
# Generated from Pep508.g4 by ANTLR 4.8
from ...._vendor.antlr4 import *
if __name__ is not None and "." in __name__:
    from .Pep508Parser import Pep508Parser
else:
    from Pep508Parser import Pep508Parser

# This class defines a complete listener for a parse tree produced by Pep508Parser.
class Pep508Listener(ParseTreeListener):

    # Enter a parse tree produced by Pep508Parser#oneSpec.
    def enterOneSpec(self, ctx:Pep508Parser.OneSpecContext):
        pass

    # Exit a parse tree produced by Pep508Parser#oneSpec.
    def exitOneSpec(self, ctx:Pep508Parser.OneSpecContext):
        pass


    # Enter a parse tree produced by Pep508Parser#spec.
    def enterSpec(self, ctx:Pep508Parser.SpecContext):
        pass

    # Exit a parse tree produced by Pep508Parser#spec.
    def exitSpec(self, ctx:Pep508Parser.SpecContext):
        pass


    # Enter a parse tree produced by Pep508Parser#nameReq.
    def enterNameReq(self, ctx:Pep508Parser.NameReqContext):
        pass

    # Exit a parse tree produced by Pep508Parser#nameReq.
    def exitNameReq(self, ctx:Pep508Parser.NameReqContext):
        pass


    # Enter a parse tree produced by Pep508Parser#name.
    def enterName(self, ctx:Pep508Parser.NameContext):
        pass

    # Exit a parse tree produced by Pep508Parser#name.
    def exitName(self, ctx:Pep508Parser.NameContext):
        pass


    # Enter a parse tree produced by Pep508Parser#identifier.
    def enterIdentifier(self, ctx:Pep508Parser.IdentifierContext):
        pass

    # Exit a parse tree produced by Pep508Parser#identifier.
    def exitIdentifier(self, ctx:Pep508Parser.IdentifierContext):
        pass


    # Enter a parse tree produced by Pep508Parser#extras.
    def enterExtras(self, ctx:Pep508Parser.ExtrasContext):
        pass

    # Exit a parse tree produced by Pep508Parser#extras.
    def exitExtras(self, ctx:Pep508Parser.ExtrasContext):
        pass


    # Enter a parse tree produced by Pep508Parser#extrasList.
    def enterExtrasList(self, ctx:Pep508Parser.ExtrasListContext):
        pass

    # Exit a parse tree produced by Pep508Parser#extrasList.
    def exitExtrasList(self, ctx:Pep508Parser.ExtrasListContext):
        pass


    # Enter a parse tree produced by Pep508Parser#versionspec.
    def enterVersionspec(self, ctx:Pep508Parser.VersionspecContext):
        pass

    # Exit a parse tree produced by Pep508Parser#versionspec.
    def exitVersionspec(self, ctx:Pep508Parser.VersionspecContext):
        pass


    # Enter a parse tree produced by Pep508Parser#versionMany.
    def enterVersionMany(self, ctx:Pep508Parser.VersionManyContext):
        pass

    # Exit a parse tree produced by Pep508Parser#versionMany.
    def exitVersionMany(self, ctx:Pep508Parser.VersionManyContext):
        pass


    # Enter a parse tree produced by Pep508Parser#versionOne.
    def enterVersionOne(self, ctx:Pep508Parser.VersionOneContext):
        pass

    # Exit a parse tree produced by Pep508Parser#versionOne.
    def exitVersionOne(self, ctx:Pep508Parser.VersionOneContext):
        pass


    # Enter a parse tree produced by Pep508Parser#versionCmp.
    def enterVersionCmp(self, ctx:Pep508Parser.VersionCmpContext):
        pass

    # Exit a parse tree produced by Pep508Parser#versionCmp.
    def exitVersionCmp(self, ctx:Pep508Parser.VersionCmpContext):
        pass


    # Enter a parse tree produced by Pep508Parser#version.
    def enterVersion(self, ctx:Pep508Parser.VersionContext):
        pass

    # Exit a parse tree produced by Pep508Parser#version.
    def exitVersion(self, ctx:Pep508Parser.VersionContext):
        pass


    # Enter a parse tree produced by Pep508Parser#quotedMarker.
    def enterQuotedMarker(self, ctx:Pep508Parser.QuotedMarkerContext):
        pass

    # Exit a parse tree produced by Pep508Parser#quotedMarker.
    def exitQuotedMarker(self, ctx:Pep508Parser.QuotedMarkerContext):
        pass


    # Enter a parse tree produced by Pep508Parser#marker.
    def enterMarker(self, ctx:Pep508Parser.MarkerContext):
        pass

    # Exit a parse tree produced by Pep508Parser#marker.
    def exitMarker(self, ctx:Pep508Parser.MarkerContext):
        pass


    # Enter a parse tree produced by Pep508Parser#markerOr.
    def enterMarkerOr(self, ctx:Pep508Parser.MarkerOrContext):
        pass

    # Exit a parse tree produced by Pep508Parser#markerOr.
    def exitMarkerOr(self, ctx:Pep508Parser.MarkerOrContext):
        pass


    # Enter a parse tree produced by Pep508Parser#markerAnd.
    def enterMarkerAnd(self, ctx:Pep508Parser.MarkerAndContext):
        pass

    # Exit a parse tree produced by Pep508Parser#markerAnd.
    def exitMarkerAnd(self, ctx:Pep508Parser.MarkerAndContext):
        pass


    # Enter a parse tree produced by Pep508Parser#markerExpr.
    def enterMarkerExpr(self, ctx:Pep508Parser.MarkerExprContext):
        pass

    # Exit a parse tree produced by Pep508Parser#markerExpr.
    def exitMarkerExpr(self, ctx:Pep508Parser.MarkerExprContext):
        pass


    # Enter a parse tree produced by Pep508Parser#markerVar.
    def enterMarkerVar(self, ctx:Pep508Parser.MarkerVarContext):
        pass

    # Exit a parse tree produced by Pep508Parser#markerVar.
    def exitMarkerVar(self, ctx:Pep508Parser.MarkerVarContext):
        pass


    # Enter a parse tree produced by Pep508Parser#markerOp.
    def enterMarkerOp(self, ctx:Pep508Parser.MarkerOpContext):
        pass

    # Exit a parse tree produced by Pep508Parser#markerOp.
    def exitMarkerOp(self, ctx:Pep508Parser.MarkerOpContext):
        pass


    # Enter a parse tree produced by Pep508Parser#envVar.
    def enterEnvVar(self, ctx:Pep508Parser.EnvVarContext):
        pass

    # Exit a parse tree produced by Pep508Parser#envVar.
    def exitEnvVar(self, ctx:Pep508Parser.EnvVarContext):
        pass


    # Enter a parse tree produced by Pep508Parser#pythonStr.
    def enterPythonStr(self, ctx:Pep508Parser.PythonStrContext):
        pass

    # Exit a parse tree produced by Pep508Parser#pythonStr.
    def exitPythonStr(self, ctx:Pep508Parser.PythonStrContext):
        pass


    # Enter a parse tree produced by Pep508Parser#pythonChar.
    def enterPythonChar(self, ctx:Pep508Parser.PythonCharContext):
        pass

    # Exit a parse tree produced by Pep508Parser#pythonChar.
    def exitPythonChar(self, ctx:Pep508Parser.PythonCharContext):
        pass



del Pep508Parser
