# flake8: noqa
# type: ignore
# Generated from Pep508.g4 by ANTLR 4.8
from ...._vendor.antlr4 import *
if __name__ is not None and "." in __name__:
    from .Pep508Parser import Pep508Parser
else:
    from Pep508Parser import Pep508Parser

# This class defines a complete generic visitor for a parse tree produced by Pep508Parser.

class Pep508Visitor(ParseTreeVisitor):

    # Visit a parse tree produced by Pep508Parser#spec.
    def visitSpec(self, ctx:Pep508Parser.SpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Pep508Parser#nameReq.
    def visitNameReq(self, ctx:Pep508Parser.NameReqContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Pep508Parser#name.
    def visitName(self, ctx:Pep508Parser.NameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Pep508Parser#identifier.
    def visitIdentifier(self, ctx:Pep508Parser.IdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Pep508Parser#identifierEnd.
    def visitIdentifierEnd(self, ctx:Pep508Parser.IdentifierEndContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Pep508Parser#extras.
    def visitExtras(self, ctx:Pep508Parser.ExtrasContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Pep508Parser#extrasList.
    def visitExtrasList(self, ctx:Pep508Parser.ExtrasListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Pep508Parser#versionspec.
    def visitVersionspec(self, ctx:Pep508Parser.VersionspecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Pep508Parser#versionMany.
    def visitVersionMany(self, ctx:Pep508Parser.VersionManyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Pep508Parser#versionOne.
    def visitVersionOne(self, ctx:Pep508Parser.VersionOneContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Pep508Parser#versionCmp.
    def visitVersionCmp(self, ctx:Pep508Parser.VersionCmpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Pep508Parser#version.
    def visitVersion(self, ctx:Pep508Parser.VersionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Pep508Parser#quotedMarker.
    def visitQuotedMarker(self, ctx:Pep508Parser.QuotedMarkerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Pep508Parser#marker.
    def visitMarker(self, ctx:Pep508Parser.MarkerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Pep508Parser#markerOr.
    def visitMarkerOr(self, ctx:Pep508Parser.MarkerOrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Pep508Parser#markerAnd.
    def visitMarkerAnd(self, ctx:Pep508Parser.MarkerAndContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Pep508Parser#markerExpr.
    def visitMarkerExpr(self, ctx:Pep508Parser.MarkerExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Pep508Parser#markerVar.
    def visitMarkerVar(self, ctx:Pep508Parser.MarkerVarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Pep508Parser#markerOp.
    def visitMarkerOp(self, ctx:Pep508Parser.MarkerOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Pep508Parser#envVar.
    def visitEnvVar(self, ctx:Pep508Parser.EnvVarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Pep508Parser#pythonStr.
    def visitPythonStr(self, ctx:Pep508Parser.PythonStrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Pep508Parser#pythonChar.
    def visitPythonChar(self, ctx:Pep508Parser.PythonCharContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Pep508Parser#urlReq.
    def visitUrlReq(self, ctx:Pep508Parser.UrlReqContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Pep508Parser#urlspec.
    def visitUrlspec(self, ctx:Pep508Parser.UrlspecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Pep508Parser#uriReference.
    def visitUriReference(self, ctx:Pep508Parser.UriReferenceContext):
        return self.visitChildren(ctx)



del Pep508Parser
